
import re

def video_parser(url):
    regex = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
    match = re.match(regex, url)
    return match.group(7) if match and len(match.group(7)) == 11 else "Invalid URL"





