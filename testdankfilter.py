import cv2
import numpy as np
import pdb
import os, sys

MAXCOLS = 1280
MAXROWS = 720

TRAP_TOP_LEFT = (50,470)
TRAP_TOP_RIGHT = (50,780)
TRAP_BOT_LEFT = (MAXROWS,0)
TRAP_BOT_RIGHT = (MAXROWS,MAXCOLS)
RADIUS = 10

THRESHOLD = 8000

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
  crow,ccol = circle_position.astype(int)
  
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

def main():
  frames = [open_image("background/"+file) for file in os.listdir("background")]
  frames = np.array(frames)
  background = frames.mean(axis=0)

  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAXROWS)

  while True:
    _, frame = cap.read()
    keypress = cv2.waitKey(1)

    cv2.imshow("filtered",frame)

    if keypress == ord("q"):
      break

  while True:
    _, frame = cap.read()
    keypress = cv2.waitKey(1)

    frame = background_filter(frame,background)
    frame = fuzzy_mask(frame)
    centroid = get_centroid(frame)

    if (centroid**2).sum() > 10:
      print(centroid)
      canvas = np.array(frame)
      canvas = draw_circle(canvas,centroid)
      cv2.imshow("filtered",canvas)
    else:
      cv2.imshow("filtered",frame)

    if keypress == ord("q"):
      break

  cv2.destroyAllWindows()

if __name__=="__main__":
  main()