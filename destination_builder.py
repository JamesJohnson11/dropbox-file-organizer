import datetime
import re
import config
import logging

class DestinationBuilder(object):

    def __init__(self, files, category_to_path_map):

        self.category_to_path_map = category_to_path_map
        self.files = files
        self.source_to_dest_map = {}

        self.file_date = (datetime.datetime.today().strftime("%Y%m%d"))[2:]


    def _get_destination_path_elements(self, file_name):
        regex = re.search(r"\.[^.]*$", file_name)
        if regex:
            ext = regex.group(0)
            output_file_name = file_name[:file_name.rfind(ext)].split(" ")
        
        else:
            ext = ""
            output_file_name = file_name.split(" ")

        destination = output_file_name.pop(0).lower()

        dest_directory_str = self.category_to_path_map.get(destination)
        if dest_directory_str is None:
            raise PathKeyDoesNotExist(destination)

        name = "-".join(output_file_name)
        return dest_directory_str, name, ext


    # Generate destination file paths for source files
    def generate_dest_paths(self):
        if not self.source_to_dest_map:
            logging.info("Generating destination paths...")

            for file in self.files:
                try:
                    directory, name, ext = self._get_destination_path_elements(file)
                    full_source_path = f"{config.SOURCE_DIR}/{file}"
                    self.source_to_dest_map[full_source_path] = f"{directory}/{self.file_date}_{name}{ext}"

                except PathKeyDoesNotExist as e:
                    logging.warn(e.error)
                    continue

            logging.info(f"{len(self.files)} paths generated.")

        return self.source_to_dest_map


class PathKeyDoesNotExist(Exception):

    def __init__(self, _key=None, error=None):
        if not error:
            error = f"The key, \"{_key}\", for the specified file does not exist. " 
            "define this key and destination in the config file."
        self.error = error