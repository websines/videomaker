import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

# Define the paths to the video folders
top_folder = "meme_videos"
bottom_folder = "client_videos"
output_folder = "merged_videos"

# Get a list of the video files in each folder
top_files = os.listdir(top_folder)
bottom_files = os.listdir(bottom_folder)

for bottom_file in bottom_files:
    for top_file in top_files:
        bottom_path = os.path.join(bottom_folder, bottom_file)
        top_path = os.path.join(top_folder, top_file)

        # Load the two video clips
        clip1 = VideoFileClip(top_path)
        clip2 = VideoFileClip(bottom_path)

        # Check which clip is longer
        if clip1.duration > clip2.duration:
            # Calculate the number of times to loop the bottom clip to match the duration of the top clip
            num_loops = int(clip1.duration / clip2.duration) + 1
            # Loop the bottom clip
            clip2 = clip2.fx(VideoFileClip.set_duration, num_loops * clip2.duration)
        else:
            # Trim the bottom clip to the duration of the top clip
            clip2 = clip2.subclip(0, clip1.duration)

        # Resize the clips to maintain 9:16 aspect ratio
        aspect_ratio = 9 / 16
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
