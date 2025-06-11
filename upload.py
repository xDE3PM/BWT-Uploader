##############################################
# BWT-Uploader v1.0.0 - Created by -=DE3PM=- #
##############################################

from src.ia import console
from rich.prompt import Prompt
from rich.panel import Panel
import sys

from src.args import Args
from src.filepath import FilePathInfo
from src.database import get_details
from src.create import Torrent
from src.minfo import MediaInfoGenerator
from src.screens import Screens
from src.uph import mdprint
from src.descr import Description
from src.tracker.BWT import BWTorrentUploader
from src.version import version, author
from src.checkupdate import VersionChecker

def main():
    console.rule(f"[bold magenta]🚀 BWT-Uploader [bold yellow]v{version} [bold green]- Created by [bold red]-={author}=-", style="bold cyan")
    checker = VersionChecker()
    checker.check_for_updates()
    args = Args()
    meta_args = args.gmeta()

    if not meta_args or not meta_args.get("filepath"):
        console.print("[bold red]Error: Filepath is required.[/bold red]")
        sys.exit(1)

    file_info = FilePathInfo()
    meta = file_info.process()
    filename = meta["filename"]
    skip_tmdb = meta.get("skip_tmdb", False)
    skip_imdb_tmdb = meta.get("skip_imdb_tmdb", False)
    console.print(f"\n[bold cyan]File Name:[/bold cyan] {filename}\n")
    details = get_details()
    mdprint(details)
    torrent = Torrent()
    torrent.create()
    generator = MediaInfoGenerator()
    generator.generate_media_info()
    manager = Screens()
    manager.generate_screenshots()
    manager.upload_images()
    
    if skip_imdb_tmdb is False:
         if skip_tmdb is False:
             movie_poster_url = details["tmdb"]["poster"] 
         else:
             movie_poster_url = details["imdb"]["poster"]
    else:
        movie_poster_url = Prompt.ask("[bold]Enter your poster URL:")
        
    description = Description()
    description.generate(movie_poster_url)
    bwtup = BWTorrentUploader()
    bwtup.upload()

    console.print("\n[bold green]Upload process completed successfully![/bold green]")

if __name__ == "__main__":
    main()

##############
# -= DE3PM=- #
##############
