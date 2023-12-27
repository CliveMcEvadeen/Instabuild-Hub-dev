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
        }
        print("Current Directory:")
        print(f"Name: {dir_info['name']}")
        print(f"Path: {dir_info['path']}")
        print(f"Created: {dir_info['created']}")
        print(f"Modified: {dir_info['modified']}")
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
            if file_path.is_file() and keyword.lower() in file_path.read_text().lower():
                file_info = self.get_file_info(file_path)
                matching_files.append(file_info)
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

    def preview_file_content(self, file_path: pathlib.Path, num_lines: int = 5):
        """
        Display a preview of the content of specific file types.
        """
        if file_path.suffix.lower() in ['.txt', '.py', '.md', '.json']:
            print(f"Content preview of {file_path}:")
            with open(file_path, 'r', encoding='utf-8') as file:
                for _ in range(num_lines):
                    line = file.readline().strip()
                    print(line)
            print("-" * 40)
        else:
            print(f"Cannot preview content of {file_path}. Unsupported file type.")
            print("-" * 40)

    def read_file_content(self, file_path: pathlib.Path, num_lines: int = None) -> str:
        """
        Read and return the content of a file.
        """
        try:
            with open(file_path, 'r', encoding=self.detect_encoding(file_path)) as file:
                content = file.read() if num_lines is None else ''.join([next(file) for _ in range(num_lines)])
            return content
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
    download_destination = "/path/to/download"
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
