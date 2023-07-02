
import re

def video_parser(url):
    regex = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
    match = re.match(regex, url)
    print(match, url)
    return match.group(7) if match and len(match.group(7)) == 11 else "Invalid URL"



# Testing
url_list = [ "http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index",
    "http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/0zM3nApSvMg",
    "http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0",
    "http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s",
    "http://www.youtube.com/embed/0zM3nApSvMg?rel=0",
    "http://www.youtube.com/watch?v=0zM3nApSvMg",
    "http://youtu.be/0zM3nApSvMg"]

for i in url_list:
    print(video_parser(i))
    if video_parser(i)!="0zM3nApSvMg":
        print(i)
        print("Error")


