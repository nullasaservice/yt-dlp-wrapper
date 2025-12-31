# yt-dlp-wrapper

An interactive Bash script that simplifies downloading videos, audio, or subtitles using **yt-dlp**.  
It guides you through format selection, resolution choices, and subtitle options without needing to remember yt-dlp flags.

## Features

- Interactive menu-driven interface
- List all available formats before downloading
- Download options:
  - Best audio only
  - Best video + audio
  - Best video + audio at **1080p**
  - Manually choose a format code
- Subtitle-only downloads:
  - Manual subtitles
  - Auto-generated subtitles
  - Choose subtitle language
- Safe input validation and clean exits

## Requirements

- **Bash** (Linux, macOS, or WSL)
- **yt-dlp**

Install yt-dlp:

    pip install -U yt-dlp

Or via package manager (example):

    sudo apt install yt-dlp

## Installation

1. Save the script as `yt-dlp-wrapper.sh`
2. Make it executable:

       chmod +x yt-dlp-wrapper.sh

3. (Optional) Move it to your PATH:

       mv yt-dlp-wrapper.sh /usr/local/bin/ytdl

## Usage

Run the script:

    ./yt-dlp-wrapper.sh

or (if added to PATH):

    ytdl

You will be prompted to:

1. Enter a video URL
2. View available formats
3. Choose one of the following options:

    1) Best audio  
    2) Best video + audio  
    3) Video + audio in 1080p (Recommended)  
    4) Choose format manually  
    5) No, I just want subtitles  

## Subtitle-Only Mode

If you choose option **5**, you can:

- Select **manual** or **auto-generated** subtitles
- Specify a language (e.g. `en`, `es`, `fr`)
- Download subtitles without the video

## Examples

### Download best audio
    Option: 1

### Download best video + audio at 1080p
    Option: 3

### Manually choose formats
    Option: 4
    Enter format code exactly (e.g., 251+137)

### Download English auto-generated subtitles only
    Option: 5
    Subtitle type: 2
    Language: en

## Notes

- The script runs `yt-dlp -F` first so you can see all available formats.
- Format codes depend on the source and may vary per video.
- 1080p downloads use the best available video stream with height exactly `1080`.

## License

MIT License — use, modify, and distribute freely.
