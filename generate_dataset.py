import os
import random

domain_images_path = './domain_data/drone_images'
domain_labels_path = './domain_data/labels'
domain_sky_path = './domain_data/sky_backgrounds'

data_pair = []


image_files = os.listdir(domain_images_path)
label_files = os.listdir(domain_labels_path)
sky_files = os.listdir(domain_sky_path)

for image_file in image_files:
    image_name, image_ext = os.path.splitext(image_file)
    label_file = image_name + '.txt'
    if label_file in label_files:
        image_path = os.path.join(domain_images_path, image_file)
        label_path = os.path.join(domain_labels_path, label_file)
        data_pair.append((image_path, label_path))


for generated_data in range(random.randin(1, 20)):
