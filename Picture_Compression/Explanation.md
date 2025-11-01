## Explanation

### What is the Problem?
When showing pictures on a TV or Xbox, the DLNA system reaches a limit at around 7mb per picture. And since modern devices take much larger pictures, another system or compressed images could be used.

### Tried Steps
- Run the Jellyfin Image on the NAS:
    - Worked with images bigger then 7mb :white_check_mark:
    - Problem, the loading time is to slow to display the Picture :x:
    - The time for an image change could not be found :x:
- Run the UniversalMediaServer Image on the NAS:
    - Also problems with images bigger the a specific size :x:
    - Harder to use than the DLNA App on the NAS.
- Create a skript, that runs in a Container and compresses the images in the DLNA Folder
    - Should include more images :white_check_mark:
    - Does lower quality and removes images with lots of action