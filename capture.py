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

# region Variable Definitions
width = 640
height = 480

w_c = width//2
h_c = height//2

w0 = 90
h0 = 90

#Main diagonal
diag_offset = 160
w1 = w_c - diag_offset
h1 = h_c - diag_offset

#Bottom two square next to diagonal
offset1 = 30
offset2 = 3
w2 = w1 + offset1
h2 = h1 - offset2

w3 = w1 - offset2
h3 = h1 + offset1

# Same corner as diagonal
w4 = w1 - 5
h4 = h1 - 25

w5 = w1 - 25
h5 = h1 - 5

#Bottom centres
w6 = w4 + offset1
h6 = h4 - offset2

w7 = w5 - offset2
h7 = h5 + offset1

#Edge verticals
v_offset = 21
w8 = w4 - v_offset
h8 = h4 - v_offset

w9 = w5 - v_offset
h9 = h5 - v_offset

w10 = w8 - v_offset
h10 = h8 - v_offset

w11 = w9 - v_offset
h11 = h9 - v_offset

#Top centres
w12 = w10 + offset1
h12 = h10 - offset2

w13 = w11 - offset2
h13 = h11 + offset1

widths = [w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13]
heights = [h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13]

down_points = [(w1,h1),(w2,h2),(w3,h3)]
box_offset = 140

# Defining points
up_face = [(w_c - w0,h_c - h0),(w_c,h_c - h0),(w_c + w0,h_c - h0),(w_c - w0,h_c),(w_c + w0,h_c),(w_c - w0,h_c + h0),(w_c,h_c + h0),(w_c + w0,h_c + h0)]
down_face = [(w1,height - h1),(width-w2,height-h2),(width-w1,height-h1),(w3,height-h3),(width-w3,h3),(w1,h1),(w2,h2),(width-w1,h1)]
front_face = [(w10,height-h10),(width-w12,height-h12),(width-w10,height-h10),(w8,height-h8),(width-w8,height-h8),(w4,height-h4),(width-w6,height-h6),(width-w4,height-h4)]
right_face = [(width-w11,height-h11),(width-w13,h13),(width-w11,h11),(width-w9,height-h9),(width-w9,h9),(width-w5,height-h5),(width-w7,h7),(width-w5,h5)]
left_face = [(w11,h11),(w13,height-h13),(w11,height-h11),(w9,h9),(w9,height-h9),(w5,h5),(w7,height-h7),(w5,height-h5)]
back_face = [(width-w10,h10),(w12,h12),(w10,h10),(width-w8,h8),(w8,h8),(width-w4,h4),(w6,h6),(w4,h4)]
# endregion

def normalise(image):
    # # Convert image to LAB color space
    # lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # # Apply histogram equalization to the L channel
    # lab_image[:, :, 0] = cv2.equalizeHist(lab_image[:, :, 0])

    # # Convert back to BGR color space
    # normalized_image = cv2.cvtColor(lab_image, cv2.COLOR_Lab2BGR)

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
    plt.show()

    return stringToSingmaster(' '.join(state_string))




def run_video():
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", width*2, height*2)

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


run_video()

# frame = cv2.imread('images/capture/original_dark.png')
# frame = cv2.imread('images/capture/normalised_dark.png')
# frame = cv2.imread('images/capture/original_bright.png')
# frame = cv2.imread('images/capture/normalised_bright.png')
# cv2.imshow('Frame', frame)
# predict_image(frame)
