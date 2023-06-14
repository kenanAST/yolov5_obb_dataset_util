import cv2
import numpy as np


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
center = np.array([150, 150], dtype=np.float32)

# Angle of rotation in degrees
angle = 45

# Rotate the points
rotated_points = rotate_points(points, center, 0 + 5)
