from flask import Flask,render_template,url_for,request,render_template_string
import urllib3
import pyfacebook
import requests
import json
from json2html import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# reading access token from file
def read_creds(filename):
    with open(filename) as f:
        token = json.load(f)
    return token
token = read_creds('./static/credentials/token.json')
access_token = token['token']

# render resoult page
@app.route('/resoults', methods=['GET','POST'])
def resoults():
    if request.method == 'POST':
        search_term = request.form['search_term']
        lang = request.form['lang']
        search_resoults = requests.get("https://graph.facebook.com/search?type=adinterest&q=["+search_term+"]&limit=10000&locale="+lang+"&access_token="+access_token).json()

        for resoult in search_resoults.items():
            interests = []
            interest_len = len(resoult[1])
            interst_number = interest_len - 1
            x = 0
            order = 1

            # create list of dict with name & size
            while x <= interst_number:
                interests.append({  
                                    'order': str(order),
                                    'name' : resoult[1][x]['name'], 
                                    'size' : str(resoult[1][x]['audience_size']),
                                    'path' : resoult[1][x]['path']
                                })

                # optinal add "topic" if there is one
                if 'topic' in  resoult[1][x]:
                    interests[x]['topic'] = resoult[1][x]['topic']

                # counters +1
                x += 1
                order += 1
    
    # check resoults            
    print(interests)

    # send data to the front
    return render_template('resoults.html', 
                            search_term = search_term, 
                            data = interests,
                            interest_len = interest_len)
# 404 handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True)



