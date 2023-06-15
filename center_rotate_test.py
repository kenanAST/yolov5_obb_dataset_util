import math
import matplotlib.pyplot as plt


def rotate_point(point, pivot, angle):
    """
    Rotate a point around a pivot point by a given angle.
    """
    px, py = point
    cx, cy = pivot

    # Convert the angle to radians
    angle_rad = math.radians(-angle)  # Change the sign of the angle

    # Compute the coordinates after rotation
    qx = cx + math.cos(angle_rad) * (px - cx) - math.sin(angle_rad) * (py - cy)
    qy = cy + math.sin(angle_rad) * (px - cx) + math.cos(angle_rad) * (py - cy)

    return qx, qy


# Original point coordinates
point = (512, 384)
# Pivot point coordinates
pivot = (896, 693)
# Rotation angle in degrees
angle = 90


# Original point coordinates
point = (512, 384)
# Pivot point coordinates
pivot = (896, 693)
# Rotation angle in degrees
angle = 90

# Compute the new point coordinates after rotation
new_point = rotate_point(point, pivot, angle)
print(f"Point: {point}")
print(f"NewPoint: {new_point}")

# Plotting the original and rotated points
plt.plot([point[0]], [point[1]], 'bo', label='Original Point')
plt.plot([new_point[0]], [new_point[1]], 'ro', label='Rotated Point')

# Plotting the pivot point
plt.plot([pivot[0]], [pivot[1]], 'go', label='Pivot Point')

# Drawing lines to connect the points
plt.plot([pivot[0], point[0]], [pivot[1], point[1]],
         'b--', label='Original Vector')
plt.plot([pivot[0], new_point[0]], [pivot[1], new_point[1]],
         'r--', label='Rotated Vector')

# Adding labels and grid
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)

# Setting axis limits
plt.xlim(-2000, 2000)
plt.ylim(-2000, 2000)

# Adding legend
plt.legend()

# Display the plot
plt.show()
