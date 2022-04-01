from flask import Flask, render_template, request, Response, jsonify

import firebase_admin
import requests
import json
import os

from firebase_admin import firestore
from firebase_admin import credentials

app = Flask(__name__)

navlist = [{"name": "Home", "link": "/"}, {"name": "About", "link": "/about"}]
# devlist = [
#     {"name": "Arban Hossain", "profile": "https://github.com/arbanhossain"},
#     {"name": "Nabil", "profile": "https://github.com/nirobnabil"}
# ]

cred = credentials.Certificate(requests.get(os.environ['GOOGLE_APPLICATION_CREDENTIALS']).json())
firebase_admin.initialize_app(cred)
db = firestore.client()
sites_ref = db.collection('devsite')

@app.route("/")
def index():
    docs = sites_ref.stream()
    dev_list = [doc.to_dict() for doc in docs]
    return render_template('home.html', title="Home", nav_list=navlist, dev_list=dev_list)

@app.route("/about")
def about():
    return render_template('about.html', title="About", nav_list=navlist)

@app.route("/fetch")
def fetch():
    if request.args.get('pass') != os.environ['passwd']:
        print(request.args.get('pass'))
        return Response(status=403)
    trending_devs = requests.get('https://ghtrendingapi.herokuapp.com/developers')
    docs = sites_ref.stream()
    existing_devs = [doc.to_dict() for doc in docs]
    for item in trending_devs.json():
        dev = item['username']
        if dev not in [i['handle'] for i in existing_devs]:
            dev_details = requests.get('https://api.github.com/users/' + dev, headers={'Authorization': f"Bearer {os.environ['GITHUB_TOKEN']}"})
            if 'message' in dev_details.json():
                return Response(dev_details.json()['message'], status=500)
            if dev_details.json()['blog'] == '': pass
            else:
                dic = {}
                dic['name'] = dev_details.json()['name']
                dic['site'] = 'https://' + dev_details.json()['blog'] if (dev_details.json()['blog'].count('https://') == 0 and dev_details.json()['blog'].count('http://')==0) else dev_details.json()['blog']
                dic['profile'] = dev_details.json()['html_url']
                dic['handle'] = dev
                doc_ref = sites_ref.document(dev)
                doc_ref.set(dic)
    return Response(status=200)

@app.route("/environ")
def environ():
    return 'No environ'

if __name__ == "__main__":
    app.run()