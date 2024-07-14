import string
from flask import Flask, request, render_template, redirect
import random
import json

app = Flask(__name__)

#To keep check if shot url generated already exist or not.
all_short_url = {}

def get_short_url():
    chars = string.ascii_letters
    digits = string.digits
    characters = chars + digits
    short_url = ""
    #Fixing the length of the shortened url to 10. And randonly choosing the character from characters.
    for i in range(10):
        short_url += "".join(random.choice(characters))
    return short_url

@app.route("/", methods = ['GET','POST'])
def short_url_func():
    if request.method == 'POST':
        long_url = request.form["long_url"]

        #Check if long url already exist in system.
        for url in all_short_url:
            if all_short_url[url] == long_url:
                return render_template("index.html", Message = f"Shortened Url is :{request.url_root}{url}")

        #Generating new shorl url and then appending it to dictionary.
        short_url = get_short_url()
        while short_url in all_short_url:
            short_url = get_short_url()

        all_short_url[short_url] = long_url

        #This is used to save the enetered long and generated short url in a json file.
        with open("all_urls.json", "w") as f:
            json.dump(all_short_url, f)

        return render_template("index.html", Message = f"Shortened url is : {request.url_root}{short_url}")
    else:
        return render_template("index.html")

#Now when given short_url is tried in new tab, it will redirect to the original long url.
@app.route("/<short_url>")
def get_long_url(short_url):
    if short_url in all_short_url:
        return redirect(all_short_url[short_url])
    else:
        return "Url not found", 404

#Loading all the content of json file into dictionary.
if __name__ == '__main__':
    with open("all_urls.json", "r") as f:
        all_short_url = json.load(f)
    app.run(debug = True)
