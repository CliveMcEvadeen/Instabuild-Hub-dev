"""
Explorer Module

This module provides an advanced file exploration toolkit, allowing users to interact
with files and directories in the current working directory. It encompasses various
features for file analysis, content preview, filtering, downloading, and more.

Key Features:
- Explore and display information about the current directory.
- Retrieve detailed information about all files in the current directory.
- Search for files containing a specific keyword in their content.
- Get statistics on the count of different file types in the directory.
- Preview content of specific file types and read file content.
- Analyze text files for word count and unique word count.
- Rename, create, and delete files.
- Filter files based on their types.
- Download selected files to a specified destination.
- Extract files from an archive to a specified destination.
- Compare the content of two files.
- Perform a recursive listing of files and folders.
- Display information about file permissions and recent changes in the directory.
- Set and display user-specific preferences for directory information.

"""

import os
import pathlib
import shutil
import chardet
import magic
import hashlib
import zipfile
import tarfile
from typing import List

class Explorer:
    def __init__(self):
        # Initialize the file explorer with the current working directory
        self.current_directory = pathlib.Path(__file__).parent.resolve()

    def explore_directory(self):
        """
        Explore and display information about the current directory.
        """
        dir_info = {
            "name": self.current_directory.name,
            "path": str(self.current_directory),
            "created": self.current_directory.stat().st_ctime,
            "modified": self.current_directory.stat().st_mtime,
            # "items": [item.name for item in sorted(os.scandir(self.current_directory))],

        }
        print("Current Directory:")
        print(f"Name: {dir_info['name']}")
        print(f"Path: {dir_info['path']}")
        print(f"Created: {dir_info['created']}")
        print(f"Modified: {dir_info['modified']}")
        # print(f"items: {dir_info['items']}")
        print("-" * 40)

    def get_all_files(self, sort_by: str = "name", file_type: str = None) -> List[dict]:
        """
        Retrieve detailed information about all files in the current directory.
        """
        file_list = []
        for file_path in self.current_directory.iterdir():
            if file_path.is_file():
                if file_type is None or self.get_file_type(file_path).startswith(file_type):
                    file_info = self.get_file_info(file_path)
                    file_list.append(file_info)

        # Sort files based on the specified criteria
        file_list.sort(key=lambda x: x.get(sort_by, 0))
        return file_list
    
    def print_file_info(self, files_info: List[dict]):
        """
        Print information about files.
        """
        for file_info in files_info:
            print(f"Name: {file_info['name']}")
            print(f"Path: {file_info['path']}")
            print(f"Size: {file_info['size']} bytes")
            print(f"Type: {file_info['type']}")
            print(f"Created: {file_info['created']}")
            print(f"Modified: {file_info['modified']}")
            print("-" * 40)

    def get_file_info(self, file_path: pathlib.Path) -> dict:
        """
        Retrieve detailed information about a specific file.
        """
        file_info = {
            "name": file_path.name,
            "path": str(file_path),
            "size": file_path.stat().st_size,  # File size in bytes
            "type": self.get_file_type(file_path),
            "created": file_path.stat().st_ctime,  # Creation time
            "modified": file_path.stat().st_mtime,  # Last modification time
        }
        return file_info

    def get_file_type(self, file_path: pathlib.Path) -> str:
        """
        Determine the file type using the 'magic' library.
        """
        mime = magic.Magic()
        return mime.from_file(str(file_path))

    def search_files(self, keyword: str) -> List[dict]:
        """
        Search for files containing a specific keyword in their content.
        """
        matching_files = []
        for file_path in self.current_directory.iterdir():
            if file_path.is_file():
                try:
                    if keyword.lower() in file_path.read_text().lower():
                        file_info = self.get_file_info(file_path)
                        matching_files.append(file_info)
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
        return matching_files


    def get_file_type_statistics(self) -> dict:
        """
        Get statistics on the count of different file types in the directory.
        """
        file_type_statistics = {}
        for file_path in self.current_directory.iterdir():
            if file_path.is_file():
                file_type = self.get_file_type(file_path)
                file_type_statistics[file_type] = file_type_statistics.get(file_type, 0) + 1
        return file_type_statistics
        # print('-' * 40)

    def preview_file_content(self, file_path: pathlib.Path, num_lines: int = 5):
        """
        Display a preview of the content of specific file types.
        """
        # Ensure that the file exists before attempting to open it
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return

        # Check if the file type is supported for preview
        supported_file_types = ['.txt', '.py', '.md', '.json', '.env', '.md']
        if file_path.suffix.lower() not in supported_file_types:
            print(f"Cannot preview content of {file_path}. Unsupported file type.")
            return

        # Open the file and display the content preview
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                print(f"Content preview of {file_path}:")
                for _ in range(num_lines):
                    line = file.readline().strip()
                    print(line)
                print("-" * 40)
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            print("-" * 40)

    def read_file_content(self, file_path: pathlib.Path, num_lines: int = None) -> str:
        """
        Read and return the content of a file.
        """
        try:
            with open(file_path, 'r', encoding=self.detect_encoding(file_path)) as file:
                content = file.read() if num_lines is None else ''.join([next(file) for _ in range(num_lines)])
            return content
        except UnicodeDecodeError as e:
            return f"Error decoding {file_path}: {str(e)}"
        except Exception as e:
            return f"Error reading {file_path}: {str(e)}"


    def detect_encoding(self, file_path: pathlib.Path) -> str:
        """
        Detect the character encoding of a file using the 'chardet' library.
        """
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding']

    def analyze_text_file(self, file_path: pathlib.Path):
        """
        Perform basic text analysis on the content of a text file.
        """
        if file_path.suffix.lower() == '.txt':
            content = self.read_file_content(file_path)
            word_count = len(content.split())
            unique_words = len(set(content.split()))
            print(f"Text analysis for {file_path}:")
            print(f"Total words: {word_count}")
            print(f"Unique words: {unique_words}")
            print("-" * 40)
        else:
            print(f"Cannot analyze content of {file_path}. Unsupported file type.")
            print("-" * 40)

    def filter_files_by_type(self, file_type: str) -> List[dict]:
        """
        Filter files based on their types.
        """
        filtered_files = [file_info for file_info in self.get_all_files() if file_info['type'].startswith(file_type)]
        return filtered_files
    
    
    def rename_file(self, old_name: str, new_name: str):
        """
        Rename a file in the current directory.
        """
        old_path = self.current_directory / old_name
        new_path = self.current_directory / new_name

        try:
            os.rename(old_path, new_path)
            return f"File '{old_name}' renamed to '{new_name}'."
        except FileNotFoundError:
            return f"Error: File '{old_name}' not found."
        except FileExistsError:
            return f"Error: File '{new_name}' already exists."
        except Exception as e:
            return f"Error renaming file: {str(e)}"

    def download_files(self, files: List[str], destination: str):
        """
        Download selected files to a specified destination.
        """
        for file_name in files:
            source_path = self.current_directory / file_name
            destination_path = pathlib.Path(destination) / file_name
            destination_path.write_bytes(source_path.read_bytes())

    def extract_archive(self, archive_file: str, destination: str):
        """
        Extract files from an archive to a specified destination.
        """
        archive_path = self.current_directory / archive_file
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination)

    def compare_files(self, file1: str, file2: str) -> bool:
        """
        Compare the content of two files.
        """
        file1_path = self.current_directory / file1
        file2_path = self.current_directory / file2
        return file1_path.read_text() == file2_path.read_text()

    def recursive_directory_listing(self):
        """
        Perform a recursive listing of files and folders.
        """
        for root, dirs, files in os.walk(self.current_directory):
            print(f"Current Directory: {root}")
            print("Files:")
            for file_name in files:
                print(f"  - {file_name}")
            print("Folders:")
            for dir_name in dirs:
                print(f"  - {dir_name}")
            print("-" * 40)

    def create_file_type(self, file_name: str, content: str = None, file_type: str = 'txt'):
        """
        Create a file in the current directory with specified content and type.
        """
        allowed_types = ['txt', 'json', 'py', 'js']  # Add more file types if needed

        if file_type not in allowed_types:
            print(f"Error: Unsupported file type '{file_type}'.")
            return

        file_path = self.current_directory / (file_name + '.' + file_type)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                if content is not None:
                    file.write(content)
            return f"File '{file_name}.{file_type}' created."
        except FileExistsError:
            return f"Error: File '{file_name}.{file_type}' already exists."
        except PermissionError:
            return f"Error: Permission denied to create file '{file_name}.{file_type}'."
        except Exception as e:
            return f"Error creating file: {str(e)}"

    def create_new_file(self, new_file_name: str, content: str = None):
        """
        Create a new file in the current directory.
        """
        new_file_path = self.current_directory / new_file_name

        try:
            with open(new_file_path, 'w', encoding='utf-8') as file:
                if content is not None:
                    file.write(content)
            return f"File '{new_file_name}' created."
        except FileExistsError:
            return f"Error: File '{new_file_name}' already exists."
        except Exception as e:
            return f"Error creating file: {str(e)}"

    def delete_file(self, file_name: str):
        """
        Delete a file in the current directory.
        """
        file_path = self.current_directory / file_name
        try:
            os.remove(file_path)
            print(f"File '{file_name}' deleted.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to delete file '{file_name}'.")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")

    def create_folder(self, folder_name: str):
        """
        Create a folder in the current directory if it doesn't exist.
        Neglect the operation if the folder already exists.
        """
        folder_path = self.current_directory / folder_name

        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder_name}' created or already exists.")
        except PermissionError:
            print(f"Error: Permission denied to create folder '{folder_name}'.")
        except Exception as e:
            print(f"Error creating folder: {str(e)}")
        
    def change_directory(self, new_directory: str):
        """
        Change the current working directory.
        """
        try:
            os.chdir(new_directory)
            self.current_directory = pathlib.Path(new_directory).resolve()
            print(f"Current working directory changed to: {self.current_directory}")
        except FileNotFoundError:
            print(f"Error: Directory '{new_directory}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to change directory to '{new_directory}'.")
        except Exception as e:
            print(f"Error changing directory: {str(e)}")

    def delete_directory(self, directory_name: str):
        """
        Delete a directory in the current working directory.
        """
        directory_path = self.current_directory / directory_name

        try:
            shutil.rmtree(directory_path)
            return f"Directory '{directory_name}' deleted."
        except FileNotFoundError:
            return f"Error: Directory '{directory_name}' not found."
        except PermissionError:
            return f"Error: Permission denied to delete directory '{directory_name}'."
        except Exception as e:
            return f"Error deleting directory: {str(e)}"

       
    def file_permission_info(self, file_name: str):
        """
        Display information about file permissions.
        """
        file_path = self.current_directory / file_name
        print(f"File Permissions for {file_name}: {os.stat(file_path).st_mode}")

    def recent_changes_info(self, num_changes: int = 5):
        """
        Display information about recent changes in the directory.
        """
        changes = sorted(self.get_all_files(), key=lambda x: x['modified'], reverse=True)[:num_changes]
        print(f"Recent Changes:")
        for change in changes:
            print(f"  - {change['name']}: {change['modified']}")
        print("-" * 40)

    def user_preferences(self, sort_by: str = "name", display_detail: bool = True):
        """
        Set and display user-specific preferences for directory information.
        """
        # Adjust the display based on user preferences
        files_info = self.get_all_files(sort_by=sort_by)
        if display_detail:
            self.print_file_info(files_info)
        else:
            for file_info in files_info:
                print(f"Name: {file_info['name']}")

    # Placeholder for Additional Features:

    # def additional_feature_1(self):
    #     """
    #     Description of additional feature 1.
    #     """
    #     # Implementation of additional feature 1

    # def additional_feature_2(self):
    #     """
    #     Description of additional feature 2.
    #     """
    #     # Implementation of additional feature 2

    # ... (Other methods for additional features)

