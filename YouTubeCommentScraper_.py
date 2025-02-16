import pandas as pd
import io
from googleapiclient.discovery import build
from flask import Flask, request, render_template, send_file, redirect, url_for
import requests
import gunicorn

# flask constructor
app = Flask(__name__)

api_key = ""
youtube = build('youtube', 'v3', developerKey=api_key) # builds the YouTube API client

# test values
# darpa finance video = oUfgBlfoXk0 (576 comments)
# darpa finance video = HEvRiI2r2lQ (1,140 comments)
# random video = TE66McLMMEw (71 comments)

print("\n")

# gets comments from replies seperately because have to get from .comments rather() than .commentThreads()
def getReplyComments(parent_id, video_id):
    reply_request = youtube.comments().list(part="snippet", parentId=parent_id, maxResults=100)
    reply_response = reply_request.execute()
    listOfReplyDicts = []

    # same like getAllComments but gets all reply comments
    while True:
        for item in reply_response["items"]:
            myDict = {
                "authorDisplayName": item["snippet"]["authorDisplayName"],
                "datePublished": item["snippet"]["publishedAt"],
                "videoId": video_id,
                "likeCount": item["snippet"]["likeCount"],
                "replyCount": 0,
                "text": item["snippet"]["textDisplay"],
            }
            listOfReplyDicts.append(myDict)

        # checks to see if there is a next page. each fetch only gets us a max of 100 comments per response so we must
        # request a next page to generate a new response with another 100 comments. if there is "nextPageToken" in
        # response, that means there are more comments to loop through'''
        if "nextPageToken" in reply_response:
            reply_response = youtube.commentThreads().list(part="snippet", maxResults=100, pageToken=response["nextPageToken"]).execute()
        else:
            break
    return listOfReplyDicts



def getAllComments(my_video_id):
    #youtube API stuff. gets you all the info from comments
    response = youtube.commentThreads().list(part="snippet", videoId=my_video_id, maxResults=100).execute()

    listOfDicts = []
    # loop to go through all the pages
    while True:
        for item in response["items"]: # save each desired key into a list to later put into dataframe
            myDict = {
                "authorDisplayName": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                "datePublished": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                "videoId": item["snippet"]["topLevelComment"]["snippet"]["videoId"],
                "likeCount": item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                "replyCount": item["snippet"]["totalReplyCount"],
                "text": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
            }
            listOfDicts.append(myDict)

            # if there are any replies, get it from getReplyComments
            if (item["snippet"]["totalReplyCount"] > 0):
                parent_id = item["snippet"]["topLevelComment"]["id"]
                replyDictList = getReplyComments(parent_id, my_video_id)
                listOfDicts.extend(replyDictList)

        # checks to see if there is a next page. each fetch only gets us a max of 100 comments per response so we must
        # request a next page to generate a new response with another 100 comments. if there is "nextPageToken" in
        # response, that means there are more comments to loop through'''
        if "nextPageToken" in response:
            response = youtube.commentThreads().list(part="snippet", videoId=my_video_id, maxResults=100, pageToken=response["nextPageToken"]).execute()
        else:
            break

    return listOfDicts

def buildCSV(listOfDicts):
    myFrame = pd.DataFrame(listOfDicts)
    csv_buffer = io.StringIO()
    myFrame.to_csv(csv_buffer, index=False) # this will make it so the csv file saves into memory and not locally
    csv_buffer.seek(0) # moves pointer to start of buffer

    return csv_buffer

def checkValidID(my_video_id):
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={my_video_id}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        return False


# ---------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template("index.html")

# builds what we will call our "main" function. this is where the magic happens between html and python
# flashbacks to hackathon lol
@app.route('/scrape', methods =["GET", "POST"])
def scrape():
    error = None
    # redirect(url_for("scrape"))  # Redirect after download

    if request.method == "POST":
       # getting input with name = video_link in HTML form
       my_video_id = request.form.get("video_link")

       if (checkValidID(my_video_id) == False):
           return render_template("index.html", error="Please enter a valid YouTube link.")

       print("loading")

       myDict = getAllComments(my_video_id)
       csv_buffer = buildCSV(myDict)

       return send_file(
           io.BytesIO(csv_buffer.getvalue().encode()),  # Convert to bytes for download
           mimetype="text/csv",
           as_attachment=True,
           download_name=f"youtube_comments_{my_video_id}.csv"
        )
    return render_template("index.html", error=error)

# ---------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)




