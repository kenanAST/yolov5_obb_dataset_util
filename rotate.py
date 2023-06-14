import cv2
import numpy as np

# A 4x5 grid division of a (1024, 768) image.
anchor_points = [
    [(128, 77), (384, 77), (640, 77), (896, 77)],
    [(128, 231), (384, 231), (640, 231), (896, 231)],
    [(128, 385), (384, 385), (640, 385), (896, 385)],
    [(128, 539), (384, 539), (640, 539), (896, 539)],
    [(128, 693), (384, 693), (640, 693), (896, 693)],
]


def rotate_points(points, center, angle):
    # Convert the angle to radians
    theta = np.radians(angle)

    # Create a rotation matrix
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])

    # Translate the points to the origin
    translated_points = points - center

    # Apply the rotation matrix to the translated points
    rotated_points = np.dot(rotation_matrix, translated_points.T).T

    # Translate the points back to their original position
    rotated_points += center

    return rotated_points


# Original points
points = np.array([[100, 100], [200, 100], [200, 200],
                  [100, 200]], dtype=np.float32)

# Center of rotation (assumed to be the center of the image)
center = np.array([340, 340], dtype=np.float32)

# Angle of rotation in degrees
angle = 45

# Rotate the points
rotated_points = rotate_points(points, center, 45)

# Read the background image
background_image = cv2.imread('uav0050.jpg')

# Resize the background image to match the desired dimensions
background_image = cv2.resize(background_image, (1024, 768))

# Create a blank image with the same dimensions as the background image
image = np.zeros_like(background_image)

# Overlay the background image on the blank image
image = cv2.addWeighted(image, 1, background_image, 1, 0)

# Draw circles in the anchor points
for row in anchor_points:
    for point in row:
        x, y = point
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(image, f'({x}, {y})', (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

# Display the image
cv2.imshow('Anchor Points', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
