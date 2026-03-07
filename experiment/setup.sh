#!/bin/bash
# Køyr dette éin gong før eksperimentet for å klargjere bileter og lydfiler.
# Krev: ImageMagick (convert) og Python 3

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK_DIR="$SCRIPT_DIR/../task-files"

echo "=== Konverterer BMP til PNG ==="
for f in "$TASK_DIR"/*.bmp; do
    base=$(basename "$f" .bmp)
    out="$SCRIPT_DIR/img/$base.png"
    if [ ! -f "$out" ]; then
        convert "$f" "$out"
        echo "  $base.png"
    fi
done

echo "=== Konverterer WAV til MP3 (betre nettlesar-støtte) ==="
for f in "$TASK_DIR"/*.wav; do
    base=$(basename "$f" .wav)
    out="$SCRIPT_DIR/snd/$base.mp3"
    wav_out="$SCRIPT_DIR/snd/$base.wav"
    if [ ! -f "$wav_out" ]; then
        cp "$f" "$wav_out"
    fi
done

echo ""
echo "=== Ferdig! Start eksperimentet med: ==="
echo "  cd $SCRIPT_DIR"
echo "  python3 -m http.server 8080"
echo "  Opne: http://localhost:8080"
