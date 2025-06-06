# 🎞️ BWT-Uploader

**BWT-Uploader** is a powerful Python-based automation tool for uploading torrents to [BwTorrents](https://bwtorrents.tv). It automatically fetches metadata, handles MediaInfo, and generates BBCode descriptions — making the upload process fast and hassle-free.

> Created with ❤️ by [xDE3PM](https://github.com/xDE3PM)

---

## 🚀 Features

- 🔍 **Auto Metadata Detection**
  - Fetches IMDb ID, TMDb ID, trailer link, poster, and more
- ⚙️ **Automatically Torrent Creator**
  - Generates `.torrent` file with optimal settings
- 📄 **Media Info Generator**
  - Extracts and formats technical details using MediaInfo
- 🖼️ **Screenshot Generator**
  - Captures screenshots and uploads them to your preferred image host
- 🧾 **BBCode Description Generator**
  - Includes poster, screenshots, MediaInfo, IMDb/TMDb/YouTube links
- 📁 **Smart Category Selector**
  - Automatically detects or manually sets the correct category
- 📡 **Freeleech Checker**
  - Calculates and checks if upload qualifies for freeleech
- 📤 **Automatically Upload Torrent**
  - Full automation from detection to upload
- 💻 **Command-line Friendly**
  - Flexible CLI arguments with custom options

---

## 🧰 Requirements

### 🐍 Python Modules

Install all Python requirements using:

```bash
pip install -r data/requirements.txt
```

### 🛠️ System Tools (Required)

These must be installed and accessible from your system’s PATH:

- [Python](https://www.python.org/downloads/) – version 3.8 or higher
- [FFmpeg](https://ffmpeg.org/download.html) – for trailer handling and screenshots
- [MediaInfo](https://mediaarea.net/en/MediaInfo) – for detailed media metadata


You must have these tools installed and accessible from your system’s PATH:

- [FFmpeg](https://ffmpeg.org/download.html) – for trailer handling and screenshots
- [MediaInfo](https://mediaarea.net/en/MediaInfo) – for detailed media metadata

---

## 📦 How to Use

### 🔧 Setup Guide

1. **Clone this repository**

    ```bash
    git clone https://github.com/xDE3PM/BWT-Uploader
    ```

2. **Navigate to the project folder**

    ```bash
    cd BWT-Uploader
    ```

3. **Install dependencies**

    ```bash
    pip install -r data/requirements.txt
    ```

4. **Install required system tools** (if not already):

    - **FFmpeg:** [Install Guide](https://ffmpeg.org/download.html)
    - **MediaInfo:** [Install Guide](https://mediaarea.net/en/MediaInfo)

---

## 🏁 Basic Usage

Run the script with the path to your video file or folder:

```bash
python upload.py "file_path"
```

### 💡 CLI Argument Help

| Argument              | Shortcut  | Description |
|-----------------------|-----------|-------------|
| `filepath`            | *(positional)* | Path to the file/folder to upload |
| `--version`           | `-v`      | Show version info |
| `--imdb`              |           | Manually enter IMDb ID (e.g., `tt1234567`) |
| `--tmdb`              |           | Manually enter TMDb ID (e.g., `123456`) |
| `--request`           | `-r`      | Mark torrent as a request |
| `--recomanded`        | `-rm`     | Mark torrent as recommended |
| `--doubleupload`      | `-du`     | Enable double upload mode |
| `--catagory`          | `-c`      | Manually set category ID (e.g., `119`) |

---

## 🙌 Credits

- [IMDbPY](https://github.com/alberanid/imdbpy)
- [TMDb API](https://www.themoviedb.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [MediaInfo](https://mediaarea.net/)
- [Rich](https://github.com/Textualize/rich)

---

## 🤝 Contributing

Found a bug or have a feature suggestion?  
Feel free to open an [issue](https://github.com/xDE3PM/BWT-Uploader/issues) or [pull request](https://github.com/xDE3PM/BWT-Uploader/pulls).

---

## 🔗 Author

**[@xDE3PM](https://github.com/xDE3PM)**  
Proudly made for the BwT community ❤️
