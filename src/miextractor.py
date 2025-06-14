import json, os, re
from pymediainfo import MediaInfo
from src.filepath import FilePathInfo
from src.ia import console

class MediaInfoExtractor:
    def __init__(self):
        self.data = None
        self.file_info = FilePathInfo()
        self.fmeta = self.file_info.process()
        self.video_path = self.fmeta.get('videopath')
        self.upload_folder = self.fmeta.get('upload_folder')
        self.template_path = "data/templates/Media_Info.txt"
        self.mi_text_path = os.path.join(self.upload_folder, "Media_Info.txt")
        self.mi_json_path = os.path.join(self.upload_folder, "MediaInfo.json")
        self.video_file_name = self.fmeta.get('video_filename')

        
    def save_mi_text(self, filepath, media_info):
        lines = media_info.splitlines()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{self.video_file_name}\n\n")    
            for line in lines:
                if line.startswith("Complete name"):
                    f.write(f"Complete name                            : {self.video_file_name}\n")
                else:
                    f.write(line + "\n")

    def save_media_info(self):
        console.print("[bold yellow] ➥ Exporting MediaInfo...[/bold yellow]")
        
        # Save Text
        media_info_text = MediaInfo.parse(
            self.video_path, 
            output="STRING", 
            full=False, 
            mediainfo_options={"inform_version": "1", "inform_timestamp": "1"}
        )

        self.save_mi_text(self.mi_text_path, media_info_text)
       
        # Save JSON
        try:
            if not os.path.isfile(self.video_path):
                return False
            media_info = MediaInfo.parse(self.video_path)
            data = json.loads(media_info.to_json())
            tracks = data.get('tracks', [])
            if not tracks:
                return False
            with open(self.mi_json_path, 'w', encoding='utf-8') as f:
                json.dump({'tracks': tracks}, f, indent=2)
            return True
        except:
            console.print(f"[red] ❌ Error saving JSON: {e}[/red]")
            return False

    def load_mediainfo_json(self):
        try:
            with open(self.mi_json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except:
            return False

    def _g(self, t, k, d=''):
        return t.get(k, d) if t else d

    def _get_list(self, t, k, i, d=''):
        return t.get(k, [''])[i] if t and len(t.get(k, [''])) > i else d

    def extract_all_details(self):
        if not self.data or not self.data.get('tracks'):
            return '', '', '', '', ''

        data = self.data
        g = self._g
        get_list = self._get_list

        # General
        general_info = []
        general = next((t for t in data['tracks'] if t.get('track_type') == 'General'), None)
        if general:
            general_info.append(f"File Name.............: {g(general, 'file_name_extension')}")
            general_info.append(f"Format................: {g(general, 'format')} ({g(general, 'format_version')})")
            general_info.append(f"Duration..............: {get_list(general, 'other_duration', 1)}")
            general_info.append(f"Overall Bitrate.......: {get_list(general, 'other_overall_bit_rate', 0)} {g(general, 'overall_bit_rate_mode')}")
            general_info.append(f"File Size.............: {get_list(general, 'other_file_size', 3)}")
        general_info = '\n'.join(general_info)

        # Video
        video_info = []
        video = next((t for t in data['tracks'] if t.get('track_type') == 'Video'), None)
        if video:
            if g(video, 'title'):
                video_info.append(f"Title ................: {g(video, 'title')}")
            video_info.append(f"Format................: {g(video, 'format')} ({g(video, 'bit_depth')} bits)")
            video_info.append(f"Format Profile........: {g(video, 'format_profile')}")
            video_info.append(f"Resolution............: {g(video, 'width')} x {g(video, 'height')}")
            video_info.append(f"Aspect Ratio..........: {get_list(video, 'other_display_aspect_ratio', 0, g(video, 'display_aspect_ratio'))}")
            video_info.append(f"Bit Rate..............: {get_list(video, 'other_bit_rate', 0)} {g(video, 'bit_rate_mode')}")
            video_info.append(f"Frame Rate............: {get_list(video, 'other_frame_rate', 0)} ({g(video, 'frame_rate_mode')})")
            if g(video, 'color_primaries'):
                video_info.append(f"Color Primaries.......: {g(video, 'color_primaries')}")
            if get_list(video, 'other_writing_library', 0):
                video_info.append(f"Encoding Library......: {get_list(video, 'other_writing_library', 0)}")
        video_info = '\n'.join(video_info) if video_info else '[b]Video Not Available.[/b]'

        # Audio
        audio_info = []
        audios = [t for t in data['tracks'] if t.get('track_type') == 'Audio']
        if audios:
            for i, t in enumerate(audios):
                audio_info.append(f"Track {i+1:02d}:")
                if g(t, 'title'):
                    audio_info.append(f"Title ................: {g(t, 'title')}")
                audio_info.append(f"Language..............: {get_list(t, 'other_language', 0)}")
                audio_info.append(f"Format................: {g(t, 'commercial_name', g(t, 'format'))} ({get_list(t, 'other_format', 0)})")
                audio_info.append(f"Bitrate...............: {get_list(t, 'other_bit_rate', 0)} ({g(t, 'bit_rate_mode')}) : {get_list(t, 'other_sampling_rate', 0)}")
                audio_info.append(f"Channels..............: {g(t, 'channel_s')} channels ({g(t, 'channel_positions')})")
                if i < len(audios) - 1:
                    audio_info.append("")
        audio_info = '\n'.join(audio_info) if audio_info else '[b]Audio Not Available.[/b]'

        # Subtitles
        text_info = []
        texts = [t for t in data['tracks'] if t.get('track_type') == 'Text']
        if texts:
            for i, t in enumerate(texts):
                title = f"{g(t, 'title')} - " if g(t, 'title') else ''
                text_info.append(f"Language .............: {title}{get_list(t, 'other_language', 0)} ({g(t, 'commercial_name', g(t, 'format'))})")
                if i < len(texts) - 1:
                    text_info.append("")
        text_info = '\n'.join(text_info) if text_info else '[b]Subtitle Not Available.[/b]'

        # Chapters
        menu_info = []
        menu = next((t for t in data['tracks'] if t.get('track_type') == 'Menu'), None)
        if menu and any(k for k in menu if re.match(r'\d{2}_\d{2}_\d{5}', k)):
            chapter_keys = sorted([k for k in menu if re.match(r'\d{2}_\d{2}_\d{5}', k)])
            for i, key in enumerate(chapter_keys, 1):
                timestamp = key.replace('_', ':')[:8]
                title = g(menu, 'title', f"Chapter {i:02d}")
                title = re.sub(r'^\w{2}:', '', title)
                menu_info.append(f"Chapter {i:02d}...........: {timestamp} - {title}")
        menu_info = '\n'.join(menu_info) if menu_info else '[b]Chapter Not Available.[/b]'

        return general_info, video_info, audio_info, text_info, menu_info

    def process(self):
        if self.save_media_info() and self.load_mediainfo_json():
            console.print("[bold green] ✔ MediaInfo Exported...[/bold green]")
        else:
            console.print("[bold red] ✘ Failed to export/load MediaInfo.[/bold red]")

    def get_custom_mediainfo(self):
        if not self.data:
            if not self.load_mediainfo_json():
                console.print("[bold red] ✘ MediaInfo data not loaded. Run process() first.[/bold red]")
                return '', '', '', '', ''
        return self.extract_all_details()
