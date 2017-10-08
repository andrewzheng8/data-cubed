from flask import Flask
from flask import request
from flask import send_file
from flask import json
import requests
import copy

from boto.s3.connection import S3Connection

s3 = S3Connection(os.environ['GMAPS_KEY'], os.environ['GIPHY_KEY'])

app = Flask(__name__)


GMAPS_API = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
GIPHY_API = 'https://api.giphy.com/v1/gifs/search'

@app.route('/', methods=['POST'])
def getPlacesAndGifs():
    if request.method == 'POST':

        request_json = request.get_json()

        try:
            query = request_json['query']
        except KeyError:
            return 'Request body json must have a key called query'
        if not isinstance(query, basestring):
            return 'query key in the request body json must point to a value of type string'

        buildJsonFile(query)
        return send_file('send.json', mimetype='application/json')

    return 'Hello World! How are you even at this point\n'

def getPlaces(query):
    payload = {'key':GMAPS_KEY, 'query':query}
    gmaps_response = requests.get(GMAPS_API, params=payload)
    return gmaps_response.json()['results']

def getGiphies(gmapsObj):
    giphy_payload = {'api_key': GIPHY_KEY, 'q': gmapsObj['name']}
    giphy_response = requests.get(GIPHY_API, params= giphy_payload)
    giphy_results = giphy_response.json()['data']
    return giphy_results

def buildJsonObject(gmapsResults):
    gmapsCopy = copy.deepcopy(gmapsResults)
    for result in gmapsCopy:
        result['giphies'] = getGiphies(result)
    return gmapsCopy

def buildJsonFile(query):
    places = getPlaces(query)
    withGiphies = buildJsonObject(places)
    with open('send.json', 'w') as json_file:
        json.dump(withGiphies, json_file)
        json_file.close()


if __name__ == '__main__':
    app.run()
