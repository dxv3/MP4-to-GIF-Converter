import sys
import os
import imageio
from moviepy.editor import VideoFileClip

def convert_mp4_to_gif(input_path, output_path, max_size=10*1024*1024):
    try:
        print(f"Loading video: {input_path}")
        clip = VideoFileClip(input_path)
        
        # Binary search for optimal fps
        min_fps = 1
        max_fps = 30
        best_fps = min_fps

        while min_fps <= max_fps:
            mid_fps = (min_fps + max_fps) // 2
            print(f"Testing fps: {mid_fps}")
            frames = []
            for frame in clip.iter_frames(fps=mid_fps, dtype='uint8'):
                frames.append(frame)


            temp_gif_path = "temp.gif"
            imageio.mimsave(temp_gif_path, frames, format='GIF', fps=mid_fps)

            gif_size = os.path.getsize(temp_gif_path)
            print(f"GIF size at {mid_fps} fps: {gif_size} bytes")

            if gif_size <= max_size:
                best_fps = mid_fps
                min_fps = mid_fps + 1
            else:
                max_fps = mid_fps - 1


            if os.path.exists(temp_gif_path):
                os.remove(temp_gif_path)

        frames = []
        for frame in clip.iter_frames(fps=best_fps, dtype='uint8'):
            frames.append(frame)

        print(f"Creating GIF with optimal fps: {best_fps}")
        imageio.mimsave(output_path, frames, format='GIF', fps=best_fps)
        print(f"GIF created successfully at {best_fps} fps.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_mp4_path> <output_gif_path>")
        sys.exit(1)

    input_mp4_path = sys.argv[1]
    output_gif_path = sys.argv[2]

    convert_mp4_to_gif(input_mp4_path, output_gif_path)
