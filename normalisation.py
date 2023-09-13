import cv2
import numpy as np
import matplotlib.pyplot as plt
from capture import predict_image

def histogram_equalization(image):
    # Convert image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Apply histogram equalization to the L channel
    lab_image[:, :, 0] = cv2.equalizeHist(lab_image[:, :, 0])

    # Convert back to BGR color space
    equalized_image = cv2.cvtColor(lab_image, cv2.COLOR_Lab2BGR)

    return equalized_image

# Load the image
image = cv2.imread('images/capture/scan.png')

# Perform histogram equalization
normalized_image = histogram_equalization(image)

# Visualize the original and normalized images
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
new_img = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2RGB)
# cv2.imwrite('images/capture/scan.png',normalized_image)
plt.imshow(new_img)
plt.title('Normalized Image (Histogram Equalization)')
plt.axis('off')

predict_image(normalized_image)
plt.show()
