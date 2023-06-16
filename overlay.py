from PIL import Image, ImageDraw
import os


def overlay_images(folder_path, background_path, output_path, rotations=None, anchor_points=None, repositions=None):
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

    center = (int(width / 2), int(height / 2))

    # Open the background image
    background = Image.open(background_path)
    background = background.resize((width, height))

    # Create a new image with the background
    merged_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    merged_image.paste(background, (0, 0))

    # Overlay each image onto the merged image with rotation, anchor point, and reposition
    for image, rotation, anchor, reposition in zip(images, rotations, anchor_points, repositions):
        rotated_image = image.rotate(rotation, center=anchor)

        # Calculate the new anchor point after repositioning
        new_anchor = (anchor[0] + reposition[0], anchor[1] + reposition[1])

        # Calculate the new position to paste the rotated image
        paste_position = (new_anchor[0] - int(rotated_image.width / 2),
                          new_anchor[1] - int(rotated_image.height / 2))

        merged_image.paste(rotated_image, paste_position, mask=rotated_image)

    # Save the merged image
    merged_image.save(output_path)
    print(
        f"Overlay image with background, rotations, and repositions saved as {output_path}")


folder_path = "./raw_data/drone_images"
background_path = "./raw_data/sky_backgrounds/coordinates.png"
output_path = "./generated_dataset/1.png"
# Rotation angles for each image in degrees
rotations = [90, 180, 45, 270, 360]

anchor_points = [
    (896, 693),
    (896, 539),
    (896, 539),
    (640, 77),
    (896, 77)
]

repositions = [
    (50, 0),
    (-50, 0),
    (0, 50),
    (0, -50),
    (100, 100)
]

overlay_images(folder_path, background_path, output_path,
               rotations, anchor_points, repositions)
