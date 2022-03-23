from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

navlist = [{"name": "Home", "link": "/"}, {"name": "About", "link": "/about"}]
devlist = [
    {"name": "Arban Hossain", "profile": "https://github.com/arbanhossain"},
    {"name": "Nabil", "profile": "https://github.com/nirobnabil"}
]

@app.route("/")
def hello_world():
    response = requests.get('https://api.sheety.co/39d37f14ef4edbd7f56fecb81e0f81ca/githubDev/devsite')
    return render_template('home.html', title="Home", nav_list=navlist, dev_list=response.json()['devsite'])

@app.route("/fetch")
def fetch():
    response = requests.get('https://gh-trending-api.herokuapp.com/developers')
    print(response.json())
    return Response(status=200)

if __name__ == "__main__":
    app.run()