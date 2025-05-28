import os
import xml.etree.ElementTree as ET
import pickle
from data import FileTag
import argparse
import shutil

data_file = "user_data.xml"
tag_file = "tag_data.pkl"

def get_work_dir_from_xml():
    # Reads the work directory from user_data.xml.
    tree = ET.parse(data_file)
    root = tree.getroot()
    work_dir = root.find("work_dir").text
    return work_dir

def create_user_data_xml(work_dir):
    # Creates the XML file with the work directory
    root = ET.Element("user_data")
    ET.SubElement(root, "work_dir").text = os.path.normpath(work_dir).lower()
    tree = ET.ElementTree(root)
    tree.write(data_file)
def get_or_create_work_dir():
    # Main function to either get from XML or prompt and save
    if os.path.exists(data_file):
        try:
            work_dir = get_work_dir_from_xml()
            if os.path.isdir(work_dir):
                return work_dir
            else:
                print("Saved directory is invalid. Please enter a new one.")
        except Exception as e:
            print("Failed to read user_data.xml:", e)

    # If XML doesn't exist or is invalid, ask the user
    while True:
        work_dir = input("Enter work directory: ").strip()
        work_dir = os.path.abspath(work_dir).lower()
        if os.path.isdir(work_dir):
            create_user_data_xml(work_dir)
            return work_dir
        else:
            print("Invalid directory. Try again.")

def save_tag_data(file_list,save_file):
    # Turns the given FileTag list to dictionary as file_path:FileTag then saves it to a .pkl file
    output_dict = dict()
    for entry in file_list:
        output_dict[entry.get_file_path()] = entry
    # Saving as dictionary to provide direct access from path to FileTag
    try:
        f = open(save_file, "wb")
        pickle.dump(output_dict, f)
    except Exception as e:
        print("Failed to save tag data ", e)
    else:
        print("Saved tag data successfully")

def save_tag_data_from_dict(file_dict, save_file):
    # Saves the tag data directly from dictionary
    try:
        f = open(save_file, "wb")
        pickle.dump(file_dict, f)
    except Exception as e:
        print("Failed to save tag data ", e)
    else:
        print("Saved tag data successfully")

def read_pickle(save_file):
    # Reads the tag data from tag_data.pkl.
    with open(save_file, "rb") as f:
        loaded_obj = pickle.load(f)
        return loaded_obj

def get_or_create_tag_data():
    # Initial method to either read or get file list
    output_dict = dict()
    if os.path.exists(tag_file):
        try:
            output_dict = read_pickle(tag_file)
        except Exception as e:
            print("Failed to read tag data,deleting the file", e)

    # If tag_data doesn't exist or is corrupt, discovers files inside the work folder and asks for a user input
    else:
        file_list = search_for_files(work_folder)
        for file in file_list:
            file.add_maintag(input(f"Enter a main tag for {file.file_name}: "))
        save_tag_data(file_list,tag_file)
        try:
            output_dict = read_pickle(tag_file)
        except Exception as e:
            print("Failed to read tag data,deleting the file", e)
            os.remove(tag_file)

    return output_dict


def remove_file(file_path,use_folder=False,work_dir=None):
    # First removes the file data from the memory then deletes the file
    file_path=os.path.join(work_dir,file_path) if work_dir else file_path
    file_path=os.path.normpath(file_path)
    file_path=file_path.lower()
    # Works recursively if the given file_path is a folder
    if use_folder and os.path.isdir(file_path):
        for entry in os.scandir(file_path):
            if entry.is_file():
                # If the inputted path is file, deletes it along with its tag data
                try:
                    file_dict.pop(str(entry.path))
                    os.remove(entry.path)
                except FileNotFoundError as e:
                    print("Couldn't locate file", e)
                except KeyError as e:
                    print("Key error on", e)
                else:
                    print("Removed file", entry.name)
                pass
            else:
                remove_file(entry.path,True)
        os.rmdir(file_path)
        print(f"Removed {file_path}")
    # If the given path is a folder but use_folder is false, denies the action
    elif os.path.isdir(file_path):
        print("Selection is a folder, please use -R modifier")
    else:
        # If the inputted path is file, deletes it along with its tag data
        try:
            file_dict.pop(str(file_path))
            os.remove(file_path)
        except FileNotFoundError as e:
            print("Couldn't locate file", e)
        except KeyError as e:
            print("Key error on", e)
        else:
            print("Removed file", file_path)
        pass

