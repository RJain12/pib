# -*- coding: utf-8 -*-

#install deepface
pip install deepface

##This prints the current working directory

import os

def current_path():
    print("current working directory before")
    print(os.getcwd())
    print()

##This changes the current working directory
os.chdir('C:/Users/wxknj/Dropbox/grant_disparities/Damian/photos')

#this checks the current working directory
current_path()

##After initially set up of deepface, this is the code to run each time open the file
import os
os.chdir('C:/Users/wxknj/Dropbox/grant_disparities/Damian/photos')
from deepface import DeepFace

##Analysis: replace with correct file name, run according to file type
demography = DeepFace.analyze("U7728105.jpg",actions = ['race'])
print(demography)

demography = DeepFace.analyze("A8902826.webp",actions = ['race'])
print(demography)

demography = DeepFace.analyze("W8825293.jpeg",actions = ['race'])
print(demography)

demography = DeepFace.analyze("A8807948.png",actions = ['race'])
print(demography)