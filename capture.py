import cv2
import numpy as np

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
            cv2.imwrite(f'images/capture/frame_{side}.png', overlay)
            print("Image taken")
            side += 1

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if key & 0xFF == ord('q'):
            break