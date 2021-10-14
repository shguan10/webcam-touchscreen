import cv2
import numpy as np
import pdb
import os, sys

MAXCOLS = 1280
MAXROWS = 720

WIN = (325,63)

TRAP_TOP_LEFT = (50,470)
TRAP_TOP_RIGHT = (50,780)
TRAP_BOT_LEFT = (MAXROWS,0)
TRAP_BOT_RIGHT = (MAXROWS,MAXCOLS)
# RADIUS = 10
RADIUS = 20

THRESHOLD = 8000
BACKGROUND_FNAME = "background.jpg"

def is_right_of(linep1,linep2,p):
  # use the cross product to determine whether p is to the right of the line from linep1 to linep2 (right thumb out of the screen)
  # all points are in (row,col) = (y,x) format
  return ((linep2[1]-linep1[1])*(p[0]-linep1[0])-(linep2[0]-linep1[0])*(p[1]-linep1[1]))>0

def is_valid(p):
  if p[0]<TRAP_TOP_LEFT[0]: return False
  if p[0]>TRAP_BOT_LEFT[0]: return False
  if not is_right_of(TRAP_BOT_LEFT,TRAP_TOP_LEFT,p): return False
  if is_right_of(TRAP_BOT_RIGHT,TRAP_TOP_RIGHT,p): return False
  return True

def generate_random_circle():
  p = (0,0)
  while not is_valid(p):
    p = (np.random.rand(2) * [MAXROWS,MAXCOLS]).astype(int)
  return p

def open_image(fname="data/346_637.jpg"):
  frame = cv2.imread(fname)
  frame = np.asarray(frame)
  return frame

def fuzzy_mask(frame,pixels=(169,207,244),dalpha=0.1,dr=2,dg=2,db=2):
  b,g,r = pixels
  
  maxr = (r + dr)*(1+dalpha)
  minr = (r - dr)*(1-dalpha)

  maxg = (g + dg)*(1+dalpha)
  ming = (g - dg)*(1-dalpha)

  maxb = (b + db)*(1+dalpha)
  minb = (b - db)*(1-dalpha)

  mask = frame[:,:,0] > minb
  mask &= frame[:,:,0] < maxb
  mask &= frame[:,:,1] > ming
  mask &= frame[:,:,1] < maxg
  mask &= frame[:,:,2] > minr
  mask &= frame[:,:,2] < maxr
  mask = (mask * 255).astype(frame.dtype)
  # pdb.set_trace()
  frame = cv2.bitwise_and(frame,frame,mask=mask)
  
  return frame

def background_filter(frame,background,threshold=THRESHOLD):
  # filter out the background
  diff = frame - background
  dnorm = (diff*diff).sum(axis=2)

  mask = dnorm > threshold
  mask = (mask * 255).astype(frame.dtype)
  frame = cv2.bitwise_and(frame,frame,mask=mask)

  return frame 

def get_centroid(frame):
  # gets the centroid of the non-filtered stuff
  mask = frame.sum(axis=2)>0
  # pdb.set_trace()
  nonzeros = np.argwhere(mask>0)
  centroid = nonzeros.sum(0)/(nonzeros.shape[0])
  return centroid

def draw_circle(frame,circle_position):
  # pdb.set_trace()
  crow,ccol = circle_position
  crow = int(crow)
  ccol = int(ccol)
  
  row_one = crow - RADIUS
  row_two = crow + RADIUS
  col_one  = ccol - RADIUS
  col_two = ccol + RADIUS

  cv2.rectangle(frame, 
                (col_one, row_one),
                (col_two, row_two),
                (0, 255, 0), 
                10)

  return frame

def read_circle(frame,circle_position):
  crow,ccol = circle_position
  crow = int(crow)
  ccol = int(ccol)
  
  row_one = crow - RADIUS
  row_two = crow + RADIUS
  col_one  = ccol - RADIUS
  col_two = ccol + RADIUS

  return frame[row_one:row_two,col_one:col_two,:]

def calculate_background_frame():
  frames = [open_image("background/"+file) for file in os.listdir("background")]
  frames = np.array(frames)
  background = frames.mean(axis=0)
  return background

def sample_finger(cap):
  circle_position = (600,800)
  while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    keypress = cv2.waitKey(1)

    canvas = np.array(frame)

    canvas = draw_circle(canvas,circle_position)

    cv2.imshow("sampling finger",canvas)
    cv2.moveWindow("sampling finger",WIN[0],WIN[1])
    if keypress == ord(" "):
      circle = read_circle(frame,circle_position)
      cv2.destroyAllWindows()

      return circle.mean(0).mean(0).astype(int)
    
def sample_background(cap):
  backgrounds = []
  times = 1
  while times>0:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    keypress = cv2.waitKey(1)

    name = "sampling background * "+str(times)+" times"
    cv2.imshow(name,frame)
    cv2.moveWindow(name,WIN[0],WIN[1])

    if keypress == ord(" "):
      times-=1
      backgrounds.append(frame)
  arr = np.array(backgrounds)
  arr = arr.mean(0)
  cv2.imwrite(BACKGROUND_FNAME,arr)
  cv2.destroyAllWindows()

  return arr

def filter(cap,finger_pixels,background):
  cv2.namedWindow("filtered")
  cv2.moveWindow("filtered",WIN[0],WIN[1])
  
  while True:
    _, frame = cap.read()
    keypress = cv2.waitKey(1)
    frame = cv2.flip(frame, 1)

    frame = background_filter(frame,background)
    frame = fuzzy_mask(frame,pixels=finger_pixels)
    centroid = get_centroid(frame)

    if (centroid**2).sum() > 10:
      # print(centroid)
      canvas = np.array(frame)
      canvas = draw_circle(canvas,centroid)
      cv2.imshow("filtered",canvas)
    else:
      cv2.imshow("filtered",frame)

    if keypress == ord("q"):
      break
  cv2.destroyAllWindows()

def mousecb(event,x,y,flags,userdata):
  if event == cv2.EVENT_LBUTTONDOWN:
    userdata.x = x
    userdata.y = y

class Userdata:
  def __init__(self):
    self.x = None
    self.y = None
    self.frame = None

def get_sample(cap,finger_pixels,background):
  cv2.namedWindow("filtered")
  cv2.moveWindow("filtered",WIN[0],WIN[1])
  ud = Userdata()
  cv2.setMouseCallback("filtered",mousecb,ud)

  while ud.x is None:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame = background_filter(frame,background)
    frame = fuzzy_mask(frame,pixels=finger_pixels)

  cv2.imwrite("data/"+str(ud.x)+"_"+str(ud.y)+".jpg",frame)
  cv2.destroyAllWindows()
  

if __name__=="__main__":
  frame = calculate_background_frame()
  cv2.imwrite(BACKGROUND_FNAME,frame)