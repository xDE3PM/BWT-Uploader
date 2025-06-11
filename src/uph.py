import sys
from src.ia import console
from rich.prompt import Prompt

def mdprint(meta):
    imdb = meta.get("imdb", {})
    tmdb = meta.get("tmdb", {})

    # Check if both tmdb and imdb details are empty
    if not tmdb and not imdb:
        console.print("[bold red]Skipping TMDb or IMDb Database Details.[/bold red]\n")
        confirm = Prompt.ask("[bold]Continue to Upload this?", choices=["y", "N"], case_sensitive=False)  
        if confirm.lower() != "y":
            console.print("[red]Exiting...[/red]")
            sys.exit(0)
        return

    console.print("\n[bold cyan]──────────────────── Database Info ────────────────────[/bold cyan]\n")

    # Title
    if tmdb.get('title') and tmdb.get('year'):
        title = tmdb.get('title')
        year = tmdb.get('year')
    else:
        title = imdb.get('title', 'N/A')
        year = imdb.get('year', 'N/A')
    console.print(f"[bold yellow]Title:[/bold yellow] {title} ({year})\n")

    # Overview
    if tmdb.get('overview'):
        overview = tmdb.get('overview')
    else:
        overview = imdb.get('plot', 'N/A')
    console.print(f"[bold green]Overview:[/bold green] {overview}\n")

    # Genre
    if tmdb.get('genres'):
        genres = ", ".join(tmdb.get('genres', [])) or "N/A"
    else:
        genres = ", ".join(imdb.get('genres', [])) or "N/A"
    console.print(f"[bold magenta]Genre:[/bold magenta] {genres}\n")

    # Category
    category = imdb.get('type', 'N/A') 
    console.print(f"[bold blue]Category:[/bold blue] {category}")

    # TMDB & IMDB
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
        console.print("[red]Exiting...[/red]")
        sys.exit(0)

