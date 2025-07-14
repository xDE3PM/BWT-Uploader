import os, json, sys
import requests
import subprocess
from guessit import guessit
from data.config import config
from src.metafile import MetaPath
from src.filepath import FilePathInfo
from src.ia import console
from rich.prompt import Prompt
from src.exit import error_exit

def search_imdb(filename, name, year, file_type):
    """
    Searches IMDb and returns the best matching IMDb ID based on name, year, and type.
    """
    BASE_URL = "https://rest.imdbapi.dev/v2"
    url = f"{BASE_URL}/search/titles"
    params = {"query": f"{name} {year}"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json().get("titles", [])

    best_match = None

    for movie in results:
        imdb_type = movie.get("type")
        start_year = movie.get("start_year")

        if file_type == "movie" and imdb_type == "movie":
            if year and str(start_year) == str(year):
                best_match = movie
                break
        elif file_type == "episode" and imdb_type in ["tvSeries", "tvMiniSeries"]:
            if year and start_year == year:
                best_match = movie
                break

    if not best_match and results:
        best_match = results[0]

    return best_match.get("id") if best_match else None

def get_imdb_details(imdbID):
    """
    Fetches full IMDb details by IMDb ID.
    """
    BASE_URL = "https://rest.imdbapi.dev/v2"
    url = f"{BASE_URL}/titles/{imdbID}"
    response = requests.get(url)
    response.raise_for_status()
    movie = response.json()

    return {
        "id": movie.get("id", imdbID),
        "title": movie.get("primary_title", "N/A"),
        "year": movie.get("start_year", "N/A"),
        "genres": movie.get("genres", []),
        "rating": movie.get("rating", {}).get("aggregate_rating", "N/A"),
        "plot": movie.get("plot", "N/A"),
        "poster": movie.get("primary_image", {}).get("url", "N/A"),
        "link": f"https://www.imdb.com/title/{imdbID}/",
        "type": movie.get("type", "N/A").upper()
    }

def search_tmdb(title, year, media_type, tmdb_api_key):
    
    def do_search(with_year):
        params = {
            "api_key": tmdb_api_key,
            "query": title,
            "language": "en-US",
            "include_adult": "false"
        }
        if with_year and year:
            key = "year" if media_type == "movie" else "first_air_date_year"
            params[key] = year
        url = f"https://api.themoviedb.org/3/search/{media_type}"
        return requests.get(url, params=params).json().get("results", [])

    results = do_search(True) or do_search(False)
    return results[0]["id"] if results else None
    
def get_tmdb_id(imdbID, tmdb_api_key):
    url = f"https://api.themoviedb.org/3/find/{imdbID}?api_key={tmdb_api_key}&external_source=imdb_id"
    data = requests.get(url).json()

    if data.get("movie_results"):
        return data["movie_results"][0]["id"]
    elif data.get("tv_results"):
        return data["tv_results"][0]["id"]
    return

def get_tmdb_details(tmdbID, media_type, tmdb_api_key):
    url = f"https://api.themoviedb.org/3/{media_type}/{tmdbID}"
    response = requests.get(url, params={"api_key": tmdb_api_key, "language": "en-US"})
    if response.status_code == 200:
        content = response.json()
        return {
            "id": tmdbID,
            "title": content.get("title") or content.get("name", "Unknown"),
            "year": (content.get("release_date") or content.get("first_air_date", ""))[:4],
            "genres": [g["name"] for g in content.get("genres", [])],
            "rating": round(content.get("vote_average", 0), 1) if content.get("vote_average") else "N/A",
            "overview": content.get("overview", "No overview available."),
            "poster": f"https://image.tmdb.org/t/p/w780{content.get('poster_path')}" if content.get("poster_path") else None,
            "backdrop": f"https://image.tmdb.org/t/p/w780{content.get('backdrop_path')}" if content.get("backdrop_path") else None,
            "tmdb_link": f"https://www.themoviedb.org/{media_type}/{tmdbID}/",
            "more_poster": f"https://www.themoviedb.org/{media_type}/{tmdbID}/images/posters",
            "more_backdrop": f"https://www.themoviedb.org/{media_type}/{tmdbID}/images/backdrops"
        }
    else:
        return {}

def get_tmdb_trailer(tmdbID, title, year, media_type, tmdb_api_key):
    url = f"https://api.themoviedb.org/3/{media_type}/{tmdbID}/videos"
    response = requests.get(url, params={"api_key": tmdb_api_key}).json()
    videos = response.get("results", [])

    for video in videos:
        if video.get("site") == "YouTube" and video.get("type") == "Trailer":
            return {
                "title": video.get("name"),
                "url": f"https://www.youtube.com/watch?v={video.get('key')}"
            }
    return {
        "title": None,
        "url": None
    }


def get_details():
    file_info = FilePathInfo()
    fmeta = file_info.process()
    tmdb_api_key = config["TMDb"]["API_KEY"]

    imdb_id = fmeta.get("imdbID", "")
    imdbID = f"tt{imdb_id}" if imdb_id and not imdb_id.startswith("tt") else imdb_id if imdb_id else None
    tmdbID = fmeta.get("tmdbID", "") 
    filename = fmeta.get("filename", "")
    skip_youtube = fmeta.get("skip_youtube", False)
    skip_tmdb = fmeta.get("skip_tmdb", False)
    skip_imdb_tmdb = fmeta.get("skip_imdb_tmdb", False)
    
    info = guessit(filename)
    title = info.get("title")
    year = info.get("year")
    file_type = info.get("type")
    media_type = "movie" if file_type == "movie" else "tv"

    # IMDb ID and Details
    if not imdb_id and skip_imdb_tmdb is False:
        console.print("[bold yellow]Fetching IMDb ID from filename...[/bold yellow]")
        imdbID = search_imdb(filename, title, year, file_type)
        if not imdbID:
            imdb_id = Prompt.ask("[bold red]IMDb ID not found. Please enter IMDb ID:[/bold red]")
            imdbID = imdb_id if imdb_id.startswith("tt") else f"tt{imdb_id}"
    if imdbID:
        console.print("[bold yellow]Fetching IMDb Metadata...[/bold yellow]")
        imdb_details = get_imdb_details(imdbID)
    else:
        imdb_details = {}

    # TMDb ID and Details
    if not tmdbID and skip_tmdb is False and skip_imdb_tmdb is False:
        if not tmdb_api_key:
            console.print("[bold red]Error: TMDb API key is missing in the configuration.[/bold red]")
            error_exit()
            
        console.print("[bold green]Fetching TMDB ID...[/bold green]")
        tmdbID = get_tmdb_id(imdbID, tmdb_api_key)
        if not tmdbID:
            console.print("[bold green]Fetching TMDb ID from filename...[/bold green]")
            tmdbID = search_tmdb(title, year, media_type, tmdb_api_key)
            if not tmdbID:
                tmdbID = Prompt.ask("[bold red]TMDb ID not found. Please enter TMDb ID number[/bold red]")    
    if tmdbID:
        console.print("[bold green]Fetching TMDb Metadata...[/bold green]")
        tmdb_details = get_tmdb_details(tmdbID, media_type, tmdb_api_key)
    else:
        tmdb_details = {}

    # YouTube Trailer
    skip_youtube = fmeta.get("skip_youtube", False)
    if skip_tmdb is False and skip_youtube is False and skip_imdb_tmdb is False:
        console.print("[bold magenta]Fetching YouTube Trailer...[/bold magenta]")
        trailer_info = get_tmdb_trailer(tmdbID, title, year, media_type, tmdb_api_key)
    else: 
        trailer_info = {
                "title": None,
                "url": None,
        }

    full_data = {
        "imdb": imdb_details,
        "tmdb": tmdb_details,
        "trailer": trailer_info
    }
    fmeta.update(full_data)

    mpath = MetaPath()
    metapath = mpath.get_metapath()
    with open(metapath, "w", encoding="utf-8") as f:
        json.dump(fmeta, f, indent=4, ensure_ascii=False)

    return fmeta
