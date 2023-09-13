import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

#Loading training data               
with open('./detector/training.data','r') as file:
    train_pixels = []
    train_labels = []
    for line in file:
        data = line.strip().split(',')
        train_pixels.append([int(data[0]),int(data[1]),int(data[2])])
        train_labels.append(data[3])

# convert to numpy array
train_pixels = np.array(train_pixels)
train_labels = np.array(train_labels)
# train the k-NN model
k = 3
model = KNeighborsClassifier(n_neighbors=k)
model.fit(train_pixels, train_labels)

def plot_model(pixel=None):
    # Close any existing figures
    plt.close('all')

    # Get the predictions from the KNeighborsClassifier model
    train_predictions = model.predict(train_pixels)

    # Create a 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract R, G, B values from train_pixels
    r = train_pixels[:,0]
    g = train_pixels[:,1]
    b = train_pixels[:,2]

    ax.scatter(r[train_predictions=='blue'],g[train_predictions=='blue'],b[train_predictions=='blue'], c='blue', label='blue')
    ax.scatter(r[train_predictions=='green'],g[train_predictions=='green'],b[train_predictions=='green'], c='green', label='green')
    ax.scatter(r[train_predictions=='red'],g[train_predictions=='red'],b[train_predictions=='red'], c='red', label='red')
    ax.scatter(r[train_predictions=='orange'],g[train_predictions=='orange'],b[train_predictions=='orange'], c='orange', label='orange')
    ax.scatter(r[train_predictions=='yellow'],g[train_predictions=='yellow'],b[train_predictions=='yellow'], c='yellow', label='yellow')
    ax.scatter(r[train_predictions=='white'],g[train_predictions=='white'],b[train_predictions=='white'], c='black', label='white')

    # Add clicked pixel
    if pixel is not None:
        ax.scatter(pixel[0][0],pixel[0][1],pixel[0][2],c='purple',s=200)

    # Customize the plot
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title('KNeighborsClassifier Clusters in 3D')
    ax.legend()

    # Show the plot
    plt.show()

# plot_model()

#convert colour string to Singmaster notation
def stringToSingmaster(string):
    turn_string = ''
    string_list = string.strip().split()
    for colour in string_list:
        if colour == 'white':
            turn_string += 'F'
        elif colour == 'orange':
            turn_string += 'L'
        elif colour == 'blue':
            turn_string += 'U'
        elif colour == 'green':
            turn_string += 'D'
        elif colour == 'red':
            turn_string += 'R'
        elif colour == 'yellow':
            turn_string += 'B'
    print(turn_string)
    return turn_string