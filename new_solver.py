
# import the opencv library
import cv2
import numpy as np
from helper import *
import detector.predict as predictor
import detector.train as trainer
import twophase.solver as sv

# trainer.train_Images()

cubestring = predictor.predict_Colour('images/Set2')

print(cubestring)

print(sv.solve(cubestring,19,0.1))