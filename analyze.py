import cv2
import numpy as np
import pdb
import os, sys
import common

def main(fname):
  frame = common.open_image(fname)
  background = common.open_image(common.BACKGROUND_FNAME)
  frame = common.background_filter(frame,background)
  frame = common.fuzzy_mask(frame)
  cv2.imwrite("dankfiltered/"+fname,frame)


if __name__=="__main__":
  for file in os.listdir("data"):
    file = "/".join(["data",file])
    print(file)
    main(file)