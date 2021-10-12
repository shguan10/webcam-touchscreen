# webcam-touchscreen
Turn your webcam into a touchscreen driver for your laptop with a compact mirror and computer vision!

## Ideas to make this happen
1. Make a dataset of your finger touching different spots on your screen and use good ol' machine learning to predict what pixel it's pointing at.
2. Use geometry to directly figure out what pixel you're pointing at.
  * How do we figure out where your finger makes contact with the screen?
  * We could do something really dank and just have the user trace a moving dot accross the screen so we get samples for how their hand looks when tracing, then use a basic similarity algorithm to choose the most similar hand position after this initial synch.
