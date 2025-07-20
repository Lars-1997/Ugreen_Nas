import os
import shutil

def read_all_files(directory: str) -> list:
    """
    Reads a directory and returns a list of all files and files in subdirectories.
    This function uses `os.walk` to traverse the directory tree, collecting all file paths.
    Args:
        directory (str): The path to the directory to read.
    Returns:
        list: A list of file paths relative to the specified directory.
    """
    list_of_files = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            list_of_files.append(os.path.relpath(filepath, directory))
    
    return list_of_files

def copy_files(source_files: list, source_dir: str, target_dir: str) -> None:
    """
    Copies a list of files from a source directory to a target directory.
    For each file in `source_files`, this function constructs the full source and target paths,
    ensures that the target directory exists, and then copies the file using `shutil.copy2`
    (preserving metadata). If a source file does not exist, a message is printed.
    Args:
        source_files (list): List of filenames (relative to `source_dir`) to be copied.
        source_dir (str): Path to the directory containing the source files.
        target_dir (str): Path to the directory where files should be copied.
    Returns:
        None
    Side Effects:
        - Creates target directories as needed.
        - Prints status messages for each file copied or not found.
    Raises:
        OSError: If an error occurs during directory creation or file copying.
    """
    for file in source_files:
        source_path = os.path.join(source_dir, file)
        target_path = os.path.join(target_dir, file)
        
        # Ensure the target directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
            print(f"Copied: {source_path} to {target_path}")
        else:
            print(f"File not found: {source_path}")