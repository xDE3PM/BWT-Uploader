import os
import sys
from src.ia import console
from rich.prompt import Prompt
from src.exit import error_exit

def print_audio_list(audio_folder, max_files=20):
    file_count = 0
    for root, dirs, files in os.walk(audio_folder):
        if file_count >= max_files:
            break
        if files:
            folder_name = os.path.basename(root)
            console.print(f"[bold yellow]➥ {folder_name}")
            for file in sorted(files):
                if file_count >= max_files:
                    break
                file_path = os.path.join(root, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                console.print(f"  [bold]└─ {file} ({size_mb:.2f} MiB)")
                file_count += 1

def mdprint(meta):
    video_media = meta.get("video_media")
    audio_music = meta.get("audio_music") 

    imdb = meta.get("imdb", {})
    tmdb = meta.get("tmdb", {})

    # VIDEO MEDIA BLOCK
    if video_media:
        if not tmdb and not imdb:
            console.print("[bold red]Skipping TMDb or IMDb Database Details.[/bold red]\n")
            confirm = Prompt.ask("[bold]Continue to Upload this?", choices=["y", "N"], case_sensitive=False)
            if confirm.lower() != "y":
                error_exit()
            return

        console.print("\n[bold cyan]──────────────────── Database Info ────────────────────[/bold cyan]\n")

        # Title
        title = tmdb.get('title') or imdb.get('title', 'N/A')
        year = tmdb.get('year') or imdb.get('year', 'N/A')
        console.print(f"[bold yellow]Title:[/bold yellow] {title} ({year})\n")

        # Overview
        overview = tmdb.get('overview') or imdb.get('plot', 'N/A')
        console.print(f"[bold green]Overview:[/bold green] {overview}\n")

        # Genre
        genres = ", ".join(tmdb.get('genres') or imdb.get('genres', [])) or "N/A"
        console.print(f"[bold magenta]Genre:[/bold magenta] {genres}\n")

        # Category
        category = imdb.get('type', 'N/A')
        console.print(f"[bold blue]Category:[/bold blue] {category}")

        # Ratings & Links
        imdb_rating = imdb.get('rating', 'N/A')
        imdb_link = imdb.get('link', 'N/A')
        console.print(f"\n[bold yellow]IMDb Rating:[/bold yellow] [bold]{imdb_rating}/10[/bold]")
        if tmdb:
            tmdb_rating = tmdb.get('rating', 'N/A')
            tmdb_link = tmdb.get('tmdb_link', 'N/A')
            console.print(f"[bold green]TMDb Rating:[/bold green] [bold]{tmdb_rating}/10[/bold]")
            console.print(f"\n[bold green]TMDb Link:[/bold green] {tmdb_link}")
        console.print(f"[bold yellow]IMDb Link:[/bold yellow] {imdb_link}\n")

        confirm = Prompt.ask("[bold]Is this Database information correct?", choices=["y", "N"], case_sensitive=False)
        if confirm.lower() != "y":
            error_exit()

    # AUDIO MUSIC BLOCK
    elif audio_music:
        audio_folder = meta.get("filepath")
        print_audio_list(audio_folder)
        print()
        confirm = Prompt.ask("[bold]Do you want to upload this music album?", choices=["y", "N"], case_sensitive=False)
        if confirm.lower() != "y":
            error_exit()
