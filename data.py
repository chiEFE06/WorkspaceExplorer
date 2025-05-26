import os


class FileTag:
    def __init__(self, file_path, maintag="", subtags=None):
        if subtags is None:
            subtags = []
        self.maintag = maintag.lower()
        self.subtags = subtags
        self.file_path = os.path.normcase(file_path).lower()
        self.file_name = os.path.basename(file_path).lower()

    def get_maintag(self):
        return self.maintag
    def get_subtags(self):
        return self.subtags
    def get_file_path(self):
        return self.file_path
    def get_file_name(self):
        return self.file_name

    def add_maintag(self,maintag):
        self.maintag = maintag.lower()

    def add_subtag(self,subtag,old_subtag=""):
        subtag = subtag.lower()
        if old_subtag != "":
            try:
                self.subtags.remove(old_subtag)
            except ValueError:
                print("Given subtag does not exist")
        if subtag not in self.subtags:
            self.subtags.append(subtag)
        else:
            print("Given subtag already exists")

    def remove_maintag(self):
        self.maintag = "ignore"

    def remove_subtag(self,old_subtag=""):
        if old_subtag != "":
            try:
                self.subtags.remove(old_subtag)
            except ValueError:
                print("Given subtag does not exist")
        else:
            self.subtags = []


    def __str__(self):
        return f"{self.file_name}, maintag='{self.maintag}', subtags={self.subtags}"
    def __repr__(self):
        return str(self) + " " + f"path: {self.file_path}"

"""class FolderTag:
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
            return self.search_for_file(folder_ord[0])"""
