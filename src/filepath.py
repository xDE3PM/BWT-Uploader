import os
from pathlib import Path
from typing import Optional
from src.args import Args

VIDEO_EXTENSIONS = {
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m2ts', '.vob'
}

AUDIO_EXTENSIONS = {
    '.mp3', '.flac', '.aac', '.m4a', '.wav', '.ogg'
}

class FilePathInfo:
    def __init__(self):
        self.meta = Args().gmeta()
        self.file_path = Path(self.meta.get("filepath", "")).resolve()
        self.file_name = None
        self.file_name_no_ext = None
        self.video_path = None
        self.video_file_name = None
        self.upload_folder = None
        self.torrent_path = None

    def _find_largest_file(self, start_path: Path, extensions: set) -> Optional[Path]:
        largest_file = None
        largest_size = -1
        for file in start_path.rglob("*"):
            if file.is_file() and file.suffix.lower() in extensions:
                try:
                    size = file.stat().st_size
                    if size > largest_size:
                        largest_size = size
                        largest_file = file
                except OSError:
                    continue
        return largest_file

    def process(self):
        raw_bluray = False
        raw_dvd = False
        video_media = False
        audio_music = False

        if self.file_path.is_file():
            self.file_name = self.file_path.name
            self.file_name_no_ext = self.file_path.stem
            self.video_path = self.file_path

            ext = self.file_path.suffix.lower()
            if ext in VIDEO_EXTENSIONS:
                video_media = True
            elif ext in AUDIO_EXTENSIONS:
                audio_music = True

        elif self.file_path.is_dir():
            self.file_name = self.file_path.name
            self.file_name_no_ext = self.file_path.name

            # Check for Blu-ray
            bdmv_path = self.file_path / "BDMV" / "STREAM"
            if bdmv_path.is_dir():
                self.video_path = self._find_largest_file(bdmv_path, VIDEO_EXTENSIONS)
                raw_bluray = True
                video_media = True

            # Check for DVD
            elif (self.file_path / "VIDEO_TS").is_dir():
                self.video_path = self._find_largest_file(self.file_path / "VIDEO_TS", VIDEO_EXTENSIONS)
                raw_dvd = True
                video_media = True

            else:
                # Look for video first
                self.video_path = self._find_largest_file(self.file_path, VIDEO_EXTENSIONS)
                if self.video_path:
                    video_media = True
                else:
                    # If no video, look for audio
                    self.video_path = self._find_largest_file(self.file_path, AUDIO_EXTENSIONS)
                    if self.video_path:
                        audio_music = True

        if self.video_path:
            self.video_file_name = self.video_path.name

        self.upload_folder = Path("uploads") / self.file_name_no_ext
        self.upload_folder.mkdir(parents=True, exist_ok=True)

        self.torrent_path = self.upload_folder / f"{self.file_name_no_ext}.torrent"

        self.meta.update({
            "filename": self.file_name,
            "filename_noext": self.file_name_no_ext,
            "videopath": str(self.video_path) if self.video_path else None,
            "video_filename": self.video_file_name,
            "filepath": str(self.file_path),
            "upload_folder": str(self.upload_folder),
            "torrent_path": str(self.torrent_path),
            "video_media": video_media,
            "raw_bluray": raw_bluray,
            "raw_dvd": raw_dvd,
            "audio_music": audio_music
        })

        return self.meta
