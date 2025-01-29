from moviepy.editor import VideoFileClip, clips_array, ColorClip

# Load the pre-rendered video files
clip1 = VideoFileClip("/home/brianmcgloughlin/Manim_Animation_Scripts/media/videos/Spinning_Ellipsoid/480p15/RotatingEllipsoid.mp4")
clip2 = VideoFileClip("/home/brianmcgloughlin/Manim_Animation_Scripts/media/videos/GW_Polarization_on_Point_of_grids/1080p60/GravitationalWavePolarizations.mp4")
clip3 = VideoFileClip("/home/brianmcgloughlin/All_Animations_for_China/Anim_1_GW_At_Hanford.mp4")

# Resize clips for the top quadrants (half the height and centered horizontally)
clip1 = clip1.resize(height=clip1.h // 2).set_position(('right', 'top'))
clip2 = clip2.resize(height=clip2.h // 2).set_position(('left', 'top'))

# Resize clip3 to take the entire bottom half of the screen (half the height, full width)
clip3 = clip3.resize(height=clip1.h * 2, width=clip1.w * 2).set_position(('center', 'bottom'))

# Create a black clip (used as placeholder for the empty quadrant)
black_clip = ColorClip(size=(clip1.w, clip1.h), color=(0, 0, 0), duration=clip1.duration)

# Combine the clips into a grid layout (2x2, with the 4th quadrant filled with a black clip)
final_clip = clips_array([[clip1, clip2], [clip3, black_clip]])

# Output the final combined video
final_clip.write_videofile("combined_output.mp4", codec="libx264", fps=24)
