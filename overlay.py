from PIL import Image, ImageDraw
import os


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

    # Overlay each image onto the merged image
    for image in images:
        merged_image.paste(image, (0, 0), mask=image)

    # Save the merged image
    merged_image.save(output_path)
    print(
        f"Overlay image with background and individual rotations saved as {output_path}")


folder_path = "./raw_data/drone_images"
background_path = "./raw_data/sky_backgrounds/anime2.png"
output_path = "./generated_dataset/1.png"
rotations = [10, 90, 0, 0, 0]  # Rotation angles for each image in degrees
anchor_points = [
    (896, 693),  # Anchor point for the first image
    (896, 539),  # Anchor point for the second image
    (896, 539),  # Anchor point for the third image
    (640, 77),   # Anchor point for the fourth image
    (896, 77)    # Anchor point for the fifth image
]

overlay_images(folder_path, background_path,
               output_path, rotations, anchor_points)
