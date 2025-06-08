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

def main():
    console.rule(f"[bold magenta]🚀 BWT-Uploader [bold yellow]v{version} [bold green]- Created by [bold red]-={author}=-", style="bold cyan")
    args = Args()
    meta_args = args.gmeta()

    if not meta_args or not meta_args.get("filepath"):
        console.print("[bold red]Error: Filepath is required.[/bold red]")
        sys.exit(1)

    file_info = FilePathInfo()
    meta = file_info.process()
    filename = meta["filename"]
    console.print(f"\n[bold cyan]File Name:[/bold cyan] {filename}\n")
    details = get_details()
    
    mdprint(details)
    confirm = Prompt.ask("[bold]Is this Database information correct?", choices=["y", "N"], case_sensitive=False) 
    if confirm.lower() != "y":
        console.print("[red]Exiting...[/red]")
        sys.exit(0)
    torrent = Torrent()
    torrent.create()
    generator = MediaInfoGenerator()
    generator.generate_media_info()
    manager = Screens()
    manager.generate_screenshots()
    manager.upload_images()
    movie_poster_url = details["tmdb"]["poster"] or details["imdb"]["poster"]
    if not movie_poster_url:
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
