from flask import Flask
from flask import request
from flask import send_file
import requests
from flask import json
import copy

app = Flask(__name__)

google_places_key = 'AIzaSyA5Fh7YneQ_XE0yZkSyM4s6E3v2RjpHoCI'
giphy_key = '34ykMUvkDjZNy1UjNhTdUMmpxmvgX9GE'

google_places_api_request = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
giphy_endpoint = 'https://api.giphy.com/v1/gifs/search'

@app.route('/', methods=['POST'])
def getPlacesAndGifs():
    if request.method == 'POST':

        request_json = request.get_json()

        try:
            query = request_json['query']
        except KeyError:
            return 'Json Object must have a key called query'
        if not isinstance(query, basestring):
            return 'Json Object query value must be of type string'

        buildJsonFile(query)
        return send_file('send.json', mimetype='application/json', as_attachment=True)

    return 'Hello World! How are you even at this point\n'

def getPlaces(query):
    payload = {'key':google_places_key, 'query':query}
    gmaps_response = requests.get(google_places_api_request, params=payload)
    return gmaps_response.json()['results']

def getGiphies(gmapsObj):
    giphy_payload = {'api_key': giphy_key, 'q': gmapsObj['name']}
    giphy_response = requests.get(giphy_endpoint, params= giphy_payload)
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
    app.run(debug=True, use_reloader=True)
