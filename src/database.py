import os, json, sys
import requests
import subprocess
from guessit import guessit
from src.ia import ia
from data.config import config
from src.metafile import MetaPath
from src.filepath import FilePathInfo
from src.ia import console
from rich.prompt import Prompt


def search_imdb(filename, name, year, file_type):
    # Search
    movies = ia.search_movie(name)
    best_match = None
    for m in movies:
        movie_details = ia.get_movie(m.movieID)
        imdb_type = movie_details.get('kind', 'Unknown')
        if file_type == "movie" and imdb_type == "movie":
            if year and movie_details.get('year') == year:
                best_match = movie_details
                break
        elif file_type == "episode" and imdb_type in ["tv series", "tv mini series"]:
            if year and movie_details.get('year') == year:
                best_match = movie_details
                break  

    # Fast one
    if not best_match:
        best_match = ia.get_movie(movies[0].movieID) if movies else None

    # Match one
    if best_match:
        return best_match.movieID
    
    return None

def get_imdb_details(imdbID):
    movie = ia.get_movie(imdbID)
    imdb_id = f"tt{imdbID}"
    return {
        "id": imdb_id,
        "title": movie.get("title", "N/A"),
        "year": movie.get("year", "N/A"),
        "genres": movie.get("genres", []),
        "rating": movie.get("rating", "N/A"),
        "plot": movie.get("plot", [""])[0],
        "poster": movie.get("full-size cover url", "N/A"),
        "link": f"https://www.imdb.com/title/{imdb_id}/",
        "type": movie.get("kind", "N/A").upper() 
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
    imdb_id = f"tt{imdbID}"
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={tmdb_api_key}&external_source=imdb_id"
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
            "rating": content.get("vote_average", "N/A"),
            "overview": content.get("overview", "No overview available."),
            "poster": f"https://image.tmdb.org/t/p/w780{content.get('poster_path')}" if content.get("poster_path") else None,
            "backdrop": f"https://image.tmdb.org/t/p/w500{content.get('backdrop_path')}" if content.get("backdrop_path") else None,
            "tmdb_link": f"https://www.themoviedb.org/{media_type}/{tmdbID}/",
            "more_poster": f"https://www.themoviedb.org/{media_type}/{tmdbID}/images/posters",
            "more_backdrop": f"https://www.themoviedb.org/{media_type}/{tmdbID}/images/backdrops"
        }
    else:
        return {}

def get_youtube_trailer(title, year, media_type):
    query = f"{title} {year} {media_type} official trailer"
    yt_cookie_path = "data/cookies/YouTube.txt"
    if not os.path.exists(yt_cookie_path):
        sys.exit("Error: YouTube Cookie file does not exist at the specified path.")
    cmd = [
        "yt-dlp", f"ytsearch5:{query}",
        "--print", "%(id)s|%(title)s",
        "--cookies", f"{yt_cookie_path}"
    ]
    try:
        output = subprocess.check_output(cmd, text=True).strip().split("\n")[0]
        video_id, video_title = output.split("|", 1)
        return {"title": video_title, "url": f"https://www.youtube.com/watch?v={video_id}"}
    except subprocess.CalledProcessError:
        return {"title": None, "url": None}

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
    return get_youtube_trailer(title, year, media_type)

def get_details():
    file_info = FilePathInfo()
    fmeta = file_info.process()
    tmdb_api_key = config["TMDb"]["API_KEY"]
    
    imdbID = fmeta.get("imdbID", "")
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
    if not imdbID and skip_imdb_tmdb is False:
        console.print("[bold yellow]Fetching IMDb ID from filename...[/bold yellow]")
        imdbID = search_imdb(filename, title, year, file_type)
        if not imdbID:
            imdbID = Prompt.ask("[bold red]IMDb ID not found. Please enter IMDb ID number[/bold red]")
    if imdbID:
        console.print("[bold yellow]Fetching IMDb Metadata...[/bold yellow]")
        imdb_details = get_imdb_details(imdbID)
    else:
        imdb_details = {}

    # TMDb ID and Details
    if not tmdbID and skip_tmdb is False and skip_imdb_tmdb is False:
        if not tmdb_api_key:
            console.print("[bold red]Error: TMDb API key is missing in the configuration.[/bold red]")
            console.print("[red]Exiting...[/red]")
            sys.exit(0)
            
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
    if skip_youtube is False:
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
