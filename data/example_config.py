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
    }
}

# Default BBCode template for the torrent description.
# You may customize the visual style and layout, but DO NOT remove the following placeholders:
#   - {movie_poster_url} : will be replaced with the movie/series poster image URL
#   - {file_name}        : will be replaced with the actual file name
#   - Replace Custom Media Info : manual note for replacing with custom MediaInfo if needed
#   - {general_info}     : will be dynamically filled with general MediaInfo details
#   - {video_info}       : will be dynamically filled with video track details
#   - {audio_info}       : will be dynamically filled with audio track details
#   - {text_info}        : will be dynamically filled with subtitle track details
#   - {chapters_info}    : will be dynamically filled with chapter information
#   - {screenshot_bbcode}: will be replaced with BBCode for uploaded screenshots

BBCODE_TEMPLATE = """
[center]
[img]{movie_poster_url}[/img]

[b][size=4][color=red]
[font=Arial]{file_name}[/font][/color]
[/size][/b]

[img]https://i.ibb.co/DfF7Pbt/Media-Info.png[/img]

†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****††*****†*****†*****†*****†

[quote]
[b][color=green]★ General ★[/color][/b]
[font=Courier New]
{general_info}
[/font]

[b][color=blue]★ Video Track ★[/color][/b]
[font=Courier New]
{video_info}
[/font]

[b][color=orange]★ Audio Track ★[/color][/b]
[font=Courier New]
{audio_info}
[/font]

[b][color=teal]★ Subtitle ★[/color][/b]
[font=Courier New]
{text_info}
[/font]

[b][color=Red]★ Chapters ★[/color][/b]
[font=Courier New]
{chapters_info}
[/font]
[/quote]

†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****†*****††*****†*****†*****†*****†

[img]https://i.ibb.co/9vZTnQk/Screenshot.png[/img]

{screenshot_bbcode}

[b][size=5][color=green][font=Courier New]....Enjoying & Keep Seeding....[/font][/color][/size][/b]
[/center]
"""
