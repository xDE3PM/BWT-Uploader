# config.py

config = {
    "TMDb": {
        # TMDb API key is required to fetch metadata (e.g., title, poster, etc.)
        "API_KEY": "tmdb_api_key"
    },

    # Number of screenshots to be taken from the video file (should be an integer)
    "screenshots_number": 8,

    # Choose an image host for uploading screenshots. 
    # Available options: "Freeimage", "Imgbb", "Imageride", "Lookmyimg", "Onlyimg", "PTScreen"
    # Default is "Imageride"
    "image_host": "Imageride",

    # API keys for each supported image host (only the one used will be required)
    "image_host_api_key": {
        "Freeimage": "freeimage_api_key",     # Required if image_host is "Freeimage"
        "Imgbb": "imgbb_api_key",             # Required if image_host is "Imgbb"
        "Imageride": "imageride_api_key",     # Required if image_host is "Imageride"
        "Lookmyimg": "lookmyimg_api_key",              # Required if image_host is "Lookmyimg"
        "Onlyimg": "onlyimg_api_key",         # Required if image_host is "Onlyimg"
        "PTScreen": "ptscreen_api_key"        # Required if image_host is "PTScreen"
    },

    "BWT": {
        "username": "your_username",   # Your BWTorrents UserName 
        "password": "your_password"    # Your BWTorrents Password 
    },

    "bbcode_config": {
        "media_info_style": "[img]https://i.ibb.co/DfF7Pbt/Media-Info.png[/img]",
        "general_style": "[b][color=green]★ General ★[/color][/b]",
        "video_track_style": "[b][color=blue]★ Video Track ★[/color][/b]",
        "audio_track_style": "[b][color=orange]★ Audio Track ★[/color][/b]",
        "subtitle_style": "[b][color=teal]★ Subtitle ★[/color][/b]",
        "chapters_style": "[b][color=Red]★ Chapters ★[/color][/b]"
    }
}

# Default BBCode template for the torrent description.
# You may customize the visual style and layout, but DO NOT remove the following placeholders:
#   - {movie_poster_url} : will be replaced with the movie/series poster image URL
#   - {file_name}        : will be replaced with the actual file name
#   - {screenshot_bbcode}: will be replaced with BBCode for uploaded screenshots

BBCODE_TEMPLATE = """
[center]
[img]{movie_poster_url}[/img]

[b][size=4][color=red]
[font=Arial]{file_name}[/font][/color]
[/size][/b]

{media_info}

[img]https://i.ibb.co/9vZTnQk/Screenshot.png[/img]

{screenshot_bbcode}

[b][size=5][color=green][font=Courier New]....Enjoying & Keep Seeding....[/font][/color][/size][/b]
[/center]
"""
