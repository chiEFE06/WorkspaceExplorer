import os
import xml.etree.ElementTree as ET
import pickle
from data import FileTag
from data import FolderTag
import sys

data_file = "user_data.xml"
tag_file = "tag_data.pkl"

def get_work_dir_from_xml():
    #Reads the work directory from user_data.xml.
    tree = ET.parse(data_file)
    root = tree.getroot()
    work_dir = root.find("work_dir").text
    return work_dir

def create_user_data_xml(work_dir):
    #Creates the XML file with the work directory
    root = ET.Element("user_data")
    ET.SubElement(root, "work_dir").text = work_dir
    tree = ET.ElementTree(root)
    tree.write(data_file)

def get_or_create_work_dir():
    #Main function to either get from XML or prompt and save
    if os.path.exists(data_file):
        try:
            work_dir = get_work_dir_from_xml()
            if os.path.isdir(work_dir):
                return work_dir
            else:
                print("Saved directory is invalid. Please enter a new one.")
        except Exception as e:
            print("Failed to read user_data.xml:", e)

    # If XML doesn't exist or is invalid, prompt user
    while True:
        work_dir = input("Enter work directory: ").strip()
        if os.path.isdir(work_dir):
            create_user_data_xml(work_dir)
            return work_dir
        else:
            print("Invalid directory. Try again.")

def dump_folder_tag(folder_obj,save_file):
    # Creates the pkl file with given FolderTag class object.
    with open(save_file, "wb") as f:
        pickle.dump(folder_obj, f)

def read_pickle(save_file):
    # Reads the tag data from tag_data.pkl.
    with open(save_file, "rb") as f:
        loaded_obj = pickle.load(f)
        return loaded_obj

def get_or_create_folder_tag():
    # Initial method to either read or store FolderTag object
    if os.path.exists(tag_file):
        try:
            root_folder = read_pickle(tag_file)
            return root_folder
        except Exception as e:
            print("Failed to read tag data", e)

    root_folder = FolderTag(work_folder)
    dump_folder_tag(root_folder, tag_file)
    return root_folder

def create_directory(folder_path,work_dir):
    folder_path=os.path.join(work_dir,folder_path)
    try:
        os.mkdir(folder_path)
    except OSError as e:
        print("Failed to create directory", e)

def remove_file(file_path,work_dir,use_folder=False):
    file_path = os.path.join(work_dir, file_path)
    if use_folder:
        os.rmdir(file_path)
    else:
        os.remove(file_path)



work_folder = get_or_create_work_dir()
root_folder = get_or_create_folder_tag()

print(root_folder.print_files())

root_folder.search_for_file("YAY.txt")


