##############################################
# BWT-Uploader v1.0.0 - Created by -=DE3PM=- #
##############################################

from src.ia import console
from rich.prompt import Prompt
import sys

from src.args import Args
from src.filepath import FilePathInfo
from src.database import get_details
from src.create import Torrent
from src.miextractor import MediaInfoExtractor
from src.screens import Screens
from src.uph import mdprint
from src.exit import error_exit
from src.descr import Description
from src.tracker.BWT import BWTorrentUploader
from src.version import version, author
from src.checkupdate import VersionChecker


def main():
    console.print()
    console.rule(f"[bold magenta]🚀 BWT-Uploader [bold yellow]v{version} [bold green]- Created by [bold red]-={author}=-", style="bold cyan")
    console.print()

    # Check for updates
    checker = VersionChecker()
    checker.check_for_updates()

    # Load CLI arguments
    args = Args()
    meta_args = args.gmeta()

    if not meta_args or not meta_args.get("filepath"):
        console.print("[bold red]Error: Filepath is required.[/bold red]")
        error_exit()

    # File Info
    file_info = FilePathInfo()
    meta = file_info.process()

    filename = meta["filename"]
    video_media = meta.get("video_media", False)
    audio_music = meta.get("audio_music", False)
    skip_tmdb = meta.get("skip_tmdb", False)
    skip_imdb_tmdb = meta.get("skip_imdb_tmdb", False)

    console.print(f"[bold cyan]File Name:[/bold cyan] {filename}\n")

    # Get metadata (IMDB/TMDB)
    if video_media:
        details = get_details()
        mdprint(details)
    elif audio_music:
        mdprint(meta)

    # Create torrent
    torrent = Torrent()
    torrent.create()

    if video_media:
        mi = MediaInfoExtractor()
        mi.video_process()
        
    # Initialize poster URL as None
    movie_poster_url = None

    # Screenshots and poster selection (only for video)
    if video_media:
        manager = Screens()
        manager.generate_screenshots()
        manager.upload_images()

        if not movie_poster_url and not skip_imdb_tmdb:
            if not skip_tmdb:
                movie_poster_url = details.get("tmdb", {}).get("poster")
                if not movie_poster_url:
                    movie_poster_url = details.get("imdb", {}).get("poster")
            else:
                movie_poster_url = details.get("imdb", {}).get("poster")

        if not movie_poster_url:
            movie_poster_url = Prompt.ask("[bold]Enter your poster URL:[/bold]")

    # Description generation
    description = Description()
    description.generate(movie_poster_url if video_media else None)

    # Upload to BWT
    bwtup = BWTorrentUploader()
    bwtup.upload()

if __name__ == "__main__":
    main()

##############
# -= DE3PM=- #
##############
