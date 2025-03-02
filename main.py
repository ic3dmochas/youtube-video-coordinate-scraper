import os
import cv2
import yt_dlp
import ffmpeg
import numpy as np

url = input(f"url: ")
debug_pixel = (7, 9)
script_dir = os.path.dirname(os.path.abspath(__file__))
bin_path = os.path.join(script_dir, "bin")
vid_file = os.path.join(bin_path, "video.mp4")
frames_dir = os.path.join(bin_path, "frames")
os.makedirs(bin_path, exist_ok=True)
os.makedirs(frames_dir, exist_ok=True)

def download():
    ydl_opts = {
        'outtmpl': vid_file,
        'format': '609',
        'postprocessors': [{ 
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4', 
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        valid_format = any(fmt['format_id'] == '609' for fmt in formats)
        
        if not valid_format:
            print("this video doesn't support the resolution required.")
            return
        
        ydl.download([url])

    if not os.path.exists(vid_file):
        print(f"video file not found at {vid_file}")
        return
    else:
        print("video file found, proceeding with ffmpeg...")

    try:
        ffmpeg.input(vid_file).output(os.path.join(frames_dir, "frame_%04d.png"), vf="fps=1").run()
    except ffmpeg._run.Error as e:
        if e.stderr:
            print(f"ffmpeg error: {e.stderr.decode()}")
        else:
            print(f"ffmpeg error: {e}")


def checkf3(frame_path):
    img = cv2.imread(frame_path)
    pixel = img[debug_pixel[1], debug_pixel[0]]
    return np.all(pixel > 200)

def checkall():
    for frame in sorted(os.listdir(frames_dir)):
        path = os.path.join(frames_dir, frame)
        if checkf3(path):
            print(f"F3 detected in {frame}")

download()
checkall()
