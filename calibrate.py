import cv2

face_pos = []
face_count = 0

# Define a callback function
def get_pixel_location(event, x, y, flags, param):
    global face_count, current_click
    if event == cv2.EVENT_LBUTTONDOWN:
        # Scale down the coordinates
        x = int(x // 2)
        y = int(y // 2)
        face_count += 1
        print(f'Pixel location {face_count} - x: {x}, y: {y} added')
        face_pos.append((x,y,face_count))

# Open a video file or capture from a camera
video_capture = cv2.VideoCapture(0)  # Replace with your video file

# Create a window and set the callback function
cv2.namedWindow('Video Frame')
cv2.setMouseCallback('Video Frame', get_pixel_location)


face_names = ['Up','Right','Front','Down','Left','Back']

while face_count != 48:
    ret, frame = video_capture.read()

    if not ret:
        break

    # Display the frame
    frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    cv2.imshow('Video Frame', frame)

    # Display text on the middle left
    image = cv2.putText(frame, face_names[face_count//8], (600, 2*30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    for point in face_pos:
        cv2.circle(image, (2*point[0],2*point[1]), 3, (0,0,255),1)
        cv2.putText(image, str(point[2]), (2*point[0],2*point[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('Video Frame', image)

    key = cv2.waitKey(1) & 0xFF
    # Check for 'q' key to exit
    if  key == ord('q'):
        break
    elif key == ord('r'):  # Reset if 'r' is pressed
        face_pos = []
        face_count = 0
       
with open('face_positions.data', 'w') as file:
    for pos in face_pos:
        file.write(f'{pos[0]},{pos[1]}\n')
print('Data saved to face_positions.data')

print(face_pos)
# Release resources
video_capture.release()
cv2.destroyAllWindows()
