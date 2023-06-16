import cv2
import numpy as np
import math


def draw_lines(image, base_point, points):
    """
    Draw lines between a base point and every point in an array on the image.
    """
    for point in points:
        cv2.line(image, tuple(base_point), tuple(point), (0, 0, 255), 2)


def draw_rectangle(image, points):
    # Draw a rectangle on the image given the 4 points
    for i in range(4):
        cv2.line(image, points[i], points[(i+1) % 4], (0, 0, 255), 2)


def rotated_image_center(point, pivot, angle):
    """
    Rotate a point around a pivot point by a given angle.
    """
    px, py = point
    cx, cy = pivot

    # Convert the angle to radians
    angle_rad = math.radians(angle)

    # Compute the coordinates after rotation
    qx = cx + math.cos(angle_rad) * (px - cx) - math.sin(angle_rad) * (py - cy)
    qy = cy + math.sin(angle_rad) * (px - cx) + math.cos(angle_rad) * (py - cy)

    return qx, qy


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


def scale_points(points, scale):
    # Create a scaling matrix
    scaling_matrix = np.array([[scale, 0], [0, scale]])

    # Apply the scaling matrix to the points
    scaled_points = np.dot(scaling_matrix, points.T).T

    return scaled_points


def get_center(points):
    """
    Calculate the center point of four given points.
    """
    x = sum(point[0] for point in points) / 4
    y = sum(point[1] for point in points) / 4
    return int(x), int(y)


def reposition_center(points, new_center):
    # Calculate the current center of the points
    current_center = np.mean(points, axis=0)

    # Calculate the translation vector to move the points to the new center
    translation_vector = new_center - current_center

    # Translate the points to the new center
    translated_points = points + translation_vector

    return translated_points


def check_rectangle_bounds(rectangle, image_size):
    """
    Check if a rectangle is within the bounds of the image.
    """
    x_points = [point[0] for point in rectangle]
    y_points = [point[1] for point in rectangle]
    min_x = min(x_points)
    max_x = max(x_points)
    min_y = min(y_points)
    max_y = max(y_points)

    image_width, image_height = image_size

    if min_x < 0 or min_y < 0 or max_x > image_width or max_y > image_height:
        return False

    return True


def check_rectangle_collision(rectangle, rectangle_array):
    for other_rectangle in rectangle_array:
        x1_min = np.min(rectangle[:, 0])
        y1_min = np.min(rectangle[:, 1])
        x1_max = np.max(rectangle[:, 0])
        y1_max = np.max(rectangle[:, 1])

        x2_min = np.min(other_rectangle[:, 0])
        y2_min = np.min(other_rectangle[:, 1])
        x2_max = np.max(other_rectangle[:, 0])
        y2_max = np.max(other_rectangle[:, 1])

        if (x1_max < x2_min or x2_max < x1_min or
                y1_max < y2_min or y2_max < y1_min):
            # No collision, check the next rectangle
            continue

        # Collision detected
        return True

    # No collision with any rectangle in the array
    return False


def draw_anchor_points(image, anchor_points):
    for i, point in enumerate(anchor_points):
        cv2.circle(image, tuple(point), 5, (0, 255, 0), -1)
        cv2.putText(image, f"({point[0]}, {point[1]})", (point[0] + 10, point[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)


# # Original points
# points = np.array([[100, 100], [200, 100], [200, 200],
#                   [100, 200]], dtype=np.float32)

# # Center of rotation (assumed to be the center of the image)
# center = np.array([340, 340], dtype=np.float32)

# # Angle of rotation in degrees
# angle = 45

# # Rotate the points
# rotated_points = rotate_points(points, center, angle)
# reposition_points = reposition_center(
#     rotated_points, np.array([974, 384], dtype=np.float32))

# print(check_rectangle_bounds(reposition_points, (1024, 768)))


# Read the background image
# background_image = cv2.imread('uav0050.jpg')

# # Resize the background image to match the desired dimensions
# background_image = cv2.resize(background_image, (1024, 768))

# # Create a blank image with the same dimensions as the background image
# image = np.zeros_like(background_image)

# # Overlay the background image on the blank image
# image = cv2.addWeighted(image, 1, background_image, 1, 0)


# # Draw the rotated rectangle
# draw_rectangle(image, reposition_points.astype(np.int32))


# # Display the image
# cv2.imshow('Anchor Points', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
