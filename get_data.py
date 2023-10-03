import cv2

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


face_positions = []

# Read face_positions.data
with open('face_positions.data', 'r') as file:
    data = file.readlines()

for line in data:
    x, y = map(int, line.strip().split(','))
    face_positions.append((x, y))

# Initialize video capture
video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera, adjust if needed

# Initialize list for RGB values
rgb_values = []

cv2.namedWindow('Video Feed')

while len(rgb_values) < 48:
    ret, frame = video_capture.read()

    if not ret:
        break

    # Normalize the frame
    frame = normalise(frame)

    cv2.imshow('Video Feed', frame)

    # Check for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Check for 'C' key to capture RGB values
    if cv2.waitKey(1) & 0xFF == ord('c'):
        for x, y in face_positions:            
            b, g, r = frame[y, x]  # OpenCV uses BGR instead of RGB
            rgb_values.append((r, g, b))
            print(f'RGB value at ({x},{y}): R={r}, G={g}, B={b}')

# Save the RGB values to a .data file
colours = ['blue','red','white','green','orange','yellow']
face_count = 0
with open('detector/training.data', 'w') as file:
    for r, g, b in rgb_values:
        file.write(f'{r},{g},{b},{colours[face_count//8]}\n')
        face_count += 1
# Release resources
video_capture.release()
cv2.destroyAllWindows()
