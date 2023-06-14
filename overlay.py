import cv2
import os


def overlay_images(folder_path, output_path, background_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            images.append(image)

    if len(images) == 0:
        print("No images found in the folder.")
        return

    background = cv2.imread(background_path)
    if background is None:
        print("Background image not found.")
        return

    overlay = background
    for image in images:
        overlay = cv2.addWeighted(overlay, 1, image, 1, 0)

    cv2.imwrite(output_path, overlay)
    print("Overlay image saved at:", output_path)


folder_path = "./raw_data/drone_images"
output_path = "./generated_dataset/1.png"
overlay_images(folder_path, output_path)