def search_for_files(work_dir):
    # Search for all files in the work dir and in its sub folders and adds them as FileTag to a list
    output = list()
    for entry in os.scandir(work_dir):
        if entry.is_dir():
            output.extend(search_for_files(entry.path))
        else:
            output.append(FileTag(entry.path))
    return output

def copy_file(file_path,target_path,copy_tags = bool(),work_dir = None):
    # Copies a file with its tag data if copy_tags is true
    file_path = os.path.join(work_dir, file_path) if work_dir else file_path
    file_path = os.path.normpath(file_path).lower()
    target_path = os.path.join(work_dir, target_path) if work_dir else target_path
    target_path = os.path.normpath(target_path)
    if os.path.isdir(file_path) or os.path.isdir(target_path):
        print("Given paths should be to a file")
        return
    if find_filetag_from_file(file_path):
        main_file = find_filetag_from_file(file_path)
        shutil.copy(file_path, target_path)
        new_maintag,new_subtags = main_file.get_tag_data()
        file_dict[target_path.lower()] = FileTag(target_path,new_maintag,new_subtags) if copy_tags else FileTag(target_path)
        if not copy_tags:
            file = file_dict[target_path.lower()]
            file.add_maintag(input(f"Enter a main tag for {file.file_name}: "))
    print("Copied the file to: ",target_path)
    return True

def move_file(file_path,target_path,work_dir = None):
    # Moves a file using copy_file and remove_file methods
    if copy_file(file_path,target_path,True,work_dir):
        remove_file(file_path,False,work_dir)

def update_files(work_dir):
    # Checks for new files inside the given directory
    # Directly operates on global variables
    for entry in os.scandir(work_dir):
        entry_path = os.path.normcase(entry.path)
        if entry.is_file():
            if entry_path not in file_paths:
                entry = FileTag(entry.path)
                entry.add_maintag(input(f"New file found, enter a main tag for {entry.file_name}: "))
                file_dict[entry_path] = entry

        else:
            update_files(entry.path)
    # Checks the memory for tagg-less files, asks for an input if any found
    for entry in file_list:
        if entry.get_maintag() == "":
            entry.add_maintag(input(f"Enter a main tag for {entry.file_name}: "))

    return

def recursive_addtag(work_dir,tag_list,path_input,tag_type,tag):
    # Adds a tag to all files inside given folder and it's sub-folders
    path = os.path.join(work_dir,path_input)
    path = os.path.normpath(path)
    for file in tag_list:
        if file.get_file_path().startswith(path):
            if tag_type == "M":
                file.add_maintag(tag)
            elif tag_type == "S":
                file.add_subtag(tag)
    save_tag_data_from_dict(file_dict, tag_file)

def recursive_removetag(work_dir,tag_list,path_input,tag_type,existing_tag=""):
    # Removes tag(s) from all files inside given folder and it's sub-folders
    path = os.path.join(work_dir,path_input)
    path = os.path.normpath(path)
    for file in tag_list:
        if file.get_file_path().startswith(path):
            if tag_type == "M":
                file.remove_maintag(existing_tag)
            elif tag_type == "S":
                file.remove_subtag(existing_tag)
    save_tag_data_from_dict(file_dict,tag_file)

def recursive_edittag(work_dir,tag_list,path_input,tag_type,tag,existing_tag=""):
    # Replaces tag(s) from all files inside given folder and it's sub-folders
    path = os.path.join(work_dir,path_input)
    path = os.path.normpath(path)
    for file in tag_list:
        if file.get_file_path().startswith(path):
            if tag_type == "M" and file.get_maintag() == existing_tag:
                file.add_maintag(tag,existing_tag)
            elif tag_type == "S":
                file.add_subtag(tag,existing_tag)

    save_tag_data_from_dict(file_dict, tag_file)

