import os
from data import FileTag
from data import FolderTag

"""def listdir_sort(path):
    file_dict = {"path":path,"folders":list(),"files":list()}
    print(file_dict)
    for file in os.listdir(path):
        if len(file.split(".")) == 1:
            file_dict["folders"].append(listdir_sort(path+"/"+file))
        else:
            file_dict["files"].append(file)
    return file_dict




def directory_view(file_dict, indent=1):
    output = ""
    indent_str = "----" * indent
    folder_name = os.path.basename(file_dict["path"])
    output += f"{indent_str}{folder_name}\n"

    for file in file_dict["files"]:
        output += f"{indent_str}----{file}\n"

    for folder in file_dict["folders"]:
        output += directory_view(folder, indent + 1)

    return output"""
"""def listdir_tagged(path):
    WorkFolder = FolderTag(path)
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            pass
        else:
            WorkFolder.insert_file(FileTag(os.path.join(path, file)))"""

work_dir = str()

while work_dir == "":
    work_dir = input("Please input a work directory")

os.chdir(work_dir)


print(os.listdir(work_dir))
WorkFolder = FolderTag(work_dir)
print(WorkFolder.print_files())