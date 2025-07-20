from functions.os_operations import *
from functions.list_operations import *

# Set the paths to the directories you want to read
path_1 = "J:\Bilder"
path_2 = "J:\Bilder_Test"
path_3 = "J:\Bilder_Ziel"

# Read all files from the specified directory
files_1 = read_all_files(path_1)
files_2 = read_all_files(path_2)
files_3 = read_all_files(path_3)

# Create a of file names without folder paths
files_1_without_foldernames = remove_folders(files_1)
files_2_without_foldernames = remove_folders(files_2)
files_3_without_foldernames = remove_folders(files_3)

# Remove files from path_1 that are present in path_2
files_1_cleaned = remove_existing_files(files_1_without_foldernames, files_2_without_foldernames)
# Remove files from path_1 and path_2 that are present in path_3
files_1_cleaned = remove_existing_files(files_1_cleaned, files_3_without_foldernames)
files_2_cleaned = remove_existing_files(files_2_without_foldernames, files_3_without_foldernames)

# Remove the removed files from the original lists
files_1 = remove_existing_files_from_list_with_folders(files_1, files_1_cleaned)
files_2 = remove_existing_files_from_list_with_folders(files_2, files_2_cleaned)

# Copy files from path_1 to path_3
copy_files(files_1, path_1, path_3)
copy_files(files_2, path_2, path_3)

# Check Results
files_3 = read_all_files(path_3)

