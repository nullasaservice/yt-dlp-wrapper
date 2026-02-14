#!/usr/bin/env python3

import subprocess
import json
import sys
from typing import List, Dict, Optional


def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, text=True)


def get_formats(url: str) -> List[Dict]:
    """
    Uses yt-dlp to get structured JSON info for the video
    """
    output = run(["yt-dlp", "-J", url])
    data = json.loads(output)
    return data["formats"]


def pick_smallest(formats: List[Dict]) -> Optional[Dict]:
    with_size = [f for f in formats if f.get("filesize")]
    return min(with_size, key=lambda f: f["filesize"], default=None)


def find_resolution_format(formats: List[Dict], target_height: int) -> Optional[str]:
    """
    Pick the format closest to the requested height.
    If no exact height match, try matching by typical width for the resolution.
    """
    # common width fallbacks for standard resolutions
    height_to_width = {720: 1280, 1080: 1920, 2160: 3840}

    video_formats = [f for f in formats if f.get("vcodec") != "none"]

    # 1) format_note contains target height (e.g., '1080p')
    candidates = [f for f in video_formats if f.get("format_note") and str(target_height) in f["format_note"]]
    chosen = pick_smallest(candidates)
    if chosen:
        return chosen["format_id"]

    # 2) resolution height match
    candidates = [f for f in video_formats if f.get("height") == target_height]
    chosen = pick_smallest(candidates)
    if chosen:
        return chosen["format_id"]

    # 3) fallback: try corresponding width
    target_width = height_to_width.get(target_height)
    if target_width:
        candidates = [f for f in video_formats if f.get("width") == target_width]
        chosen = pick_smallest(candidates)
        if chosen:
            return chosen["format_id"]

    # 4) fallback: largest below target height
    candidates = [f for f in video_formats if f.get("height") <= target_height]
    chosen = pick_smallest(candidates)
    if chosen:
        return chosen["format_id"]

    return None


def handle_resolution_download(url: str) -> None:
    """
    Let the user pick from 720p, 1080p, 4K
    """
    print("""
Choose target resolution:
  1) 720p
  2) 1080p
  3) 4K
============================================
""")
    res_option = input("Option: ").strip()
    if res_option == "1":
        target_height = 720
    elif res_option == "2":
        target_height = 1080
    elif res_option == "3":
        target_height = 2160  # 4K UHD
    else:
        print("Invalid option.")
        sys.exit(1)

    formats = get_formats(url)
    video_id = find_resolution_format(formats, target_height)

    if not video_id:
        print(f"No suitable format found for target {target_height}p.")
        sys.exit(1)

    format_string = f"{video_id}+bestaudio"
    print(f"\n>>> Selected video format: {video_id}")
    subprocess.run(["yt-dlp", "-f", format_string, url])


def handle_subtitles(url: str) -> None:
    print("""
Choose subtitle type:
  1) Manual subtitles
  2) Auto-generated subtitles
============================================
""")
    sub_type = input("Option: ").strip()
    lang = input("Enter subtitle language (e.g., en, es): ").strip()

    if sub_type == "1":
        cmd = ["yt-dlp", "--skip-download", "--write-subs", "--sub-lang", lang, url]
    elif sub_type == "2":
        cmd = ["yt-dlp", "--skip-download", "--write-auto-subs", "--sub-lang", lang, url]
    else:
        print("Invalid option.")
        sys.exit(1)

    subprocess.run(cmd)


def main():
    url = input("Enter video URL: ").strip()
    if not url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    print("\n>>> Retrieving available formats...\n")
    subprocess.run(["yt-dlp", "-F", url])

    print("""
============================================
Choose video/audio option:
  1) Best audio
  2) Best video + audio
  3) Choose predefined resolution from list (Recommended)
  4) Choose format manually
  5) No, I just want subtitles
============================================
""")
    option = input("Option: ").strip()

    if option == "1":
        subprocess.run(["yt-dlp", "-f", "bestaudio", url])

    elif option == "2":
        subprocess.run(["yt-dlp", "-f", "bestvideo+bestaudio", url])

    elif option == "3":
        handle_resolution_download(url)

    elif option == "4":
        fmt = input("Enter format code exactly (e.g., 251+137): ").strip()
        subprocess.run(["yt-dlp", "-f", fmt, url])

    elif option == "5":
        handle_subtitles(url)

    else:
        print("Invalid option.")
        sys.exit(1)


if __name__ == "__main__":
    main()
