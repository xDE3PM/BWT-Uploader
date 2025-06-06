import os
import json
import re, sys
import requests
from src.ia import console
from rich.table import Table
from rich.prompt import IntPrompt, Prompt
from src.metafile import MetaPath
from src.filepath import FilePathInfo

CATGROUPS = {
    1: ("Bollywood", [
        (119, "Bollywood-Untouched WEB-DLs"),
        (120, "Bollywood - 1080p WEB-Rips"),
        (188, "Bollywood - 720p WEB-Rips"),
        (115, "Bollywood-Untouched BluRay"),
        (118, "Bollywood-Remuxes BluRay"),
        (116, "Bollywood-1080p BluRay Rips"),
        (117, "Bollywood-720p BluRay Rips"),
        (124, "Bollywood-3D-Movies"),
        (121, "Bollywood-Untouched DVDs"),
        (122, "Bollywood-DVDRips 1080p/720p"),
        (189, "Bollywood-Encoded DVDs"),
        (123, "Bollywood - SDRips - WEB/DVD"),
        (114, "Bollywood-4K Ultra HD / Upscal"),
        (190, "Bollywood-Movie Packs"),
        (113, "Bollywood-Pre-Release"),
        (125, "Bollywood- Web Series"),
    ]),
    2: ("Hollywood", [
        (131, "Hollywood-Untouched WEB-DLs"),
        (132, "Hollywood-1080p WEB-Rips"),
        (192, "Hollywood - 720p WEB-Rips"),
        (127, "Hollywood-Untouched BluRay"),
        (130, "Hollywood-BluRay Remuxes"),
        (128, "Hollywood-1080p BluRay Rips"),
        (129, "Hollywood-720p BluRay Rips"),
        (135, "Hollywood-3D-Movies"),
        (133, "Hollywood-Untouched DVDs"),
        (134, "Hollywood-DVDRips 1080p/720p"),
        (191, "Hollywood-Encoded DVDs"),
        (193, "Hollywood- SDRips - WEB/DVD"),
        (126, "Hollywood-4K Ultra HD / Upscal"),
        (194, "Hollywood - Movie Packs"),
        (136, "Hollywood-Pre-Release"),
    ]),
    3: ("Tamil", [
        (210, "Tamil-Untouched WEB-DLs"),
        (211, "Tamil-1080p/720p WEBRips"),
        (212, "Tamil-Untouched BluRay"),
        (217, "Tamil-Remuxes BluRay"),
        (216, "Tamil-BluRay Rips"),
        (213, "Tamil-Untouched DVDs"),
        (214, "Tamil-SD-WEBRips / DVDRips"),
        (209, "Tamil-4K Ultra HD - Upscaled"),
        (215, "Tamil-Movie Packs"),
    ]),
    4: ("Telugu", [
        (200, "Telugu-Untouched WEB-DLs"),
        (201, "Telugu-1080p/720p WEBRips"),
        (202, "Telugu-Untouched BluRay"),
        (208, "Telugu-Remuxes BluRay"),
        (207, "Telugu-BluRay Rips"),
        (203, "Telugu-Untouched DVDs"),
        (204, "Telugu-SD-WEBRips / DVDRips"),
        (199, "Telugu-4K Ultra HD - Upscaled"),
        (205, "Telugu-Movie Packs"),
    ]),
    5: ("Hindi Dubbed", [
        (184, "South Hindi Dubbed"),
        (183, "English Movies Hindi Dubbed"),
        (197, "Turkish Hindi Dubbed"),
    ]),
     6: ("Regional", [
        (145, "Bangla-Movies"),
        (143, "Bhoipuri-Movies"),
        (185, "Gujarati-Movies"),
        (141, "Kannada-Movies"),
        (142, "Lollywood-Movies"),
        (137, "Malayalam-Movies"),
        (144, "Marathi-Movies"),
        (140, "Punjabi-Movies"),
    ]),
    7: ("TV Series", [
        (125, "Bollywood- Web Series"),
        (157, "TV-Hollywood"),
        (147, "TV - &Tv"),
        (146, "TV-Colors"),
        (221, "TV-JioTv"),
        (148, "TV-Life OK"),
        (198, "TV-MTV"),
        (158, "TV-Others"),
        (195, "TV-Packs"),
        (149, "TV-Pakistani Dramas"),
        (150, "TV-Sab TV"),
        (151, "TV-Sony"),
        (155, "TV-Sports"),
        (152, "TV-Star Bharat"),
        (153, "TV-Star Plus"),
        (154, "TV-Zee TV"),
        (156, "TV-Documentary"),
        (218, "TV-Ishara TV"),
        (219, "TV-Bengali"),
        (220, "TV-Shemaroo Umang"),
    ]),
    8: ("Music", [
        (196, "Music Packs"),
        (160, "Music-Classical"),
        (161, "Music-Flacs"),
        (162, "Music-Ghazals"),
        (163, "Music-Hindi OSTs"),
        (164, "Music-Instrumental"),
        (165, "Music-Kannada Music"),
        (166, "Music-Lollywood Music"),
        (167, "Music-Malayalam Music"),
        (168, "Music-Marathi Music"),
        (170, "Music-Pop-Music"),
        (171, "Music-Punjabi-Music"),
        (172, "Music-Remix"),
        (173, "Music-Tamil Music"),
        (174, "Music-Telugu Music"),
        (169, "Music-Videos"),
    ])
}

