import os
from os.path import join, dirname
import datetime
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(find_dotenv())

TOKEN = os.environ.get('TOKEN')

SOURCE_DIR = '/Desktop/drop-file-org/source'
DEST_DIR = '/Desktop/drop-file-org/destination/'

BASE_DEST_PATH = f"{DEST_DIR}{datetime.datetime.now().year}"

RECEIPTS = "receipts"
VIDEOS = "videos"
MUSIC = "music"

CATEGORY_TO_PATH_MAP = {
    RECEIPTS: f"{BASE_DEST_PATH} Receipts",
    VIDEOS: f"{BASE_DEST_PATH} Videos",
    MUSIC: f"{BASE_DEST_PATH} Music",
}