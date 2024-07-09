import sys
import os
from moviepy.editor import VideoFileClip
from PIL import Image

def convert_mp4_to_gif(input_path, output_path):
    clip = VideoFileClip(input_path)
    clip.write_gif(output_path, program='ffmpeg', opt='nq')

    if os.path.getsize(output_path) > 10 * 1024 * 1024:  # 10mb
        print("GIF is too large, optimising...")
        optimise_gif(output_path)

def optimise_gif(gif_path):
    with Image.open(gif_path) as img:
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        img.save(gif_path, optimize=True, quality=85)

    if os.path.getsize(gif_path) > 10 * 1024 * 1024:
        print("Optimisation failed, please try a shorter or lower resolution video.")
    else:
        print("Optimisation successful, file size is under 10MB.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_mp4_path> <output_gif_path>")
        sys.exit(1)

    input_mp4_path = sys.argv[1]
    output_gif_path = sys.argv[2]

    convert_mp4_to_gif(input_mp4_path, output_gif_path)
