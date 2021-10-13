import cv2 
import numpy as np
import pdb

MAXCOLS = 1280
MAXROWS = 720

TRAP_TOP_LEFT = (50,470)
TRAP_TOP_RIGHT = (50,780)
TRAP_BOT_LEFT = (MAXROWS,0)
TRAP_BOT_RIGHT = (MAXROWS,MAXCOLS)
RADIUS = 10
SAVEDIR = "data"

def is_right_of(linep1,linep2,p):
  # use the cross product to determine whether p is to the right of the line from linep1 to linep2 (thumbs up)
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

def save_frame(frame,circle_position):
  name = "/".join([SAVEDIR,
                   str(circle_position[0])+"_"+str(circle_position[1])+".jpg"
                   ])
  cv2.imwrite(name,frame)
  return name

def draw_circle(frame,circle_position):
  
  crow,ccol = circle_position
  
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
  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAXROWS)

  circle_position = generate_random_circle()

  while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    keypress = cv2.waitKey(1)
    draw_circle(frame,circle_position)

    cv2.imshow("Live Feed",frame)

    if keypress == ord(" "):
      save_frame(frame,circle_position)

      circle_position = generate_random_circle()

    elif keypress == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()

if __name__=="__main__":
  main()