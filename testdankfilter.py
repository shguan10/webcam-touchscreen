import cv2
import numpy as np
import pdb
import os, sys
import common


def main():
  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, common.MAXCOLS)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, common.MAXROWS)

  finger_pixels = common.sample_finger(cap)

  background = common.sample_background(cap)

  common.filter(cap,finger_pixels,background)

  cap.release()

if __name__=="__main__":
  main()