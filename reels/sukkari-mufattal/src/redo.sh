#!/bin/bash
# إعادة تصيير مشاهد محددة ثم ضم الفيديو:  bash src/redo.sh 4 5   (بدون أرقام = كل المشاهد)
set -eu
cd /home/claude/reel
SC="${*:-1 2 3 4 5 6}"
python3 -I src/build.py
mkdir -p out
python3 -m http.server 8770 --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!; sleep 1
python3 src/render.py "$(echo $SC | tr ' ' ',')" 8770 || { kill $SRV; exit 1; }
kill $SRV 2>/dev/null || true
for i in 1 2 3 4 5 6; do [ -f out/sc$i.mp4 ] || cp out/scenes/sc$i.mp4 out/sc$i.mp4; echo "file 'sc$i.mp4'"; done > out/list.txt
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i out/list.txt -c copy -movflags +faststart out/tmp_final.mp4
mv out/tmp_final.mp4 out/basateen-sukkari-mufattal-malaki-reel-30s.mp4
python3 -I src/verify.py
