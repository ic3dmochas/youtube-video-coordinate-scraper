import os
import shutil
import cv2
import yt_dlp
import ffmpeg
import time
import numpy as np

version = "v1.2.0"

print(f"[log]  F3 Scraper {version} by @ic3dwtf")
url = input(f"[log]  url: ")

debug_pixel = (4, 5)
script_dir = os.path.dirname(os.path.abspath(__file__))
bin_path = os.path.join(script_dir, "bin")
vid_file = os.path.join(bin_path, "video")
frames_dir = os.path.join(bin_path, "frames")

if os.path.exists(bin_path):
    shutil.rmtree(bin_path) 

os.makedirs(bin_path, exist_ok=True)
os.makedirs(frames_dir, exist_ok=True)

ydl_opts = {
    'outtmpl': vid_file + '.%(ext)s',
    'postprocessors': [{ 
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4', 
    }],
    'quiet': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    formats = info_dict.get('formats', [])
    
    for fmt in formats:
        if fmt.get('height') == 360 and fmt.get('ext') in 'mp4':
            print(f"[log]  video supported! id {fmt['format_id']}, resolution: {fmt['height']}p, ext: {fmt['ext']}, fps: {fmt['fps']}")
            input("[log]  press enter to download . . .")
            break
    else:
        input("[log]  video not supported...")
        exit()

ydl_opts['format'] = fmt['format_id']
ydl.download([url])

print("[log]  video downloaded, proceeding with ffmpeg...")
time.sleep(1)
    
if not os.path.exists(vid_file + '.mp4'): 
    input(f"[log]  video file not found at {vid_file + '.mp4'}")
    exit()
else:
    print("[log]  video file found, proceeding with ffmpeg...")

try:
    ffmpeg.input(vid_file + '.mp4').output(os.path.join(frames_dir, "frame_%04d.png"), vf="fps=1").run()
except ffmpeg._run.Error as e:
    if e.stderr:
        print(f"[log]  ffmpeg error: {e.stderr.decode()}")
    else:
        print(f"[log]  ffmpeg error: {e}")

for frame in sorted(os.listdir(frames_dir)):
    path = os.path.join(frames_dir, frame)
    img = cv2.imread(path)
    pixel = img[debug_pixel[1], debug_pixel[0]]
    if np.all(pixel > 200):
        print(f"[log]  F3 detected in {frame}")
    else:
        print(f"[log]  failed detection at {frame}")
        os.remove(path)

input("[log]  finished! press enter to exit . . .")
