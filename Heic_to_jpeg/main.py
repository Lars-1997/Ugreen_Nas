#####################################################
###                 Import Modules                ###
#####################################################
import os
from PIL import Image
from pillow_heif import register_heif_opener

######################################################
###               Set Variables                    ###
######################################################
delete_files = os.environ["DELETE_HEIC_FILES"]


######################################################
###               Create Functions                 ###
######################################################
def create_list_of_heic_files(source_directory):
    """
    Creates a list of all .heic files in the specified source directory and its subdirectories.
    Args:
        source_directory (str): The path to the source directory.
    Returns:
        list: A list of file paths for all .heic files found.
    """
    heic_files = []
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith(".heic"):
                heic_files.append(os.path.join(root, file))
    return heic_files


def convert_heic_to_jpeg(heic_file_path, output_directory):
    """
    Converts a .heic file to .jpeg format and saves it in the specified output directory.
    Args:
        heic_file_path (str): The path to the .heic file.
        output_directory (str): The directory where the converted .jpeg file will be saved.
    Returns:
        str: The path to the converted .jpeg file.
    """
    register_heif_opener()
    image = Image.open(heic_file_path)
    jpeg_file_name = os.path.splitext(os.path.basename(heic_file_path))[0] + ".jpeg"
    original_file_path = os.path.dirname(heic_file_path)
    jpeg_file_path = os.path.join(original_file_path, jpeg_file_name)
    image.convert("RGB").save(jpeg_file_path, "JPEG")
    return jpeg_file_path


def remove_unwanted_heic_files_from_directory(source_directory):
    """
    Removes unwanted .heic files from the specified source directory.
    Args:
        source_directory (str): The path to the source directory.
        unwanted_file_names (list): A list of unwanted .heic file names to be removed.
    """
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith(".heic"):
                os.remove(os.path.join(root, file))


######################################################
###                 Start Skript                   ###
######################################################
source = "/app/images_source"
heic_files = create_list_of_heic_files(source)
for file in heic_files:
    convert_heic_to_jpeg(file, source)
    print(f"Converted: {file} to JPEG format.")

if delete_files.lower() == "true":
    remove_unwanted_heic_files_from_directory(source)
print(os.listdir(source))
