"""
    Combining frames into a video, then adding sound from the source video.

    frames: a glob-like pattern, for example '/content/out_resized/frame*.jpg'
    vid_name: path to the input video
    fps: fps :D
    out_fname: output video name. Use mp4 container by default.
"""

ffmpeg -f image2 -r {fps} -pattern_type glob -i "{frames}"  -i "{vid_name}" -c:v copy -c:a aac -map 0:v:0 \
 -map 1:a:0 -shortest  -vcodec libx264 -r {fps} -crf 18  -pix_fmt yuv420p   "{out_fname}"

"""
    The simplest way to combine frames into video

    frames: a glob-like pattern, for example '/content/out_resized/frame*.jpg'
    fps: fps :D
    out_fname: output video name. Use mp4 container by default.
"""

ffmpeg -pattern_type glob -i "{frames}" -filter:v fps={fps} "{out_fname}"

"""
    The simplest way to split a video into frames

    vid_name: input video'
    out_dir: output folder. 
    q:v 2: image quality of in range 1-31, 1 being the highest

    You can change the pattern if you need more digits (increase the number in %05d pattern), or change the filename. 
"""

ffmpeg -v quiet -i "{vid_name}" -q:v 2 "{out_dir}/frame_%05d.jpg"
    
""" 
    Extract every nth frame (2 in this case)
"""
ffmpeg -v quiet -i "{vid_name}" -vf "select=not(mod(n\,2))" -vsync vfr -q:v 2 "{out_dir}/frame_%05d.jpg"
