import dropbox
import config
import logging
import dropbox
import helpers
import destination_builder

logging.basicConfig(level=logging.INFO)


def main(dbx):
    # Retrieve contents from source
    source_files = helpers.get_dir_contents(config.SOURCE_DIR, dbx)
    logging.info(f"Retrieved {len(source_files)} files.")

    # Ensure all destination dir exists
    for dest_dir in config.CATEGORY_TO_PATH_MAP.values():
        # If destination directory doesn't exist, create it
        if not helpers.does_path_exist(dest_dir, dbx):
            logging.info(f"The directory \"{dest_dir}\" does not exist.")
            helpers.create_path_specific_dir(dest_dir, dbx)


    # Map source files to destination
    source_to_dest_map = destination_builder.DestinationBuilder(source_files, config.CATEGORY_TO_PATH_MAP).generate_dest_paths()


    # Move source files to destination
    moved_files = []
    for source, dest in source_to_dest_map.items():
        moved_files.append((helpers.move_file(source, dest, dbx), source, dest))

    logging.info(f"Execution complete. The following {len(moved_files)} files were moved:")
    for f in moved_files:
        logging.info(f"\tMoved {f[0]} from \"{f[1]}\" to \"{f[2]}\"")

if __name__ == '__main__':
    with dropbox.Dropbox(oauth2_access_token=config.TOKEN) as dbx:
        main(dbx)