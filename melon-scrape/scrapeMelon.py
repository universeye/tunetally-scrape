import requests
import re
from bs4 import BeautifulSoup
import json

URL = {
    'LIVE': 'https://www.melon.com/chart/index.htm',
    'DAY': 'https://www.melon.com/chart/day/index.htm',
    'WEEK': 'https://www.melon.com/chart/week/index.htm',
    'MONTH': 'https://www.melon.com/chart/month/index.htm'
}


def getList(time):
    """Generates json file of the top 100 songs + (additional metadata) on Melon

    Args:
        time (str): Which chart you want (LIVE, RISE, DAY, WEEK, MONTH)

    Returns:
        json (str): Seralized json string that contains the top 100 songs. 
                    Key is ranking of song; value is name, ranking, artists, songId, albumId (id's are Melon specific).  
                                        NOTE: You want to use json.loads(getList("time")) to deseralize the data. 

    """
    html = requests.get(URL[time.upper()], headers={
                        'User-Agent': "github.com/ko28/melon-api"}).text
    soup = BeautifulSoup(html, "lxml")
    data = {}
    # Melon recently changed how their live chart works, tried to fix it as best as I could
    if time.upper() == "LIVE":
        rank = 1
        for tag in soup.findAll("tr", {"data-song-no": True}):
            img_tag = tag.find("img")
            img_url = img_tag['src'] if img_tag else None
            
            data[rank] = {
                "name": tag.find("div", {"class": "ellipsis rank01"}).getText().strip(),
                "artists": tag.find("span", {"class": "checkEllipsis"}).getText(),
                "ranking": rank,
                "songId": re.search(r'goSongDetail\(\'([0-9]+)\'\)', str(tag)).group(1),
                "albumId": re.search(r'goAlbumDetail\(\'([0-9]+)\'\)', str(tag)).group(1),
                "albumImageUrl": img_url,
                "albumTitle": tag.find("div", {"class": "ellipsis rank03"}).find("a").getText().strip()
            }
            rank += 1

    else:
        for tag in soup.findAll("tr", {"class": ["lst50", "lst100"]}):
            img_tag = tag.find("img")
            img_url = img_tag['src'] if img_tag else None
            
            data[tag.find("span", {"class": ["rank top", "rank"]}).getText()] = {
                "name": tag.find("div", {"class": "ellipsis rank01"}).getText().strip(),
                "ranking": tag.find("span", {"class": ["rank top", "rank"]}).getText(),
                "artists": tag.find("span", {"class": "checkEllipsis"}).getText(),
                "songId": re.search(r'goSongDetail\(\'([0-9]+)\'\)', str(tag)).group(1),
                "albumId": re.search(r'goAlbumDetail\(\'([0-9]+)\'\)', str(tag)).group(1),
                "albumImageUrl": img_url,
                "albumTitle": tag.find("div", {"class": "ellipsis rank03"}).find("a").getText().strip()
            }
        # Some data is in Korean, must format with utf-8 to avoid printing out utf code
    return json.dumps(data, ensure_ascii=False).encode('utf-8')


def getLyric(songId):
    url = 'https://www.melon.com/song/detail.htm?songId='+str(songId)
    req = requests.get(
        url, headers={'User-Agent': "github.com/ko28/melon-api"})
    raw = req.text.lower()
    html = raw.replace("<br>", "\n")
    soup = BeautifulSoup(html, "lxml")
    lyric = soup.find("div", {"class": "lyric"})
    payload = {"lyric": lyric.text.strip()}
    return json.dumps(payload, ensure_ascii=False).encode('utf-8')
