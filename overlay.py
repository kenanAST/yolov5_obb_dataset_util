from PIL import Image
import os

# A 5x4 grid division of a (1024, 768) image.
anchor_points = [(102.4, 96),  (307.2, 96),  (512, 96),  (716.8, 96),  (921.6, 96),  (102.4, 288),  (307.2, 288),  (512, 288),  (716.8, 288),  (921.6, 288),
                 (102.4, 480),  (307.2, 480),  (512, 480),  (716.8, 480),  (921.6, 480),  (102.4, 672),  (307.2, 672),  (512, 672),  (716.8, 672),  (921.6, 672)]


def overlay_images(folder_path, background_path, output_path, rotations=None, anchor_points=None):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            print(filename)
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            images.append(image)

    if not images:
        print("No images found in the folder.")
        return

    # Determine the dimensions of the final image
    width = max(image.width for image in images)
    height = max(image.height for image in images)

    # Open the background image
    background = Image.open(background_path)
    background = background.resize((width, height))

    # Create a new image with the background
    merged_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    merged_image.paste(background, (0, 0))

    # Overlay each image onto the merged image with rotation
    for image, rotation, anchor_point in zip(images, rotations, anchor_points):
        rotated_image = image.rotate(
            rotation, expand=True, center=anchor_point)
        merged_image.paste(rotated_image, (0, 0), mask=rotated_image)

    # Save the merged image
    merged_image.save(output_path)
    print(
        f"Overlay image with background and individual rotations saved as {output_path}")

# Example usage:


folder_path = "./raw_data/drone_images"
background_path = "./raw_data/sky_backgrounds/anime2.png"
output_path = "./generated_dataset/1.png"
rotations = [0, 0, 0, 0, 0]  # Rotation angles for each image in degrees
anchor_points = [(0, 0), (0, 0), (0, 0)
                 ]  # Anchor points for each image

overlay_images(folder_path, background_path,
               output_path, rotations, anchor_points)
