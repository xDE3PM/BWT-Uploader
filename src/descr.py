import os
import textwrap
from data.config import BBCODE_TEMPLATE
from src.filepath import FilePathInfo
from src.ia import console
from src.miextractor import MediaInfoExtractor

class Description:
    def __init__(self):
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.upload_folder = self.fmeta.get('upload_folder')
        self.filename = self.fmeta.get('filename')

        self.description_bbcode_path = os.path.join(self.upload_folder, "[BBCode]Torrent_Description.txt")
        self.screenshot_links = os.path.join(self.upload_folder, "screenshots/uploaddata/bbcode_medium.txt")

    def generate(self, movie_poster_url=""):
        mi = MediaInfoExtractor()

        # VIDEO / DVD / BLURAY path
        if self.fmeta.get("video_media") or self.fmeta.get("raw_dvd") or self.fmeta.get("raw_bluray"):
            if not os.path.isfile(self.screenshot_links):
                console.print(f"[bold red]❌ Screenshot BBCode file missing:[/bold red] {self.screenshot_links}")
                return

            media_bbcode = mi.gen_video_info()
            with open(self.screenshot_links, 'r', encoding="utf-8") as f:
                screenshot_bbcode = f.read().strip()

            # Use full template
            content = textwrap.dedent(BBCODE_TEMPLATE).format(
                movie_poster_url=movie_poster_url,
                file_name=self.filename,
                media_info=media_bbcode,
                screenshot_bbcode=screenshot_bbcode
            )

            with open(self.description_bbcode_path, "w", encoding="utf-8") as f:
                f.write(content)
                f.write(
                    "\n[center][font=Arial][size=4][b]"
                    "[url=https://github.com/xDE3PM/BWT-Uploader]"
                    "[color=#FF0000]Created by BWT-Uploader[/color][/url][/b][/size][/font][/center]\n"
                )

            return

        # AUDIO MUSIC path
        if self.fmeta.get("audio_music"):
            audio_bbcode = mi.gen_audio_info()
            with open(self.description_bbcode_path, "w", encoding="utf-8") as f:
                f.write(audio_bbcode)
                f.write(
                    "\n\n[center][font=Arial][size=4][b]"
                    "[url=https://github.com/xDE3PM/BWT-Uploader]"
                    "[color=#FF0000]Created by BWT-Uploader[/color][/url][/b][/size][/font][/center]\n"
                )
                
            return
           