if __name__ == "__main__":
    explorer = Explorer()

    # Display directory information
    explorer.explore_directory()

    # Get and display all files sorted by name
    print("Files in the current directory (sorted by name):")
    files_info = explorer.get_all_files(sort_by="name")
    explorer.print_file_info(files_info)

    # Search for files containing a keyword
    keyword = "example"
    print(f"Files containing '{keyword}':")
    matching_files = explorer.search_files(keyword)
    explorer.print_file_info(matching_files)

    # Get statistics on file types
    print("File type statistics:")
    type_statistics = explorer.get_file_type_statistics()
    for file_type, count in type_statistics.items():
        print(f"{file_type}: {count} files")

    # Preview content of specific file types
    file_to_preview = "example.txt"
    explorer.preview_file_content(explorer.current_directory / file_to_preview)

    # Read and display content of a file
    file_to_read = "example.txt"
    num_lines_to_read = 3
    content = explorer.read_file_content(explorer.current_directory / file_to_read, num_lines=num_lines_to_read)
    print(f"Content of {file_to_read} (first {num_lines_to_read} lines):")
    print(content)

    # Analyze text file
    text_file_to_analyze = "sample_text.txt"
    explorer.analyze_text_file(explorer.current_directory / text_file_to_analyze)

    # Rename a file
    old_name = "old_name.txt"
    new_name = "new_name.txt"
    explorer.rename_file(old_name, new_name)

    # Create a new file with content
    new_file_name = "new_file.txt"
    new_file_content = "This is the content of the new file."
    explorer.create_new_file(new_file_name, content=new_file_content)

    # Delete a file
    file_to_delete = "file_to_delete.txt"
    explorer.delete_file(file_to_delete)

    # Filter files by type
    filtered_text_files = explorer.filter_files_by_type("text")
    print("Filtered Text Files:")
    explorer.print_file_info(filtered_text_files)

    # Download files
    files_to_download = ["example.txt", "sample.json"]
    download_destination = "C:\\Users\\ADAN COMPUTER\\Desktop\\instabuildhub\\sys\\download"
    explorer.download_files(files_to_download, download_destination)

    # Extract archive
    archive_to_extract = "example.zip"
    extraction_destination = "/path/to/extract"
    explorer.extract_archive(archive_to_extract, extraction_destination)

    # Compare files
    file1 = "example.txt"
    file2 = "sample.txt"
    is_same_content = explorer.compare_files(file1, file2)
    print(f"Content of {file1} and {file2} is the same: {is_same_content}")

    # Recursive directory listing
    explorer.recursive_directory_listing()

    # File permission info
    file_to_check = "example.txt"
    explorer.file_permission_info(file_to_check)

    # Recent changes info
    explorer.recent_changes_info()

    # User preferences
    explorer.user_preferences(sort_by="modified", display_detail=False)

    # Placeholder for Additional Features:

    # ... (Examples for using additional features)

    # Additional Feature Usage Examples:

    # explorer.additional_feature_1()
    # explorer.additional_feature_2()

    # ... (Other examples for using additional features)
