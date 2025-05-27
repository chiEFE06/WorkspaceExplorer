# Workspace Explorer

Workspace Explorer is a tag based file explorer app. It is console based and can help with organizing a certain work folder with the help of tags.
Each file is given a single main tag, and can be tagged with multiple sub-tags.

## Usage
On initial launch, the program will ask for work folder to tag in. After discovering all files in subdirectories it will ask for a main tag for each file. This step is skip able, however the program will ask to fill in the missing tag on each launch. To prevent that, the user can input ignore as the main tag.
The program only accepts paths relative to the work directory first chosen. 
All the M/S arguments below symbolise the tag type, maintag and subtag respectively.

| Command   | Description                                                    | Usage                                          | Arguments                                                                                                                                                                                               |
|-----------|----------------------------------------------------------------|------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Search    | Searches for a tag inside the work folder                      | search (-R relative_path) M/S tag              | -R: limits the command to the given relative directory instead of the whole work folder.                                                                                                                |
| addtag    | Adds a tag to a file                                           | addtag (-R) relative_path M/S tag              | -R: runs the command for all the files in the given folder, instead for only a single file.                                                                                                             |
| removetag | Removes tag(s) from a file                                     | removetag (-R) relative_path M/S (-t tag)      | -R: runs the command for all the files in the given folder, instead for only a single file. -t: Specifies a tag to be removed. If it's not given, the command will will erase all the matching tag_type |
| edittag   | Changes a tag from a file with a new one                       | edittag (-R) relative_path M/S new_tag old_tag | -R: runs the command for all the files in the given folder, instead for only a single file.                                                                                                             |
| mkdir     | Creates a folder                                               | mkdir relative_path                            | None                                                                                                                                                                                                    |
| remove    | Removes file(s) along with their tag data                      | remove (-R) relative_path                      | -R: runs the command for all the files in the given folder, instead for only a single file.                                                                                                             |
| help      | Built-in python module to display commands and their arguments | -h or 'command' -h                             | None                                                                                                                                                                                                    |



Project was written on Python 3.13