def print_files(folder_path,tag_type=str(),indent=0):
    # Lists files with their hierarchy
    output = str()
    indent_str = "____"*indent
    output += f"{indent_str}{os.path.basename(folder_path)}\n"
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            output += print_files(entry.path,tag_type,indent + 1)
        elif entry.is_file():
            file = find_filetag_from_file(entry.path)
            if tag_type == "M":
                output += f"{indent_str}____{file.get_file_name()}: {file.get_maintag()}\n"
            elif tag_type == "S":
                output += f"{indent_str}____{file.get_file_name()}: {file.get_subtags()}\n"
            elif tag_type == "B":
                output += f"{indent_str}____{file.get_file_name()}: {file.get_maintag()} | {file.get_subtags()}\n"
    return output

def find_filetag_from_file(path):
    # Finds the FileTag object from its path, returns an error if not found
    try:
        file = file_dict[path.lower()]
    except KeyError:
        print(f"File '{path}' not found in tag data.")
        return
    return file

def search_for_tags(path,tag_list,tag_type,tag):
    # Linear search inside the memory for any given tag
    output = list()
    path = path.lower()
    for file in tag_list:
        if file.get_file_path().startswith(path):
            if tag_type == "M" and file.get_maintag() == tag:
                output.append(f"Found {file.get_file_name()} in {file.get_file_path()}")
            elif tag_type == "S" and tag in file.get_subtags():
                output.append(f"Found {file.get_file_name()} in {file.get_file_path()}")
    return "\n".join(output)

