import os
import sys
import math
import base64
import json
import requests
import ffmpeg
from src.filepath import FilePathInfo
from data.config import config
from src.ia import console
from src.exit import error_exit


class Screens:
    def __init__(self):
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.video_path = self.fmeta.get('videopath')
        self.upload_folder = self.fmeta.get('upload_folder')

    def generate_screenshots(self):
        num_screenshots = int(config.get("screenshots_number", 10))
        quality = 2
        output_directory = os.path.join(self.upload_folder, "screenshots")
        os.makedirs(output_directory, exist_ok=True)

        if any(f.lower().endswith((".png", ".jpg")) for f in os.listdir(output_directory)):
            console.print("[bold green] ✔ Screenshots already exist. Skipping generation.")
            return

        try:
            probe = ffmpeg.probe(self.video_path)
            duration = float(probe['format']['duration'])
        except ffmpeg.Error as e:
            console.print(f"[bold red] ✖ Error probing video: {e.stderr.decode()}")
            error_exit()

        adjusted_duration = max(60, math.floor(duration) - 500)
        timestamps = [adjusted_duration / num_screenshots * i for i in range(1, num_screenshots + 1)]

        console.print("[bold yellow] ➥ Generating Screenshots...")
        generated_count = 0
        for i, timestamp in enumerate(timestamps, start=1):
            output_path = os.path.join(output_directory, f"screenshot_{i:02d}.png")
            try:
                (
                    ffmpeg
                    .input(self.video_path, ss=timestamp)
                    .output(output_path, vframes=1, q=quality)
                    .run(overwrite_output=False, quiet=True)
                )
                generated_count += 1
            except ffmpeg.Error as e:
                console.print(f"[bold red] ✖ Error at {timestamp}s: {e.stderr.decode()}")
                error_exit()

        if generated_count > 0:
            console.print("[bold green] ✔ Screenshots generated successfully.")
        else:   
            console.print("[bold red] ✖ No screenshots were generated.")
        
    def upload_images(self):
        image_host = config.get("image_host")
        image_host_api_key = config.get("image_host_api_key", {}).get(image_host)

        API_URLS = {
            "Freeimage": "https://freeimage.host/api/1/upload",
            "Imgbb": "https://api.imgbb.com/1/upload",
            "Imageride": "https://www.imageride.net/api/1/upload",
            "Lookmyimg": "https://lookmyimg.com/api/1/upload",
            "Onlyimg": "https://imgoe.download/api/1/upload",
            "PTScreen": "https://ptscreens.com/api/1/upload"
        }

        if not image_host or image_host not in API_URLS:
            console.print(f"[bold red] ✖ Invalid or unsupported image host: {image_host}")
            error_exit()

        if not image_host_api_key:
            console.print(f"[bold red] ✖ API key missing for image host: {image_host}")
            error_exit()

        api_url = API_URLS[image_host]

        folder = os.path.join(self.upload_folder, "screenshots")
        output_folder = os.path.join(folder, "uploaddata")
        os.makedirs(output_folder, exist_ok=True)

        bbcode_medium_path = os.path.join(output_folder, "bbcode_medium.txt")
        files = sorted(f.strip() for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg")))

        if os.path.exists(bbcode_medium_path):
            console.print("[bold green] ✔ Screenshots already uploaded. Skipping upload.")
            return

        if not files:
            console.print("[bold red] ✖ No screenshots found to upload.")
            error_exit()

        console.print("[bold yellow] ➥ Uploading Screenshots...")
        upload_results = []
        bbc_full, bbc_medium, bbc_thumb = [], [], []

        for img in files:
            output_path = os.path.join(folder, img)
            with open(output_path, "rb") as file:
                img_base64 = base64.b64encode(file.read()).decode('utf-8')

            payload = {"key": image_host_api_key, "image": img_base64}

            try:
                response = requests.post(api_url, data=payload)
                response.raise_for_status()
            except requests.RequestException as e:
                console.print(f"[bold red] ✖ Network error uploading {img}: {str(e)}")
                error_exit()

            try:
                img_response = response.json()
            except json.JSONDecodeError:
                console.print(f"[bold red] ✖ JSON decode error for {img}")
                error_exit()

            if not img_response.get("success", True):
                error_msg = img_response.get("error", {}).get("message", "Unknown error")
                console.print(f"[bold red] ✖ Upload failed for {img}: {error_msg}")
                error_exit()
                
            upload_results.append({img: img_response})

            url_full = img_response.get('data', {}).get('url', '')
            url_viewer = img_response.get('data', {}).get('url_viewer', '')
            url_medium = img_response.get('data', {}).get('medium', {}).get('url', '')
            url_thumb = img_response.get('data', {}).get('thumb', {}).get('url', '')

            if url_full and url_viewer:
                bbc_full.append(f"[url={url_viewer}][img]{url_full}[/img][/url]")
            if url_medium and url_viewer:
                bbc_medium.append(f"[url={url_viewer}][img]{url_medium}[/img][/url]")
            if url_thumb and url_viewer:
                bbc_thumb.append(f"[url={url_viewer}][img]{url_thumb}[/img][/url]")

        with open(os.path.join(output_folder, "upload_responses.json"), "w") as json_file:
            json.dump(upload_results, json_file, indent=4)

        with open(os.path.join(output_folder, "bbcode_full.txt"), "w") as f_full, \
             open(os.path.join(output_folder, "bbcode_medium.txt"), "w") as f_medium, \
             open(os.path.join(output_folder, "bbcode_thumb.txt"), "w") as f_thumb:
            f_full.write("\n\n".join(bbc_full))
            f_medium.write("\n\n".join(bbc_medium))
            f_thumb.write("\n\n".join(bbc_thumb))

        console.print("[bold green] ✔ Screenshots uploaded successfully.")
