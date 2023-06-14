import cv2
import numpy as np


# A 5x4 grid division of a (1024, 768) image.
anchor_points = [
    (102.4, 96), (307.2, 96), (512, 96), (716.8, 96), (921.6, 96),
    (102.4, 288), (307.2, 288), (512, 288), (716.8, 288), (921.6, 288),
    (102.4, 480), (307.2, 480), (512, 480), (716.8, 480), (921.6, 480),
    (102.4, 672), (307.2, 672), (512, 672), (716.8, 672), (921.6, 672)
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

# Create a blank image
image = np.zeros((680, 680, 3), dtype=np.uint8)

# Convert the rotated points to integers
rotated_points = np.int32(rotated_points)


center_point = (340, 340)
cv2.circle(image, center_point, radius=20, color=(255, 0, 0), thickness=-1)

# Connect the points to form a rectangle
cv2.polylines(image, [rotated_points], isClosed=True,
              color=(0, 0, 255), thickness=2)

# Display the image
cv2.imshow('Rectangle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
