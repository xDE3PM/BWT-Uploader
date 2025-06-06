from src.ia import console

def mdprint(meta):
    imdb = meta.get("imdb", {})
    tmdb = meta.get("tmdb", {})

    console.print("\n[bold cyan]──────────────────── Database Info ────────────────────[/bold cyan]\n")

    # Title
    title = f"{tmdb.get('title', 'N/A')} ({tmdb.get('year', 'N/A')})"
    console.print(f"[bold yellow]Title:[/bold yellow] {title}\n")

    # Overview
    overview = imdb.get("plot", "N/A")
    console.print(f"[bold green]Overview:[/bold green] {overview}\n")

    # Genre
    genres = ", ".join(imdb.get("genres", [])) or "N/A"
    console.print(f"[bold magenta]Genre:[/bold magenta] {genres}\n")

    # Category
    category = imdb.get("type", "N/A")
    if category == "movie":
        result = "MOVIE"
    elif category == "tv series":
        result = "TV Series"
    
    console.print(f"[bold blue]Category:[/bold blue] {result}")

    # TMDB & IMDB
    tmdb_link = tmdb.get("tmdb_link", "N/A")
    imdb_link = imdb.get("link", "N/A")
    console.print(f"\n[bold yellow]TMDb Link:[/bold yellow] {tmdb_link}")
    console.print(f"[bold green]IMDb Link:[/bold green] {imdb_link}\n")