def main():
    # main function for command arguments
    parser = argparse.ArgumentParser(prog="Workplace Explorer", description="Tag-based file explorer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # addtag command
    addtag_parser = subparsers.add_parser("addtag", help="Adds tag(s) to file(s)")
    addtag_parser.add_argument(
        "-R", "--recursive", help="Recursively add tag(s) to all files inside a folder", action="store_true"
    )
    addtag_parser.add_argument("relative_path", help="Relative path to file or folder")
    addtag_parser.add_argument("tag_type", choices=["M", "S"], help="Tag type: M for maintag, S for subtag")
    addtag_parser.add_argument("tag_to_add", help="Tag to add")

    # removetag command
    removetag_parser = subparsers.add_parser("removetag", help="Removes tag(s) from file(s)")
    removetag_parser.add_argument(
        "-R", "--recursive", help="Recursively remove tag(s) from all files inside a folder", action="store_true"
    )
    removetag_parser.add_argument("relative_path", help="Relative path to file or folder")
    removetag_parser.add_argument("tag_type", choices=["M", "S"], help="Tag type: M for maintag, S for subtag")
    removetag_parser.add_argument("-t","--tag_to_remove", help="Tag to remove", default="")

    # edittag command
    edittag_parser = subparsers.add_parser("edittag", help="Edits tag(s) of file(s)")
    edittag_parser.add_argument(
        "-R", "--recursive", help="Recursively edit tag(s) of all files inside a folder", action="store_true"
    )
    edittag_parser.add_argument("relative_path", help="Relative path to file or folder")
    edittag_parser.add_argument("tag_type", choices=["M", "S"], help="Tag type: M for maintag, S for subtag")
    edittag_parser.add_argument("new_tag", help="New tag")
    edittag_parser.add_argument("old_tag", help="Tag to replace")

    #search command
    search_parser = subparsers.add_parser("search", help="Search tag(s) of file(s)")
    search_parser.add_argument("-R","--search_folder", help="Specify the folder to search in")
    search_parser.add_argument("tag_type", choices=["M", "S"], help="Tag type: M for maintag, S for subtag")
    search_parser.add_argument("tag", help="Tag to search for")

    #mkdir command
    mkdir_parser = subparsers.add_parser("mkdir", help="Create a folder")
    mkdir_parser.add_argument("relative_path", help="Relative path of the new folder")

    #remove command
    remove_parser = subparsers.add_parser("remove", help="Remove files/folders")
    remove_parser.add_argument("-R","--recursive", help="Recursively remove files inside a folder", action="store_true")
    remove_parser.add_argument("relative_path", help="Relative path")

    #copy command
    copy_parser = subparsers.add_parser("copy", help="Copy a file")
    copy_parser.add_argument("source_path", help="Relative path of the source file")
    copy_parser.add_argument("dest_path", help="Relative path of the destination file")
    copy_parser.add_argument("-t","--copy_tags", help="Copy tags along the file",action="store_true")

    #move command
    move_parser = subparsers.add_parser("move", help="Move a file")
    move_parser.add_argument("source_path", help="Relative path of the source file")
    move_parser.add_argument("dest_path", help="Relative path of the destination file")

    #list command
    list_parser = subparsers.add_parser("list", help="List all files")
    list_parser.add_argument("tag_type", choices=["M", "S","B"], help="Tag type: M for maintag, S for subtag, B for both")


    args = parser.parse_args()

    if args.command == "addtag":
        tag_type = args.tag_type
        tag = args.tag_to_add
        path = os.path.join(work_folder, args.relative_path)
        path = os.path.normpath(path)
        if args.recursive:
            recursive_addtag(work_folder,file_list,args.relative_path,tag_type,tag)
        else:
            file = find_filetag_from_file(path)
            if tag_type == "M":
                file.add_maintag(tag)
            elif tag_type == "S":
                file.add_subtag(tag)

        print('Successfully added ' + tag + ' to ' + path)

    elif args.command == "removetag":
        tag_type = args.tag_type
        tag = args.tag_to_remove
        path = os.path.join(work_folder, args.relative_path)
        path = os.path.normpath(path)
        if args.recursive:
            recursive_removetag(work_folder,file_list,args.relative_path,tag_type,tag)
        else:
            file = find_filetag_from_file(path)
            if tag_type == "M":
                file.remove_maintag(tag)
            elif tag_type == "S":
                file.remove_subtag(tag)

    elif args.command == "edittag":
        tag_type = args.tag_type
        existing_tag = args.old_tag
        new_tag = args.new_tag
        path = os.path.join(work_folder, args.relative_path)
        path = os.path.normpath(path)
        if args.recursive:
            recursive_edittag(work_folder,file_list,args.relative_path,tag_type,new_tag,existing_tag)
        else:
            file = find_filetag_from_file(path)
            if tag_type == "M" and file.get_maintag() == existing_tag:
                file.add_maintag(new_tag,existing_tag)
            elif tag_type == "S":
                file.add_subtag(new_tag,existing_tag)

    elif args.command == "search":
        tag_type = args.tag_type
        tag = args.tag.lower()
        search_folder = os.path.join(work_folder,args.search_folder) if args.search_folder else work_folder
        search_folder = os.path.normpath(search_folder)
        print(search_for_tags(search_folder,file_list,tag_type, tag))

    elif args.command == "mkdir":
        path = os.path.join(work_folder, args.relative_path)
        path = os.path.normpath(path)
        try:
            os.mkdir(path)
        except FileExistsError:
            print("Folder " + path + " already exists")
        except OSError as e:
            print("Failed to create directory", e)
        except Exception as e:
            print(e)
        else:
            print('Successfully created ' + path)

    elif args.command == "remove":
        path = os.path.join(work_folder, args.relative_path)
        path = os.path.normpath(path)
        remove_file(path,args.recursive)

    elif args.command == "copy":
        copy_file(args.source_path,args.dest_path,args.copy_tags,work_folder)

    elif args.command == "move":
        move_file(args.source_path,args.dest_path,work_folder)

    elif args.command == "list":
        print(print_files(work_folder,args.tag_type))


print("Getting or creating work folder")
work_folder = get_or_create_work_dir()
print("Work folder is: " + work_folder)
print("Getting or creating tag data")
file_dict = get_or_create_tag_data()
file_list = list(file_dict.values())
file_paths = list(file_dict.keys())
print("Tag data creation successful")
print("Checking and updating any changes")
update_files(work_folder)
print("Checked for updates")
save_tag_data_from_dict(file_dict,tag_file)
main()
save_tag_data_from_dict(file_dict, tag_file)



