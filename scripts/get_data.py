import requests
import json
from pyyoutube import Api
 
key = "AIzaSyD-ZE3mSmd5QDLFCQVCcHSypaXuNROHnV0"
api = Api(api_key=key)
 
query = "'Mission Impossible'"
video = api.search_by_keywords(q=query, search_type=["video"], count=10, limit=30)
 
maxResults = 100
nextPageToken = ""
s = 0
 
for id_ in [x.id.videoId for x in video.items]:
    uri = "https://www.googleapis.com/youtube/v3/commentThreads?" + \
            "key={}&textFormat=plainText&" + \
            "part=snippet&" + \
            "videoId={}&" + \
            "maxResults={}&" + \
            "pageToken={}"
    uri = uri.format(key, id_, maxResults, nextPageToken)
    content = requests.get(uri).text
    data = json.loads(content)
    for item in data['items']:
        s += int(item['snippet']['topLevelComment']['snippet']['likeCount'])
 
with open('/home/angry/mlops_3/datasets/data.csv', 'a') as f:
    f.write("{}\n".format(s)) 
