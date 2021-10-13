# webcam-touchscreen
Turn your webcam into a touchscreen driver for your laptop with a compact mirror and computer vision!

## Ideas to make this happen
1. Make a dataset of your finger touching different spots on your screen and use good ol' machine learning to predict what pixel it's pointing at.
2. Use geometry to directly figure out what pixel you're pointing at.
  * How do we figure out where your finger makes contact with the screen?
  * We could do something really dank and just have the user trace a moving dot accross the screen so we get samples for how their hand looks when tracing, then use a basic similarity algorithm to choose the most similar hand position after this initial synch.
  * We need to make a data collection app first. Have the user touch X different spots on the screen, and record the pictures.
## Helpful links
Here are some links I found helpful while making this hack.
1. [this](https://dev.to/amarlearning/finger-detection-and-tracking-using-opencv-and-python-586m)
