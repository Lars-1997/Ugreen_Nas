from functions.os_operations import *
from functions.list_operations import *
import datetime
import time


##############################################################
###    Set the paths to the directories you want to read   ###
##############################################################
source_1 = "/app/skripts/image_folders/images_source_1"
source_2 = "/app/skripts/image_folders/images_source_2"
target = "/app/skripts/image_folders/images_target"

while True:
    now = datetime.datetime.now()
    if now.hour == 12 and now.minute == 0:
        ##############################################################
        ###       Read all files from the specified directory      ###
        ##############################################################
        # Files in the first source directory
        files_1 = read_all_files(source_1)

        # Files in the second source directory
        files_2 = read_all_files(source_2)

        # Files in the target directory
        files_3 = read_all_files(target)

        ##############################################################
        ###         Remove folders from the list of files          ###
        ##############################################################
        # Only neccessary in the foldes where the original files are stored
        # For the first source directory
        folders_to_remove_1 = read_all_folders_to_be_ignored(source_1)
        remove_unwanted_folders_from_list(files_1, folders_to_remove_1)

        # For the second source directory
        folders_to_remove_2 = read_all_folders_to_be_ignored(source_2)
        remove_unwanted_folders_from_list(files_2, folders_to_remove_2)

        ##############################################################
        ###       Create a of file names without folder paths      ###
        ##############################################################
        # For User and Device unrelated comparisons
        files_1_without_foldernames = remove_folders(files_1)
        files_2_without_foldernames = remove_folders(files_2)
        files_3_without_foldernames = remove_folders(files_3)

        ##############################################################
        ###         Remove the files, that are in duplicated,      ###
        ###             followed by already existing file          ###
        ##############################################################
        # Remove files from source_1 that are present in source_2
        files_1_cleaned = remove_existing_files(
            files_1_without_foldernames, files_2_without_foldernames
        )
        # Remove files from source_1 and source_2 that are present in target
        files_1_cleaned = remove_existing_files(
            files_1_cleaned, files_3_without_foldernames
        )
        files_2_cleaned = remove_existing_files(
            files_2_without_foldernames, files_3_without_foldernames
        )

        ##############################################################
        ###       Remove the compared files form the OG List       ###
        ##############################################################
        # Remove the removed files from the original lists
        files_1 = remove_existing_files_from_list_with_folders(files_1, files_1_cleaned)
        files_2 = remove_existing_files_from_list_with_folders(files_2, files_2_cleaned)

        ##############################################################
        ###           Finally move the files to the target         ###
        ##############################################################
        # Copy files from source_1 to target
        copy_files(files_1, source_1, target)
        copy_files(files_2, source_2, target)

        # Check Results
        files_3 = read_all_files(target)

        time.sleep(60)
    elif now.minute % 15 == 0:
        print(f"Service Check: It is {now}")
        time.sleep(60-now.second)
    else:
        time.sleep(60)
