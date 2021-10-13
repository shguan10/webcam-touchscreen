import cv2 
import numpy as np
import pdb

MAXCOLS = 1280
MAXROWS = 720
RADIUS = 10
SAVEDIR = "data"

def generate_random_circle():
  return (np.random.rand(2) * [MAXROWS,MAXCOLS]).astype(int)

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

  #To set the resolution
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAXROWS)

  circle_position = generate_random_circle()

  while True:
    _, frame = cap.read()

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