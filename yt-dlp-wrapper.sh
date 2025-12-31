#!/usr/bin/env bash

echo -n "Enter video URL: "
read URL

if [ -z "$URL" ]; then
    echo "No URL provided. Exiting."
    exit 1
fi

echo
echo ">>> Retrieving available formats..."
echo
yt-dlp -F "$URL"
echo

echo "============================================"
echo "Choose video/audio option:"
echo "  1) Best audio"
echo "  2) Best video + audio"
echo "  3) Video + audio in 1080p (Recommended)"
echo "  4) Choose format manually"
echo "  5) No, I just want subtitles"
echo "============================================"
echo -n "Option: "
read OPTION

FORMAT=""
SUB_CMD=""
SUB_LANG=""

# Subtitle-only menu
if [ "$OPTION" = "5" ]; then
    echo
    echo "Choose subtitle type:"
    echo "  1) Manual subtitles"
    echo "  2) Auto-generated subtitles"
    echo "============================================"
    echo -n "Option: "
    read SUB_TYPE

    echo -n "Enter subtitle language (e.g., en, es, fr): "
    read SUB_LANG

    case "$SUB_TYPE" in
        1) SUB_CMD="--write-subs --sub-lang $SUB_LANG" ;;
        2) SUB_CMD="--write-auto-subs --sub-lang $SUB_LANG" ;;
        *) echo "Invalid option."; exit 1 ;;
    esac

    echo
    echo ">>> Downloading subtitles only..."
    yt-dlp --skip-download $SUB_CMD "$URL"
    exit 0
fi

# Video/audio menu
case "$OPTION" in
    1)
        FORMAT="bestaudio"
        ;;
    2)
        FORMAT="bestvideo+bestaudio"
        ;;
    3)
        # Best video at 1080p + best audio
        FORMAT="bestvideo[height=1080]+bestaudio"
        ;;
    4)
        echo
        echo "Enter format code exactly (e.g., 251+137): "
        read FORMAT
        ;;
    *)
        echo "Invalid option."
        exit 1
        ;;
esac

echo
echo ">>> Downloading video/audio with format: $FORMAT"
yt-dlp -f "$FORMAT" "$URL"
