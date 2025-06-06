import os
import requests
from bs4 import BeautifulSoup
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
        self.media_info_path_2 = os.path.join(self.upload_folder, "Media_Info.txt")
        self.screenshot_links = os.path.join(self.upload_folder, "screenshots/uploaddata/bbcode_medium.txt")
        self.cookie_file = 'data/cookies/katb.txt'

    def load_cookies(self, session):
        with open(self.cookie_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    parts = line.strip().split('\t')
                    if len(parts) >= 7:
                        domain, _, path, _, _, name, value = parts[:7]
                        session.cookies.set(name, value, domain=domain, path=path)

    def upload_mediainfo_to_katb(self, mediainfo_path):
        session = requests.Session()
        self.load_cookies(session)

        try:
            with open(mediainfo_path, 'r', encoding='utf-8') as f:
                text_to_share = f.read()
        except Exception as e:
            console.print(f"[bold red]Error reading MediaInfo file:[/bold red] {e}")
            return None

        url = 'https://katb.in/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_input = soup.find('input', {'name': '_csrf_token'})
            if not csrf_input:
                console.print("[bold red]CSRF token not found.[/bold red]")
                return None
            csrf_token = csrf_input['value']

            data = {
                'paste[content]': text_to_share,
                '_csrf_token': csrf_token
            }

            response = session.post(url, data=data, headers=headers)
            if response.status_code == 200:
                return response.url
            else:
                console.print(f"[bold red]Failed to upload to Katb.in. Status code:[/bold red] {response.status_code}")
                return None
        else:
            console.print(f"[bold red]Failed to connect to Katb.in. Status code:[/bold red] {response.status_code}")
            return None

    def generate(self, more_backdrop_link):
        if os.path.exists(self.description_bbcode_path):
            return
            
        with open(self.screenshot_links, 'r', encoding="utf-8") as f:
            screenshot_bbcode = f.read().strip()

        media_info_file = self.media_info_path_2
        custom_media_info_file = self.media_info_path
        with open(custom_media_info_file, "r", encoding="utf-8") as f:
            mediainfo = f.read().strip()

        console.print(f"[bold cyan]\n TMDb Backdrop Images:[/bold cyan] {more_backdrop_link}")
        movie_poster_url = Prompt.ask("[bold cyan] Enter Backdrop poster URL:[/bold cyan]")
        
        # Upload MediaInfo and get URL
        mediainfo_url = self.upload_mediainfo_to_katb(media_info_file)
       # mediainfo_url = "https://katb.in/wafahumokoy"
        
        if not mediainfo_url: 
            mediainfo_url = Prompt.ask("[bold cyan] Enter Mediainfo URL:[/bold cyan]")
            
        file_name = os.path.basename(self.file_info.video_path).strip()

        mediainfo = mediainfo.replace('★ General ★', '[quote]\n[b][color=green]★ General ★[/color][/b]\n[font=Courier New]')
        mediainfo = mediainfo.replace('★ Video Track ★', '[/font]\n\n[b][color=blue]★ Video Track ★[/color][/b]\n[font=Courier New]')
        mediainfo = mediainfo.replace('★ Audio Track ★', '[/font]\n\n[b][color=orange]★ Audio Track ★[/color][/b]\n[font=Courier New]')
        mediainfo = mediainfo.replace('★ Subtitle ★', '[/font]\n\n[b][color=teal]★ Subtitle ★[/color][/b]\n[font=Courier New]')
        mediainfo += '\n[/font]\n[/quote]'

        new_content = textwrap.dedent(BBCODE_TEMPLATE).format(
            movie_poster_url=movie_poster_url,
            file_name=file_name,
            mediainfo=mediainfo,
            mediainfo_url=mediainfo_url,
            screenshot_bbcode=screenshot_bbcode
        )
        with open(self.description_bbcode_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            f.write('[b][center][url=https://github.com/xDE3PM/BWT-Uploader][color=RoyalBlue]Created by BWT-Uploader[/color][/url][/center][/b]\n')
