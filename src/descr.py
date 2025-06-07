import os
import requests
import textwrap
from data.config import BBCODE_TEMPLATE
from src.filepath import FilePathInfo
from src.ia import console
from rich.prompt import Prompt

class Description:
    def __init__(self):
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.upload_folder = self.fmeta.get('upload_folder')
        self.description_bbcode_path = os.path.join(self.upload_folder, "[BBCode]Torrent_Description.txt")
        self.media_info_path = os.path.join(self.upload_folder, "Custom_Media_Info.txt")
        self.screenshot_links = os.path.join(self.upload_folder, "screenshots/uploaddata/bbcode_medium.txt")
        
    def generate(self, more_backdrop_link):
        if os.path.exists(self.description_bbcode_path):
            return

        with open(self.screenshot_links, 'r', encoding="utf-8") as f:
            screenshot_bbcode = f.read().strip()

        with open(self.media_info_path, "r", encoding="utf-8") as f:
            mediainfo = f.read().strip()

        # 🔹 Remove the line before "★ Subtitle ★"
        lines = mediainfo.splitlines()
        cleaned_lines = []
        for i in range(len(lines)):
            if i + 1 < len(lines) and '★ Subtitle ★' in lines[i + 1]:
                continue
            cleaned_lines.append(lines[i])
        mediainfo = '\n'.join(cleaned_lines)

        # 🔹 Apply BBCode formatting
        mediainfo = mediainfo.replace(
            '★ General ★',
            '[quote]\n[b][color=green]★ General ★[/color][/b]\n[font=Courier New]'
        )
        mediainfo = mediainfo.replace(
            '★ Video Track ★',
            '[/font]\n\n[b][color=blue]★ Video Track ★[/color][/b]\n[font=Courier New]'
        )
        mediainfo = mediainfo.replace(
            '★ Audio Track ★',
            '[/font]\n\n[b][color=orange]★ Audio Track ★[/color][/b]\n[font=Courier New]'
        )
        mediainfo = mediainfo.replace(
            '★ Subtitle ★',
            '[/font]\n\n[b][color=teal]★ Subtitle ★[/color][/b]\n[font=Courier New]'
        )
        mediainfo += '\n[/font]\n[/quote]'

        console.print(f"[bold cyan]\n TMDb Backdrop Images:[/bold cyan] {more_backdrop_link}")
        movie_poster_url = Prompt.ask("[bold cyan] Enter Backdrop poster URL:[/bold cyan]")

        file_name = os.path.basename(self.file_info.video_path).strip()

        new_content = textwrap.dedent(BBCODE_TEMPLATE).format(
            movie_poster_url=movie_poster_url,
            file_name=file_name,
            screenshot_bbcode=screenshot_bbcode
        )

        with open(self.description_bbcode_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            f.write('[b][center][url=https://github.com/xDE3PM/BWT-Uploader][color=RoyalBlue]Created by BWT-Uploader[/color][/url][/center][/b]\n')
