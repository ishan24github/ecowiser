import subprocess
import pysrt

from celery import shared_task

# @shared_task
def extract_subtitles(video_path, subtitle_path):
    
    # ccextractor_cmd = ['ccextractor', video_path, '-o', subtitle_path]
    ccextractor_cmd = ['ffmpeg', '-i', video_path,'>', subtitle_path]

    try:
        result = subprocess.run(ccextractor_cmd, check=True)
        subtitles = result.stdout
        return subtitles
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles: {e}")
        return None
    

def parse_and_search_subtitles(subtitles_file, search_word):
    subs = pysrt.open(subtitles_file, encoding='utf-8')
    matching_segments = []
    segments = []

    for idx, sub in enumerate(subs):
        # print(f"Subtitle {idx + 1}: Start={sub.start}, End={sub.end}")
        # print(sub.text.lower())
        if search_word in sub.text.lower():
            segments.append([sub.start, sub.end])
            matching_segments.append(idx+1)
            

    return matching_segments, segments
