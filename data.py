import os


class FileTag:
    def __init__(self,file_path,maintag="",subtags=[]):
        self.maintag = maintag
        self.subtags = subtags
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

    def __str__(self):
        return f"FileTag({self.file_name}, main='{self.maintag}', subtags={self.subtags})"

class FolderTag:
    def __init__(self, folder_path):
        self.folder_name = os.path.basename(folder_path)
        self.folder_path = folder_path
        self.files = []
        self.folders = []

        for entry in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, entry)
            if os.path.isdir(full_path):
                self.insert_folder(full_path)
            else:
                self.insert_file(full_path)

    def insert_file(self, file_path):
        self.files.append(FileTag(file_path))

    def insert_folder(self, folder_path):
        self.folders.append(FolderTag(folder_path))

    def print_files(self,indent=0):
        output = ""
        indent_str = "----" * indent
        output += f"{indent_str}{self.folder_name}\n"
        for file in self.files:
            output += f"{indent_str}----{file.file_name}\n"
        for folder in self.folders:
            output += folder.print_files(indent + 1)
        return output

    def search_for_file(self, file_name):

        for file in self.files:
            if file.file_name == file_name:
                print(f"Found {file.file_name}")
                return file

        for folder in self.folders:
            folder.search_for_file(file_name)

    def file_by_path(self, relative_path):
        folder_ord = relative_path.split("/")
        if len(folder_ord) == 1:
            return self.search_for_file(folder_ord[0])
