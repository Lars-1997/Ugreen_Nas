#####################################################
###                 Import Modules                ###
#####################################################
import os
from PIL import Image

#####################################################
###                 Set Variables                 ###
#####################################################
file_path = "/app/images_source"
image_quality = int(os.environ["IMAGE_QUALITY"]) if "IMAGE_QUALITY" in os.environ and int(os.environ["IMAGE_QUALITY"]) <= 100 else 85

#####################################################
###                Create Functions               ###
#####################################################

def create_list_of_all_images(source_directory):
    """
    Creates a list of all .jpg files in the specified source directory and its subdirectories.
    Args:
        source_directory (str): The path to the source directory.
    Returns:
        list: A list of file paths for all .jpg files found.
    """
    images = []
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                images.append(os.path.join(root, file))
    return images

def compress_image(input_path, output_path, quality):
    """
    Compresses a .jpg image to the specified quality.
    Args:
        image_path (str): The path to the image file.
        quality (int): The quality level for compression (1-100).
    """
    with Image.open(input_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output_path, "JPEG", quality=quality)




images_path = create_list_of_all_images(file_path)
destination_folder = os.path.join(file_path, "compressed_images")
os.makedirs(destination_folder, exist_ok=True)
for image in images_path:
    image_name = os.path.basename(image)
    output_image_path = os.path.join(destination_folder, image_name)
    compress_image(image, output_image_path, quality=image_quality)
images = create_list_of_all_images(destination_folder)
print(images)