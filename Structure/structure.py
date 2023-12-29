import os
from datetime import datetime
from hurry.filesize import size
from colorama import init, Fore  # Install the 'colorama' package using pip

init(autoreset=True)  # Initialize colorama

class ProjectStructure:
    def __init__(self, base_path, include_file_types=None, exclude_file_types=None):
        self.base_path = base_path
        self.include_file_types = include_file_types
        self.exclude_file_types = exclude_file_types
        self.structure = {}
        self.show_file_content = False  # Default to not show file content

    def _is_valid_file(self, file_name):
        if self.include_file_types and not any(file_name.lower().endswith(ext) for ext in self.include_file_types):
            return False
        if self.exclude_file_types and any(file_name.lower().endswith(ext) for ext in self.exclude_file_types):
            return False
        return True

    def _build_structure(self, current_path, node):
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                node[entry] = {"type": "folder", "size": None, "modified": None, "content": {}}
                self._build_structure(entry_path, node[entry]["content"])
            elif os.path.isfile(entry_path) and self._is_valid_file(entry):
                size_in_bytes = os.path.getsize(entry_path)
                modified_time = datetime.fromtimestamp(os.path.getmtime(entry_path))
                node[entry] = {
                    "type": "file",
                    "size": size(size_in_bytes),
                    "modified": modified_time.strftime("%Y-%m-%d %H:%M:%S")
                }

    def _calculate_folder_size(self, node):
        total_size = 0
        for name, info in node.items():
            if info["type"] == "folder":
                total_size += self._calculate_folder_size(info["content"])
            elif info["type"] == "file":
                file_path = os.path.join(self.base_path, name)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
                else:
                    pass
                    # print(f"{Fore.RED}File not found: {file_path}")
        return total_size

    def _calculate_total_size(self):
        return self._calculate_folder_size(self.structure)

    def _draw_file_content(self, file_name, indent):
        file_path = os.path.join(self.base_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"{Fore.GREEN}  " * indent + f"{Fore.GREEN}Content:")
                print(content)
        except Exception as e:
            print(f"{Fore.RED}  " * indent + f"{Fore.RED}Error reading content of {file_name}: {str(e)}")

    def read_project_structure(self):
        self._build_structure(self.base_path, self.structure)

    def draw_project_structure(self, node=None, indent=0):
        if node is None:
            node = self.structure

        for name, info in node.items():
            if info["type"] == "folder":
                print(f"{Fore.BLUE}  " * indent + f"- {name} (Folder)")
                if info["size"] is not None:
                    print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Size: {info['size']}")
                if info["modified"] is not None:
                    print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Last Modified: {info['modified']}")
                self.draw_project_structure(info["content"], indent + 1)
            elif info["type"] == "file":
                print(f"{Fore.GREEN}  " * indent + f"- {name} (File)")
                print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Size: {info['size']}")
                print(f"{Fore.CYAN}  " * (indent + 1) + f"{Fore.CYAN}Last Modified: {info['modified']}")
                if self.show_file_content:
                    self._draw_file_content(name, indent + 1)

        if indent == 0:
            total_size = self._calculate_total_size()
            print(f"\nTotal Project Size: {Fore.CYAN}{size(total_size)}")

