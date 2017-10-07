from flask import Flask
from flask import request
import requests

app = Flask(__name__)

google_places_key = 'AIzaSyA5Fh7YneQ_XE0yZkSyM4s6E3v2RjpHoCI'
giphy_key = '34ykMUvkDjZNy1UjNhTdUMmpxmvgX9GE'

google_places_api_request = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
giphy_endpoint = 'https://api.giphy.com/v1/gifs/search'

@app.route('/', methods=['POST'])
def getData():
    if request.method == 'POST':

        r_json = request.get_json()
        print r_json['query']
        payload = {'key':google_places_key, 'query':r_json['query']}
        gmaps_req = requests.get(google_places_api_request, params=payload)
        print gmaps_req.url
        places = gmaps_req.json()['results']
        print len(places)
        for place in places:
            giphy_payload = {'api_key': giphy_key, 'q': place['name']}
            giphy_req = requests.get(giphy_endpoint, params= giphy_payload)
            giphy_results = giphy_req.json()['data']
            print 'GIPHY RESULTS ********'
            print len(giphy_results)
            for item in giphy_results:
                print 'gif object ******', item
            print place
        return 'Post\n'

    return 'Hello World! How are you even at this point\n'

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
