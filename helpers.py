import dropbox
import os
import re
import logging


# Check to see if path exists already
def does_path_exist(path, dbx):
    try:
        return dbx.files_get_metadata(path) is not None

    except dropbox.exceptions.ApiError as e:
        error_object = e.error

        if isinstance(error_object, dropbox.files.GetMetadataError) and error_object.is_path():
            base_error = error_object.get_path()

            if isinstance(base_error, dropbox.files.LookupError) and base_error.is_not_found():
                return False

            else:
                raise error_object

        else:
            raise error_object


# Create directory at path
def create_path_specific_dir(path, dbx):
    if re.search(r"\.[^.]*$", path) is not None:
        raise ValueError("Path needs to be a directory and not a file.")

    _ = dbx.files_create_folder(path)
    logging.info(f"Created directory at path: \"{path}\"")


# Retrieve directory contents
def get_dir_contents(directory, dbx):
    returned_content = []

    try:
        folder_contents = dbx.files_list_folder(directory)
    
    except dropbox.exceptions.ApiError as e:
        error_object = e.error

        if isinstance(error_object, dropbox.files.ListFolderError):
            base_error = error_object.get_path()

            if isinstance(base_error, dropbox.files.LookupError) and base_error.is_not_found():
                raise Exception(f"Dropbox cannot locate the object at path \"{directory}\".")

            else:
                raise base_error

        else:
            raise error_object

    dir_contents = folder_contents.entries
    while folder_contents.has_more:
        cursor = folder_contents.cursor
        folder_contents = dropbox.Dropbox.files_list_folder_continue(cursor)
        dir_contents += folder_contents.entries

    for file_obj in dir_contents:
        if isinstance(file_obj, dropbox.files.FileMetadata):
            returned_content.append(file_obj.name)

        else:
            logging.warn(f"The object type for \"{file_obj.name}\" is not supported.")

    return returned_content


# Move file from source folder to destination folder
def move_file(source_path, destination_path, dbx):
    dbx.files_move(source_path, destination_path)
    return dbx.files_get_metadata(destination_path).name
