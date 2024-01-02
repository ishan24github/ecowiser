import subprocess
import pysrt

def extract_subtitles(video_path, temp_file):
    ccextractor_cmd = ['ccextractor', video_path, '-o', temp_file]

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
