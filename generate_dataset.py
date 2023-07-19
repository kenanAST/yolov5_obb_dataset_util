import os
import random
import numpy as np
from domain import draw_lines, draw_anchor_points, draw_rectangle, rotate_points, reposition_center, check_rectangle_bounds, check_rectangle_collision, get_center
from overlay import overlay_images
import cv2
import imgname_generate

number_of_images = 10

domain_images_path = './domain_data/images'
domain_labels_path = './domain_data/labelTxt'
domain_sky_path = './domain_data/sky_backgrounds'

data_pair = []

if (not os.path.exists('./generated_dataset')):
    os.makedirs('./generated_dataset/display_labelled')
    os.makedirs('./generated_dataset/images')
    os.makedirs('./generated_dataset/labelTxt')


image_files = os.listdir(domain_images_path)
label_files = os.listdir(domain_labels_path)
sky_files = [file for file in os.listdir(
    domain_sky_path) if file.lower().endswith(('.png', '.jpg'))]


for image_file in image_files:
    image_name, image_ext = os.path.splitext(image_file)
    label_file = image_name + '.txt'
    if label_file in label_files:
        image_path = os.path.join(domain_images_path, image_file)
        label_path = os.path.join(domain_labels_path, label_file)

        with open(label_path, 'r') as file:
            label_data = file.read().strip().split(' ')
            label_data = np.array(
                label_data[:8], dtype=np.float32).reshape((-1, 2))

        data_pair.append((image_path, label_data))


for data in range(number_of_images):
    generated_images = []
    generated_labels = []
    generated_rotations = []
    generated_anchor_points = []
    generated_repositions = []
    generated_new_centers = []
    sky_file = random.choice(sky_files)

    number_of_objects = random.randint(1, 20)

    checker = None
    checker_2 = None
    checker_3 = None

    for generated_data in range(number_of_objects):

        # Generate rotation and position and check if there is collision or within bounds
        while True:
            raw_data = random.randint(0, len(data_pair) - 1)
            image, label = data_pair[raw_data]
            checker = label
            original_center_x, original_center_y = get_center(label)
            generated_pos_x = random.randint(0, 1024)
            generated_pos_y = random.randint(0, 768)
            generated_position = (generated_pos_x, generated_pos_y)
            generated_angle = random.randint(0, 360)

            # original_center_x, original_center_y = get_center(label)
            # generated_pos_x = 700
            # generated_pos_y = 400
            # generated_position = (generated_pos_x, generated_pos_y)
            # generated_angle = 90

            difference_center_x, difference_center_y = difference_center = (
                generated_pos_x - original_center_x, generated_pos_y - original_center_y)

            new_image_center = (0 + difference_center_x,
                                0 + difference_center_y)

            # print(f"New Image Center: {new_image_center}")
            # print(f"New BBox Center: {(generated_position)}")

            # print(f"Old Image Center: {get_center(label)}")
            # print(f"Old BBox Center: {(0,0)}")

            difference_new_image = (
                new_image_center[0] - 0, new_image_center[1] - 0)

            difference_new_bbox = (
                generated_pos_x - original_center_x, generated_pos_y - original_center_y)

            # Reposition
            repositioned_points = reposition_center(label, generated_position)

            center = get_center(repositioned_points)

            # Rotation
            rotated_points = rotate_points(
                repositioned_points, center, generated_angle)

            # Check if the points are within the bounds
            if check_rectangle_bounds(rotated_points, (1024, 768)) and (not check_rectangle_collision(rotated_points, generated_labels)):
                generated_images.append(image)
                generated_labels.append(rotated_points)
                generated_rotations.append(-generated_angle)
                generated_anchor_points.append(get_center(label))
                generated_repositions.append(difference_new_bbox)
                generated_new_centers.append(center)
                break

    sky_path = f'./domain_data/sky_backgrounds/{sky_file}'
    save_image_path = f'./generated_dataset/images/uav{"{:04d}".format(data)}.png'
    save_labels_path = f'./generated_dataset/labelTxt'

    overlay_images(generated_images, sky_path,
                   save_image_path, generated_rotations, generated_anchor_points, generated_repositions)

    # Create the directory if it doesn't exist
    os.makedirs(save_labels_path, exist_ok=True)

    text_check = ''
    label_filename = f'uav{"{:04d}".format(data)}.txt'
    label_filepath = os.path.join(save_labels_path, label_filename)
    with open(label_filepath, 'w') as file:
        # Generate the label or .txt file for each image
        for i, new_label in enumerate(generated_labels):
            for points in new_label:
                text_check += (f'{points[0]} {points[1]} ')
            text_check += ('uav 0\n')
        file.write(text_check)

    # Read the background image
    background_image = cv2.imread(save_image_path)

    # Resize the background image to match the desired dimensions
    background_image = cv2.resize(background_image, (1024, 768))

    # Create a blank image with the same dimensions as the background image
    image = np.zeros_like(background_image)

    # Overlay the background image on the blank image
    image = cv2.addWeighted(image, 1, background_image, 1, 0)

    # Draw the rotated rectangle
    for label in generated_labels:
        draw_rectangle(image, label.astype(np.int32))

    draw_anchor_points(image, generated_new_centers)
    draw_anchor_points(image, [(512, 384)])
    draw_lines(image, (512, 384), generated_new_centers)

    # Display the image
    # cv2.imshow('Anchor Points', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Save the image
    save_display_path = f'./generated_dataset/display_labelled/uav{"{:04d}".format(data)}.png'
    cv2.imwrite(save_display_path, image)

imgname_generate.write_sorted_filenames(
    './generated_dataset/images', './generated_dataset/imgnamefile.txt')
