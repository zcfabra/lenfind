#!/usr/bin/python3

import os 
import requests
from bs4 import BeautifulSoup
import re
import datetime
import sys

# url = "https://www.youtube.com/playlist?list=PLUkh9m2BorqlDu2zrSN9WZ3xEp3qNgnQj"
# url2 = "https://www.youtube.com/playlist?list=PLwRJQ4m4UJjNymuBM9RdmB3Z9N5-0IlY0"



def main():
    args = sys.argv
    if len(args)!= 2:
        print("Program takes exactly one playlist URL")
        return
    if "playlist" not in args[1]:
        print("Requires a valid playlist URL")
        return

    url = args[1]
    try:
        res = requests.get(url)
    except:
        print("Something went wrong while making the web request")
        return

    # print(res.text)


    bs = BeautifulSoup(res.text, "html.parser")

    text = "".join(bs.find_all(text=True))
    # print(text)

    pat = re.compile(r'(?:\d+:)+\d+')
    matches = re.findall(pat,text)
    refined = [each for ix, each in enumerate(matches) if ix %2 == 0] # returns 2x items for each timecode match --> maybe investigate
    # print(refined)
    total = 0
    for each in refined:
        proc = each.split(":")
        accum = 0
        for ix, each in enumerate(proc[::-1]):
            if ix == 0:
                accum += int(each)
            if ix == 1:
                # print("HIT")
                accum += int(each) * 60
            if ix == 2:
                accum += int(each) * 3600
            if ix == 3:
                accum += int(each) * 216000
        # print(accum)
        total += accum

    # print(total)

    print(f"At 1x Speed: {str(datetime.timedelta(seconds=total)).split('.')[0]}")
    print(f"At 1.5x Speed: {str(datetime.timedelta(seconds=total/1.5)).split('.')[0]}")
    print(f"At 1.75x Speed: {str(datetime.timedelta(seconds=total/1.75)).split('.')[0]}")
    print(f"At 2x Speed: {str(datetime.timedelta(seconds=total//2)).split('.')[0]}")


        



if __name__ == "__main__":
    main()