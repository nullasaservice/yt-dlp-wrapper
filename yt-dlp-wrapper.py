#!/usr/bin/env python3

import subprocess
import json
import sys
from typing import List, Dict, Optional


def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, text=True)


def get_video_info(url: str) -> Dict:
    output = run(["yt-dlp", "-J", url])
    return json.loads(output)


def get_video_formats(info: Dict) -> List[Dict]:
    return [
        f for f in info["formats"]
        if f.get("vcodec") != "none" and f.get("acodec") == "none" and f.get("format_note")
    ]


def group_by_resolution(formats: List[Dict]) -> Dict[int, List[Dict]]:
    resolutions = {}
    for f in formats:
        h = int(f["format_note"].split("p")[0])
        resolutions.setdefault(h, []).append(f)
    return resolutions


def pick_smallest(formats: List[Dict]) -> Optional[Dict]:
    with_size = [f for f in formats if f.get("filesize")]
    if not with_size:
        return None
    return min(with_size, key=lambda f: f["filesize"])


def handle_dynamic_resolution_download(url: str) -> None:
    info = get_video_info(url)
    formats = get_video_formats(info)

    if not formats:
        print("No video formats found.")
        sys.exit(1)

    grouped = group_by_resolution(formats)

    # Sort resolutions descending (4K first etc.)
    available_resolutions = sorted(grouped.keys(), reverse=True)

    print("\nAvailable video resolutions:")
    for idx, res in enumerate(available_resolutions, start=1):
        print(f"  {idx}) {res}p")

    print("============================================")
    choice = input("Select resolution: ").strip()

    try:
        selected_height = available_resolutions[int(choice) - 1]
    except (IndexError, ValueError):
        print("Invalid option.")
        sys.exit(1)

    selected_formats = grouped[selected_height]
    chosen_format = pick_smallest(selected_formats)

    if not chosen_format:
        print("No suitable format found for that resolution.")
        sys.exit(1)

    format_id = chosen_format["format_id"]
    print(f"\n>>> Selected: {selected_height}p (format {format_id})")

    subprocess.run(["yt-dlp", "-f", f"{format_id}+bestaudio", url])


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
  3) Choose from resolution list (Recommended)
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
        handle_dynamic_resolution_download(url)

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