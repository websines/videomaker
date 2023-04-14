import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
from multiprocessing import Pool

# Define the paths to the video folders
top_folder = "meme_videos"
bottom_folder = "client_videos"
output_folder = "merged_videos"

# Get a list of the video files in each folder
top_files = os.listdir(top_folder)
bottom_files = os.listdir(bottom_folder)

def process_video(bottom_file, top_file):
    bottom_path = os.path.join(bottom_folder, bottom_file)
    top_path = os.path.join(top_folder, top_file)
    # Load the two video clips
    clip1 = VideoFileClip(top_path)
    clip2 = VideoFileClip(bottom_path)

    # Find the duration of the longer clip
    max_duration = max(clip1.duration, clip2.duration)

    # Trim both clips to the same duration
    if clip2.duration > clip1.duration:
        num_loops = int(max_duration / clip1.duration) + 1
        clip1 = concatenate_videoclips([clip1] * num_loops)
        clip1 = clip1.subclip(0, max_duration) 
    elif clip1.duration > clip2.duration:
        num_loops = int(max_duration / clip2.duration) + 1
        clip2 = concatenate_videoclips([clip2] * num_loops)
        clip2 = clip2.subclip(0, max_duration) 

    print(clip1.duration, clip2.duration)
    
    bottom_height = int(clip1.h / 2)
    top_height = int(bottom_height * 1.2)
    top_width = clip1.w
    clip1 = clip1.resize((top_width, top_height))
    clip2 = clip2.resize((top_width, bottom_height))

    # Stack the clips vertically and play them at the same time
    final_clip = CompositeVideoClip([clip1, clip2.set_position((0, top_height))],
                                    size=(clip1.w, top_height + bottom_height))

    # Write the merged video file to the output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_filename = os.path.join(output_folder, f"merged_video_{bottom_file.split('.')[0]}_{top_file.split('.')[0]}.mp4")
    final_clip.write_videofile(output_filename, fps=30)

    # Free up memory by deleting the clips
    del clip1, clip2, final_clip

if __name__ == '__main__':
    # create a list of arguments for process_video
    arguments = []
    for i, bottom_file in enumerate(bottom_files):
        for j, top_file in enumerate(top_files):
            arguments.append((bottom_file, top_file))
    # use multiprocessing to process videos in parallel
    with Pool(processes=2) as pool:
        pool.starmap(process_video, arguments)