import os


class FileTag:
    def __init__(self, file_path, maintag="", subtags=tuple()):
        self.maintag = maintag.lower()
        self.subtags = subtags
        #For some reason, mutable objects like lists are stored globally for all FileTag type objects. Hence, all operations on subtags are made by type-casting to a list
        self.file_path = os.path.normcase(file_path).lower()
        self.file_name = os.path.basename(file_path).lower()

    #get_attr functions, although they are not even private
    def get_maintag(self):
        return self.maintag
    def get_subtags(self):
        return self.subtags
    def get_file_path(self):
        return self.file_path
    def get_file_name(self):
        return self.file_name
    def get_tag_data(self):
        return self.maintag, self.subtags

    def add_maintag(self,maintag,old_maintag=""):
        # Adds or replaces the main tag of the file
        # If an old_maintag given, only replaces when tags match
        maintag, old_maintag = maintag.lower(), old_maintag.lower()
        if (old_maintag != "" and old_maintag == self.maintag) or (old_maintag == ""):
            self.maintag = maintag

    def add_subtag(self,subtag,old_subtag=""):
        # Adds a subtag if an old_subtag is not inputted
        # Replaces the subtag if an old_subtag is inputted
        subtag = subtag.lower()
        old_subtag = old_subtag.lower()
        output_list = list(self.subtags)
        if old_subtag != "":
            try:
                output_list.remove(old_subtag)
            except ValueError:
                print("Subtag to replace does not exist")
        if subtag not in output_list:
            output_list.append(subtag)
        else:
            print("Given subtag already exists")

        self.subtags = tuple(output_list)

    def remove_maintag(self,old_maintag=""):
        # Replaces the main tag of the file with "ignore"
        # If an old_maintag given, only replaces when tags match
        old_maintag = old_maintag.lower()
        if (old_maintag != "" and old_maintag == self.maintag) or (old_maintag == ""):
            self.maintag = "ignore"


    def remove_subtag(self,old_subtag=""):
    # Clears the subtags tuple if an old_subtag is not given
    # Removes the specific subtag from subtags tuple if an old_subtag is given
        old_subtag = old_subtag.lower()
        output_list = list(self.subtags)
        if old_subtag != "":
            try:
                output_list.remove(old_subtag)
            except ValueError:
                print("Subtag to remove does not exist")
        else:
            output_list = []
        self.subtags = tuple(output_list)

    # debug functions
    def __str__(self):
        return f"{self.file_name}, maintag='{self.maintag}', subtags={self.subtags}"
    def __repr__(self):
        return str(self) + " " + f"path: {self.file_path}"

    #ditched the FolderTag idea because of nested classes
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
