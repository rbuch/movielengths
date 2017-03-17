#! /usr/bin/env python3
import http.client
import json
import time
import sys

if len(sys.argv) < 2:
    print("Gotta pass a length, yo")
    sys.exit(1)

length = int(sys.argv[1])
    
conn = http.client.HTTPSConnection("api.themoviedb.org")

with open('moviedb_api', 'r') as f:
    key = f.read().strip()

payload = "{}"

conn.request("GET", "/3/discover/movie?with_runtime.lte={}&with_runtime.gte={}&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&api_key={}".format(length, length, key), payload)

res = conn.getresponse()
data = res.read()

jsonobj = json.loads(data.decode("utf-8"))
total_pages = int(jsonobj["total_pages"])

print("{} total pages.".format(total_pages))

movielist = list(map(lambda x: x["title"], jsonobj["results"]))

for i in range(2, total_pages):
    conn.request("GET", "/3/discover/movie?with_runtime.lte={}&with_runtime.gte={}&include_video=false&include_adult=false&sort_by=popularity.desc&language=en-US&page={}&api_key={}".format(length, length, i, key), payload)

    res = conn.getresponse()
    data = res.read()
    
    jsonobj = json.loads(data.decode("utf-8"))
    movielist = movielist + list(map(lambda x: x["title"], jsonobj["results"]))
    print("Got page {}".format(i))
    # API prohibits requesting more than 40 queries every 10 seconds, so sleep
    if i % 40 == 0:
        time.sleep(10)

with open('{}minutemovies.txt'.format(length), 'w') as f:
    for movie in movielist:
        f.write(movie + "\n")

