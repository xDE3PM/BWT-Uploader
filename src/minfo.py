import os
from pymediainfo import MediaInfo
from src.filepath import FilePathInfo
from src.ia import console

class MediaInfoGenerator:
    def __init__(self):
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.video_path = self.fmeta.get('videopath')
        self.upload_folder = self.fmeta.get('upload_folder')
        self.template_path = "data/templates/Media_Info.txt"
        self.video_file_name = self.fmeta.get('video_filename')

    def generate_media_info(self):
        console.print("[bold yellow] ➥ Exporting MediaInfo...[/bold yellow]")
        mediainfo_opath = os.path.join(self.upload_folder, "Media_Info.txt")
        custom_mediainfo_opath = os.path.join(self.upload_folder, "Custom_Media_Info.txt")

        media_info = MediaInfo.parse(
            self.video_path, 
            output="STRING", 
            full=False, 
            mediainfo_options={"inform_version": "1", "inform_timestamp": "1"}
        )

        custom_media_info = MediaInfo.parse(
            self.video_path, 
            output="STRING", 
            full=False, 
            mediainfo_options={"inform": f"file://{self.template_path}", "inform_version": "1", "inform_timestamp": "1"}
        )

        self._save_media_info(mediainfo_opath, media_info)
        self._save_custom_media_info(custom_mediainfo_opath, custom_media_info)
        console.print("[bold green] ✔ MediaInfo Exported...[/bold green]")

    def _save_media_info(self, filepath, media_info):
        lines = media_info.splitlines()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{self.video_file_name}\n\n")    
            for line in lines:
                if line.startswith("Complete name"):
                    f.write(f"Complete name                            : {self.video_file_name}\n")
                else:
                    f.write(line + "\n")

    def _save_custom_media_info(self, filepath, custom_media_info):
        with open(filepath, "w", encoding="utf-8") as output_file:
            output_file.write(custom_media_info)

    
