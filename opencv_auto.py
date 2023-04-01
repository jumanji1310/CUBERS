
# import the opencv library
import cv2
import numpy as np
from helper import *

colours = np.zeros((3,3,3))

code = ""


# Front - White || Up - Blue || Down - Green || Right - Red || Left - Orange || Back - Yellow

pixel = 0

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global code
        print(f'Pixel Coordinates {pixel}: {x}, {y}')
        colour = getPixelColour(img[y-1][x-1])
        print(colour)
        code += colour

# define a video capture object
vid = cv2.VideoCapture(0)

side = 1
face = ["Up", "Right", "Front", "Down", "Left", "Back"]

capture = True
if capture:
    while side != 7:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Adding square to video
        overlay = cv2.rectangle(frame, (220, 140), (420, 340), (0,0,255), 2)

        # Adding text for current side
        overlay = cv2.putText(overlay, f'Side {side} ({face[side-1]})', (320, 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        # Display the resulting frame
        cv2.imshow('frame', overlay)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            cv2.imwrite(f'frame_{side}.png', overlay)
            print("Image taken")
            side += 1

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if key & 0xFF == ord('q'):
            break


read = 1
offset = 33
coords = [[220 + offset, 140 + offset],[220 + 3*offset, 140 + offset],[220 + 5*offset, 140 + offset],
[220 + offset, 140 + 3*offset],[220 + 3*offset, 140 + 3*offset],[220 + 5*offset, 140 + 3*offset],
[220 + offset, 140 + 5*offset],[220 + 3*offset, 140 + 5*offset],[220 + 5*offset, 140 + 5*offset]]

while read != 7:
    pixel = 0
    img = cv2.imread(f'frame_{read}.png')
    print(f"Side {read}")
    for coord in coords:
        # cv2.circle(img, (coord[0]-1, coord[1]-1), 5, (0,0,255),-1)
        # colour = getPixelColour(img[coord[1]-1][coord[0]-1])
        colour, result = distance_Metric(img[coord[1]-1][coord[0]-1])
        print(colour, result, img[coord[1]-1][coord[0]-1], min(result))
        code += colour[0]
    cv2.imshow("image",img)
    cv2.waitKey(0)
    read += 1

print(code)
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()