if __name__ == "__main__":
    # Example usage
    instabuildhub_path = r"C:\Users\ADAN COMPUTER\Desktop\instabuildhub"
    project_structure = ProjectStructure(
        base_path=instabuildhub_path,
        include_file_types=[
    ".py", ".yaml", ".txt", ".cff", ".json", ".sh", ".env", ".template", ".dockerignore", ".toml",
    ".h264", ".mkv", ".flv", ".wmv", ".3gp",  # Video Files
    ".flac", ".aac", ".wma",                  # Audio Files
    ".bmp", ".tiff", ".ico",                  # Image Files
    ".psd", ".ai", ".eps",                    # Adobe Photoshop Files
    ".indd", ".cdr", ".svg",                  # Design Files
    ".avi", ".mpeg", ".mpg", ".mov",          # Video Files
    ".ogg", ".webm",                          # Audio/Video Files
    ".epub", ".mobi", ".azw",                 # E-book Files
    ".tar", ".gz", ".bz2", ".xz",             # Tarball Archives
    ".rpm", ".deb",                           # Package Installer Files
    ".bat", ".cmd", ".sh", ".bash",           # Shell Script Files
    ".ico", ".cur",                           # Icon Files
    ".webp", ".jp2", ".jxr", ".bpg",          # Advanced Image Formats
    ".ac3", ".mka",                           # Audio Files
    ".blend", ".obj", ".fbx", ".stl",         # 3D Model Files
    ".pdb", ".obj", ".pyc", ".pyd",           # Compiled Files
    ".bak", ".old", ".swp", ".swo",           # Backup and Temporary Files
    ".ps1", ".psm1", ".psd1",                 # PowerShell Script Files
    ".html", ".htm", ".php",                  # Web Files
    ".css", ".scss", ".less",                 # Style Sheets
    ".js", ".jsx", ".ts", ".tsx", ".vue",     # JavaScript and Web Development
    ".java", ".class", ".jar",                # Java Files
    ".py", ".pyc", ".pyd",                    # Python Files
    ".rb", ".rhtml", ".erb",                  # Ruby Files
    ".pl", ".pm",                             # Perl Files
    ".cpp", ".c", ".h", ".hpp",               # C and C++ Files
    ".swift", ".m", ".mm",                    # Swift Files
    ".go",                                   # Go Files
    ".dart",                                 # Dart Files
    ".lua",                                  # Lua Files
    ".rust",                                 # Rust Files
    ".scala",                                # Scala Files
    ".kotlin",                               # Kotlin Files
    ".groovy",                               # Groovy Files
    ".bat", ".cmd",                          # Batch Files
    ".ps1", ".psm1",                         # PowerShell Files
    ".json", ".yaml", ".yml",                # Data Serialization
    ".xml", ".json", ".yaml", ".yml",        # Data Serialization
    ".sql", ".db", ".sqlite",                # Database Files
    ".conf", ".config", ".ini",              # Configuration Files
    ".ini",                                  # Configuration Files
    ".md", ".markdown",                      # Markdown Files
    ".tex", ".bib",                           # LaTeX Files
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", # Document Files
    ".xls", ".xlsx",                         # Spreadsheet Files
    ".csv",                                  # CSV Files
    ".rtf",                                  # Rich Text Format
    ".txt",                                  # Text Files
    ".log",                                  # Log Files
    ".bak", ".swp", ".swo",                  # Backup and Swap Files
    ".url", ".webloc", ".desktop",           # Shortcut Files
    ".dll", ".lib", ".so",                   # Library Files
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", # Document Files
    ".xls", ".xlsx",                         # Spreadsheet Files
    ".zip", ".rar", ".tar", ".gz",           # Archive Files
    ".exe", ".msi", ".apk",                  # Executable Files
    ".mp3", ".wav", ".ogg",                  # Audio Files
    ".mp4", ".avi", ".mov", ".mkv",          # Video Files
    ".jpeg", ".jpg", ".png", ".gif",         # Image Files
    ".svg", ".eps", ".ai",                   # Vector Graphics
    ".torrent",                              # Torrent Files
    ".dwg",                                  # AutoCAD Drawing
    ".ppt", ".pptx",                         # PowerPoint Presentation
    ".key",                                  # Keynote Presentation
    ".accdb",                                # Microsoft Access Database
    ".msg",                                  # Outlook Mail Message
    ".eml",                                  # Email Message
    ".ics",                                  # Calendar File
    ".apk",                                  # Android Package File
    ".rpm",                                  # Red Hat Package Manager File
    ".dmg",                                  # Mac OS X Disk Image
    ".iso",                                  # Disc Image
    ".ova",                                  # Open Virtualization Appliance
    ".vdi",                                  # VirtualBox Disk Image
    ".bak", ".backup",                       # Backup Files
    ".conf", ".config",                      # Configuration Files
    ".bak",                                  # Backup File
    ".swf",                                  # Shockwave Flash File
    ".ics",                                  # iCalendar File
    ".dll", ".sys",                          # System Files
    ".idx", ".sub",                          # Subtitle Files

     ".iso",                                  # Disc Image
    ".ova",                                  # Open Virtualization Appliance
    ".vdi",                                  # VirtualBox Disk Image
    ".bak", ".backup",                       # Backup Files
    ".conf", ".config",                      # Configuration Files
    ".bak",                                  # Backup File
    ".swf",                                  # Shockwave Flash File
    ".ics",                                  # iCalendar File
    ".dll", ".sys",                          # System Files
    ".idx", ".sub",                          # Subtitle Files
    ".ics",                                  # iCalendar File
    ".bat", ".com", ".cmd",                  # Batch Files
    ".eps", ".ps",                           # PostScript Files
    ".gz", ".bz2", ".tar", ".xz",            # Compressed Archive Files
    ".dmg",                                  # Mac OS X Disk Image
    ".bin", ".cue",                          # CD/DVD Image Files
    ".arj", ".lzh", ".tar.gz", ".tar.bz2",   # Archive Files
    ".xml", ".xsl", ".xsd",                  # XML Files
    ".url", ".webloc", ".desktop",           # Shortcut Files
    ".bmp", ".gif", ".png", ".tiff", ".jpg", # Bitmap and Image Files
    ".txt", ".ini", ".conf", ".log",         # Text and Configuration Files
    ".wav", ".mp3", ".flac", ".aac",         # Audio Files
    ".avi", ".mp4", ".mkv", ".mov",          # Video Files
    ".ttf", ".otf", ".fon",                  # Font Files
    ".csv", ".tsv",                          # Spreadsheet and Tab-Delimited Files
    ".json", ".yaml", ".yml",                # JSON and YAML Files
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", # Document Files
    ".xls", ".xlsx",                         # Spreadsheet Files
    ".md", ".markdown",                      # Markdown Files
    ".php", ".jsp", ".asp", ".aspx",         # Web Development Files
    ".html", ".htm", ".css", ".js",          # Web Files
    ".py", ".java", ".cpp", ".c", ".swift",  # Code Files
    ".dll", ".lib", ".so",                   # Library Files
    ".exe", ".msi", ".app",                  # Executable Files
    ".pkg", ".deb", ".rpm",                  # Package Installer Files
    ".db", ".sqlite",                        # Database Files
    ".psd", ".ai", ".cdr",                    # Design Files
    ".wmv", ".mov", ".mkv", ".flv",          # Multimedia Files
    ".ogg", ".mp3", ".wav", ".flac",         # Audio Files
    ".jpeg", ".jpg", ".png", ".gif",         # Image Files
    ".ppt", ".pptx", ".key",                 # Presentation Files
    ".eml", ".msg",                          # Email Files
    ".log", ".txt",                          # Log Files
    ".tmp", ".temp", ".swp",                 # Temporary Files
    ".bak", ".old",                          # Backup and Old Files
    ".srt", ".sub",                          # Subtitle Files
    ".rar", ".zip", ".7z", ".tar", ".gz",    # Archive Files
    ".bak", ".backup",                       # Backup Files
    ".conf", ".config", ".ini",              # Configuration Files
    ".bak",                                  # Backup File
    ".swf",                                  # Shockwave Flash File
    ".ics",                                  # iCalendar File
    ".dll", ".sys",                          # System Files
    ".idx", ".sub",                          # Subtitle Files
    ".m3u", ".pls",                          # Playlist Files
    ".conf", ".config",                      # Configuration Files
    ".bak",                                  # Backup File
    ".swf",                                  # Shockwave Flash File
    ".ics",                                  # iCalendar File
    ".dll", ".sys",                          # System Files
    ".idx", ".sub",   
    ".in" 
],  # Include specific file types (optional)

        exclude_file_types=[".log"]  # Exclude specific file types (optional)
    )
    project_structure.read_project_structure()
    project_structure.draw_project_structure()
