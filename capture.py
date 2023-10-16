import cv2
import numpy as np
import matplotlib.pyplot as plt
from detector.predict import *

def click_event(event, x, y, flags, param):
  
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # normalised_img = normalise(frame)

        # Converting to RGB
        RGB_frame = cv2.cvtColor(param, cv2.COLOR_BGR2RGB)
        
        print(x, ' ', y)

        pixel_colour = RGB_frame[y,x].reshape((-1, 3))

        print(pixel_colour)
        print(model.predict(pixel_colour))
        plot_model(pixel_colour)

with open('face_positions.data','r') as file:
    data = file.readlines()

# Process data and store in array as tuples
pairs = []
for line in data:
    x, y = map(int, line.strip().split(','))
    pairs.append((x, y))

up_face = pairs[:8]
right_face = pairs[8:16]
front_face = pairs[16:24]
down_face = pairs[24:32]
left_face = pairs[32:40]
back_face = pairs[40:48]

def normalise(image):
    # Convert the image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split the LAB image into L, A, and B channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Apply Adaptive Histogram Equalization to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_channel_equalized = clahe.apply(l_channel)

    # Merge the equalized L channel with the original A and B channels
    equalized_lab_image = cv2.merge([l_channel_equalized, a_channel, b_channel])

    # Convert the LAB image back to BGR color space
    normalized_image = cv2.cvtColor(equalized_lab_image, cv2.COLOR_LAB2BGR)

    return normalized_image

def predict_image(img):
    #plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    # Customize the plot
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title('KNeighborsClassifier Clusters in 3D')
    ax.legend()

    state_string = []
    RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    up_check = [['orange'],['red'],['blue'],['green'],['orange'],['white'],['orange'],['white']]
    right_check = [['red'],['green'],['yellow'],['yellow'],['green'],['red'],['red'],['green']]
    front_check = [['blue'],['blue'],['green'],['white'],['blue'],['green'],['yellow'],['yellow']]
    down_check = [['orange'],['orange'],['blue'],['red'],['white'],['red'],['blue'],['orange']]
    left_check = [['blue'],['yellow'],['red'],['red'],['orange'],['green'],['blue'],['white']]
    back_check = [['orange'],['green'],['white'],['white'],['yellow'],['yellow'],['white'],['yellow']]
    checks = [up_check,right_check,front_check,down_check,left_check,back_check]
    centres = ['blue','red','white','green','orange','yellow']

    total_score = 0
    for j, face in enumerate([up_face,right_face,front_face,down_face,left_face,back_face]):
        counter = 1
        score = 0
        for i, point in enumerate(face):
            # pixel_colour = RGB_img[point[1],point[0]].reshape((-1, 3))

            # Create a mask for the circle
            circle_mask = np.zeros(RGB_img.shape[:2], dtype=np.uint8)
            cv2.circle(circle_mask, point, 2, 255, -1)

            # Calculate the mean value of each channel within the circle
            r_mean = np.mean(RGB_img[:, :, 0][circle_mask == 255])
            g_mean = np.mean(RGB_img[:, :, 1][circle_mask == 255])
            b_mean = np.mean(RGB_img[:, :, 2][circle_mask == 255])

            pixel_colour = [[r_mean,g_mean,b_mean]]

            # predict pixel colour 
            prediction = model.predict(pixel_colour)

            print(prediction,end="")

            # adding to state string
            state_string.append(prediction[0])
            if counter == 4:
                state_string.append(centres[j])
            counter += 1

            score += 1 if prediction == checks[j][i] else 0

            #adding to plot
            ax.scatter(pixel_colour[0][0],pixel_colour[0][1],pixel_colour[0][2],c=prediction,label=prediction)

        total_score += score
        print(f'\n{checks[j]} {score}')
    print(f'Accuracy = {total_score/48*100:.2f}%')

    # Show the plot
    # plt.show()

    return stringToSingmaster(' '.join(state_string))


width = 640
height = 480
w_c = width//2
h_c = height//2
box_offset = 140
def run_video():
    # cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Frame", width, height)

    # define a video capture object
    vid = cv2.VideoCapture(0)
    while 1:
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Adding square to video
        frame = cv2.rectangle(frame, (w_c - box_offset, h_c - box_offset), (w_c + box_offset, h_c + box_offset), (0,0,255), 2)

        # # Adding cross from centre
        # cv2.line(frame,(w_c-400,h_c-400),(w_c+400,h_c+400),(0,0,255),2)
        # cv2.line(frame,(w_c-400,h_c+400),(w_c+400,h_c-400),(0,0,255),2)

        thickness = 1
        radius = 3
        draw = 1
        if draw:
            # Plotting all circles in each face
            for point in up_face:
                cv2.circle(frame, point, radius, (0,0,255),thickness)

            for point in down_face:
                cv2.circle(frame, point, radius, (0,255,0),thickness)

            for point in front_face:
                cv2.circle(frame, point, radius, (0,0,255),thickness)

            for point in back_face:
                cv2.circle(frame, point, radius, (0,0,255),thickness)

            for point in right_face:
                cv2.circle(frame, point, radius, (255,0,0),thickness)

            for point in left_face:
                cv2.circle(frame, point, radius, (255,0,0),thickness)

        # Normalise frame
        norm_frame = normalise(frame)
        # norm_frame = cv2.resize(norm_frame, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        cv2.imshow('Frame', norm_frame)

        cv2.setMouseCallback('Frame', click_event,param=norm_frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            cv2.imwrite(f'images/capture/scan.png', norm_frame)
            print("Image taken")

        if key & 0xFF == ord('w'):
            cv2.imwrite(f'images/capture/temp_scan.png', norm_frame)
            predict_image(norm_frame)


        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if key & 0xFF == ord('q'):
            break

# run_video()

# frame = cv2.imread('images/capture/original_dark.png')
# frame = cv2.imread('images/capture/normalised_dark.png')
# frame = cv2.imread('images/capture/original_bright.png')
# frame = cv2.imread('images/capture/normalised_bright.png')
# cv2.imshow('Frame', frame)
# predict_image(frame)
