import cv2 
import numpy as np
import pdb

import common

def prompted():
  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, common.MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, common.MAXROWS)

  finger_pixels = common.sample_finger(cap)
  background = common.sample_background(cap)

  circle_position = common.generate_random_circle()

  cv2.namedWindow("filtered")
  cv2.moveWindow("filtered",common.WIN[0],common.WIN[1])

  num = 0
  while True:
    _, frame = cap.read()
    keypress = cv2.waitKey(1)

    frame = cv2.flip(frame, 1)
    
    frame = common.background_filter(frame,background)
    frame = common.fuzzy_mask(frame,pixels=finger_pixels)
    canvas = frame.copy()
    canvas = common.draw_circle(canvas,circle_position)
    cv2.imshow("filtered",canvas)

    if keypress == ord(" "):
      cv2.imwrite("data/"+str(circle_position[0])+"_"+str(circle_position[1])+".jpg",frame)
      circle_position = common.generate_random_circle()
      num+=1
      print(num)
    elif keypress == ord("r"):
      circle_position = common.generate_random_circle()
    elif keypress == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()

def moused():
  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, common.MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, common.MAXROWS)

  finger_pixels = common.sample_finger(cap)
  background = common.sample_background(cap)

  common.get_samples(cap,finger_pixels,background)

  cap.release()

if __name__=="__main__":
  prompted()