import os
import random
import numpy as np
from domain import rotate_points, reposition_center, check_rectangle_bounds, check_rectangle_collision


number_of_images = 10

domain_images_path = './domain_data/drone_images'
domain_labels_path = './domain_data/labels'
domain_sky_path = './domain_data/sky_backgrounds'

data_pair = []


image_files = os.listdir(domain_images_path)
label_files = os.listdir(domain_labels_path)
sky_files = [file for file in os.listdir(
    domain_sky_path) if file.lower().endswith('.png')]

for image_file in image_files:
    image_name, image_ext = os.path.splitext(image_file)
    label_file = image_name + '.txt'
    if label_file in label_files:
        image_path = os.path.join(domain_images_path, image_file)
        label_path = os.path.join(domain_labels_path, label_file)

        with open(label_path, 'r') as file:
            label_data = file.read().strip().split(', ')
            label_data = np.array(
                label_data[:8], dtype=np.float32).reshape((-1, 2))

        data_pair.append((image_path, label_data))


for i in range(number_of_images):
    generated_images = []
    generated_labels = []
    anchor_points = []

    for generated_data in range(random.randint(1, 20)):
        sky_file = random.choice(sky_files)

        while True:
            raw_data = random.randint(0, len(data_pair) - 1)
            image, label = data_pair[raw_data]
            generated_pos_x = random.randint(0, 1024)
            generated_pos_y = random.randint(0, 768)
            generated_position = (generated_pos_x, generated_pos_y)
            generated_angle = random.randint(0, 360)

            # Reposition
            repositioned_points = reposition_center(label, generated_position)

            # Rotation
            rotated_points = rotate_points(
                repositioned_points, generated_angle)

            # Check if the points are within the bounds
            if check_rectangle_bounds(rotated_points, (1024, 768) and check_rectangle_collision(rotated_points, generated_labels)):
                generated_images.append(image)
                generated_labels.append(rotated_points)
                break
