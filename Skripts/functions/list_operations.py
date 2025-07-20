def remove_folders (list: list) -> list:
    """
    Removes folder paths from a list of file paths and returns only file names.
    Args:
        list (list): A list of file paths.
    Returns:
        list: A list of file names without folder paths.
    """
    file_names = []
    for file in list:
        file_name = file.split("\\")[-1]
        file_names = [] if 'file_names' not in locals() else file_names
        file_names.append(file_name)
    return file_names


def remove_existing_files(list_to_remove: list, list_to_check:list) -> list:
    """
    Removes files from list_to_remove that are present in list_to_check.
    Args:
        list_to_remove (list): List of file names to be checked if they exist in the list_to_check.
        list_to_check (list): List of file names to check against if they exist in the first list.
    Returns:
        list: A list of file names from list_to_remove that are not in list_to_check
    """
    return [file for file in list_to_remove if file not in list_to_check]

def remove_existing_files_from_list_with_folders(list_to_remove: list, list_with_movable_files: list) -> list:
    """
    Removes files from list_to_remove that are not present in list_with_movable_files, considering full paths.
    Args:
        list_to_remove (list): List of file paths to be checked if they exist in the list_with_movable_files.
        list_with_movable_files (list): List of file names to check against if they exist in the first list.
    Returns:
        list: A list of file paths from list_to_remove that do not have corresponding file names in list_with_movable_files.
    """
    return [file for file in list_to_remove if file.split("\\")[-1] in list_with_movable_files]