class BWTorrentUploader:
    def __init__(self):
        self.m_path = MetaPath()
        self.meta_path = self.m_path.get_metapath()
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.filepath = self.fmeta.get('filepath')
        self.torrent_path = self.fmeta.get('torrent_path')
        self.upload_folder = self.fmeta.get('upload_folder')
        self.base_url = "https://bwtorrents.tv"
        self.filename = self.fmeta.get('filename_noext')
        
    def load_metadata(self):
        bbcode_path = os.path.join(self.upload_folder, "[BBCode]Torrent_Description.txt")
        with open(self.meta_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        imdb_link = metadata.get("imdb", {}).get("link", "")
        youtube_link = metadata.get("trailer", {}).get("url", "")
        name = metadata.get("FilePathInfo", {}).get("filename_noext", "")
        poster = metadata.get("tmdb", {}).get("poster") or metadata.get("imdb", {}).get("poster", "")
        category_id = metadata.get("catagory_id") or self.select_category()
        request = metadata.get("request")
        double_upload = metadata.get("doubleupload")
        recomanded = metadata.get("recomanded")

        with open(bbcode_path, 'r', encoding='utf-8') as f:
            description = f.read()

        return {
            "imdb_link": imdb_link,
            "youtube_link": youtube_link,
            "name": name,
            "poster": poster,
            "category_id": category_id,
            "request": request,
            "double_upload": double_upload,
            "recomanded": recomanded,
            "description": description
        }

    def freeleech_check(self, folder_path):
        """
        Check if the total size of files in the given path exceeds 10 GB for freeleech eligibility.
        
        Args:
            folder_path (str): Path to the file or folder to check.
        
        Returns:
            str: '1' if total size >= 10 GB (freeleech), '0' otherwise.
        """
        total_size_gb = 0.0
        
        # Check if the path exists
        if not os.path.exists(folder_path):
            console.print(f"[bold red]Error:[/bold red] Path does not exist: {folder_path}")
            return '0'
        
        # If it's a single file, calculate its size
        if os.path.isfile(folder_path):
            try:
                total_size_gb = os.path.getsize(folder_path) / (1024 ** 3)
                console.print(f"[bold cyan]File Size:[/bold cyan] {total_size_gb:.2f} GB for {folder_path}")
            except OSError as e:
                console.print(f"[bold red]Error:[/bold red] Could not read file size for {folder_path}: {e}")
                return '0'
        # If it's a directory, sum the sizes of all files
        else:
            try:
                for dirpath, dirnames, filenames in os.walk(folder_path):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        try:
                            if os.path.exists(file_path):
                                total_size_gb += os.path.getsize(file_path) / (1024 ** 3)
                        except OSError as e:
                            console.print(f"[bold red]Error:[/bold red] Could not read size for {file_path}: {e}")
                            continue
                console.print(f"[bold cyan]Total Size:[/bold cyan] {total_size_gb:.2f} GB for folder {folder_path}")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] Failed to scan folder {folder_path}: {e}")
                return '0'
        
        # Return '1' for freeleech if size >= 10 GB, '0' otherwise
        freeleech = '1' if total_size_gb >= 10 else '0'
        console.print(f"[bold green]Freeleech Status:[/bold green] {freeleech} (Size: {total_size_gb:.2f} GB)")
        return freeleech

    def select_category(self):
        console.print("\n[bold cyan]Select a Main Category:[/bold cyan]")
        for group_id, (name, _) in CATGROUPS.items():
            console.print(f" [bold yellow]{group_id}[/bold yellow]. {name}")

        group_choice = IntPrompt.ask("\nEnter category number", choices=[str(i) for i in CATGROUPS])
        group_name, subcats = CATGROUPS[group_choice]
        console.print("\n")
        table = Table(title=f"{group_name} Categories", header_style="bold magenta")
        table.add_column("No.", width=4)
        table.add_column("Category Name", style="bold")
        table.add_column("Code", style="green", justify="right")

        for i, (code, name) in enumerate(subcats, 1):
            table.add_row(str(i), name, str(code))

        console.print(table)

        sub_choice = IntPrompt.ask("\nEnter subcategory number", choices=[str(i) for i in range(1, len(subcats)+1)])
        selected_code, selected_name = subcats[sub_choice - 1]

        console.print(f"\n[bold green]Selected:[/bold green] {selected_name}")
        console.print(f"[bold blue]Category Code:[/bold blue] {selected_code}\n")

        return selected_code

    def load_cookies(self):
        cookie_path = "data/cookies/BWT.txt"
        cookies = {}
        with open(cookie_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip() or line.startswith('#'):
                    continue
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    cookies[parts[5]] = parts[6]
        return cookies

    def upload(self):
        filepath = self.filepath
        torrent_path = self.torrent_path
        meta = self.load_metadata()
        cookies = self.load_cookies()
        freeleech = self.freeleech_check(filepath)

        data = {
            'name': meta['name'],
            'descr': meta['description'],
            'type': meta['category_id'],
        }

        if meta.get('imdb_link'):
            data['imdb_link'] = meta['imdb_link']
        if meta.get('poster'):
            data['poster'] = meta['poster']
        if meta.get('youtube_link'):
            data['tube'] = meta['youtube_link']
        if meta.get('request') is True:
            data['request'] = 'yes'
        if meta.get('request') is False:
            data['request'] = 'no'
        if meta.get('double_upload') is True:
            data['double_upload'] = '1'
        if meta.get('recomanded') is True:
            data['recomanded'] = '1'
        if freeleech == '1':
            data['free'] = '1'

        print(data)
        
        confirm = Prompt.ask("[bold] Continue to Upload This?", choices=["y", "N"], case_sensitive=False) 
        if confirm.lower() != "y":
            console.print("[red]Exiting...[/red]")
            sys.exit(0)
            
        with open(torrent_path, 'rb') as torrent_file:
            files = {'file': torrent_file}
            response = requests.post(f"{self.base_url}/takeupload.php", cookies=cookies, files=files, data=data)

        console.print(f"\n[bold cyan]Status Code:[/bold cyan] {response.status_code}\n")
        
        if response.status_code == 200:
            match = re.search(r'details\.php\?id=(\d+)&filelist', response.text)
            if match:
                torrent_id = match.group(1)
                torrent_url = f"{self.base_url}/details.php?id={torrent_id}"
                console.print(
                    f"[bold green]Torrent Uploaded Successfully![/bold green]\n\n"
                    f"[bold]Torrent Name:[/bold] {self.filename}\n"
                    f"[bold]Torrent ID:[/bold] {torrent_id}\n"
                    f"[bold]Torrent URL:[/bold] [blue underline]{torrent_url}[/blue underline]"
                )
            else:
                console.print("[bold yellow]Upload succeeded but no torrent ID was found.[/bold yellow]")
        else:
            console.print(f"[bold red]Upload Failed![/bold red]")
            console.print(f"[dim]{response.text}[/dim]")
