# Ugreen_Nas

This script plans to automatically move the interesting pictures saved by the "Backup and Sync" App to a common Shared Folder, where all the users, at the moment two, can see each other's pictures. 
To do that, the following steps are planned.

Plan:
- Create Python File: :white_check_mark:
  - Create a List of all Files in the first Folder :white_check_mark:
  - Create a List of all Files in the second Folder :white_check_mark:
  - Create a List of all Files in the third Folder :white_check_mark:
  - Compare List one and three, and List two and three :white_check_mark:
  - Remove objects that are in List three :white_check_mark:
  - Compare the remaining objects in List one and two :white_check_mark:
  - Move all the remaining items on List one and two to the position of List three :white_check_mark:

- Create a Docker build of that Skript 
  - Create a Dockerfile that works and moves images from one folder to another :white_check_mark:
  - Create a setup file so that the variables do not have to be handled manually
- Figure out how to schedule the Docker Build to run every day, even when the NAS is restarted every day ✅

Problems:
- Python File
  - The "Backup and Sync" App moves the data to a different Folder structure
    - Find out how much information one could get from the metadata of the saved files
    - Find out if one could find out which type of phone is used and map how that phone safes images

Possible Improvements:
- Python File
  - Add the option to ignore specific folders for sensitive images :white_check_mark:
  - Make that lists one and two are compared to list three simultaneously (Not sure how big the impact is)
