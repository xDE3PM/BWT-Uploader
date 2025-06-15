import os
import requests
import textwrap
from data.config import BBCODE_TEMPLATE
from src.filepath import FilePathInfo
from src.ia import console
from rich.prompt import Prompt
from src.miextractor import MediaInfoExtractor

class Description:
    def __init__(self):
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.upload_folder = self.fmeta.get('upload_folder')
        self.filename_noext = self.fmeta.get('filename_noext')
        self.description_bbcode_path = os.path.join(self.upload_folder, "[BBCode]Torrent_Description.txt")
        self.media_info_path = os.path.join(self.upload_folder, "Custom_Media_Info.txt")
        self.screenshot_links = os.path.join(self.upload_folder, "screenshots/uploaddata/bbcode_medium.txt")
        
    def generate(self, movie_poster_url):
        if os.path.exists(self.description_bbcode_path):
            return

        with open(self.screenshot_links, 'r', encoding="utf-8") as f:
            screenshot_bbcode = f.read().strip()

        mi = MediaInfoExtractor()
        general, video, audio, subtitle, chapters = mi.get_custom_mediainfo()
        file_name = self.filename_noext

        new_content = textwrap.dedent(BBCODE_TEMPLATE).format(
            movie_poster_url=movie_poster_url,
            file_name=file_name,
            general_info=general,
            video_info=video,
            audio_info=audio,
            text_info=subtitle,
            chapters_info=chapters,
            screenshot_bbcode=screenshot_bbcode
        )

        with open(self.description_bbcode_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            f.write('[center][font=Arial][size=4][b][url=https://github.com/xDE3PM/BWT-Uploader][color=#FF0000]Created by BWT-Uploader[/color][/url][/b][/size][/font][/center]\n')
