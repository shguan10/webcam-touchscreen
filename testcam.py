import cv2 

import numpy as np
MAXCOLS = 1280
MAXROWS = 720
RADIUS = 10
def generate_random_circle():
  return np.random.rand(2) * [MAXROWS,MAXCOLS]

def main():
  cap = cv2.VideoCapture(0)

  #To set the resolution
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAXROWS)

  circle_position = generate_random_circle()

  while True:
    _, frame = cap.read()

    draw_circle(frame,circle_position)

    cv2.imshow("Live Feed",frame)

    if cv2.waitKey(1) == ord(" "):
      save_frame(frame,circle_position)
      circle_position = generate_random_circle()

    if cv2.waitKey(1) == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()

if __name__=="__main__":
  main()