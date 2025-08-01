from functions.os_operations import *
from functions.list_operations import *

# Set the paths to the directories you want to read
source_1 = "/app/skripts/image_folders/images_source_1"
source_2 = "/app/skripts/image_folders/images_source_2"
target = "/app/skripts/image_folders/images_target"

# Read all files from the specified directory
files_1 = read_all_files(source_1)
files_2 = read_all_files(source_2)
files_3 = read_all_files(target)

# Create a of file names without folder paths
files_1_without_foldernames = remove_folders(files_1)
files_2_without_foldernames = remove_folders(files_2)
files_3_without_foldernames = remove_folders(files_3)

# Remove files from source_1 that are present in source_2
files_1_cleaned = remove_existing_files(files_1_without_foldernames, files_2_without_foldernames)
# Remove files from source_1 and source_2 that are present in target
files_1_cleaned = remove_existing_files(files_1_cleaned, files_3_without_foldernames)
files_2_cleaned = remove_existing_files(files_2_without_foldernames, files_3_without_foldernames)

# Remove the removed files from the original lists
files_1 = remove_existing_files_from_list_with_folders(files_1, files_1_cleaned)
files_2 = remove_existing_files_from_list_with_folders(files_2, files_2_cleaned)

# Copy files from source_1 to target
copy_files(files_1, source_1, target)
copy_files(files_2, source_2, target)

# Check Results
files_3 = read_all_files(target)

