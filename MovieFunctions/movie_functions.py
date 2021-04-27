import http.client
import string
import json
from MovieFunctions import movie_functions

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "7370d66108msh075650f3a47a6a8p148fb0jsne3f707ea2d26",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
}


# Sets up HTTPS connection
def get_data(title):
    title = title.replace(" ", "%20")
    conn.request("GET", "/title/find?q=" + title, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)

    return data


def get_ratings(movie_id):
    conn.request("GET", "/title/get-ratings?tconst=" + movie_id, headers=headers)

    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)
    rating = data['rating']
    print(rating)

    return rating


def get_id(title):
    title = title.replace(" ", "%20")
    conn.request("GET", "/title/find?q=" + title, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)
    movie_id = data['results'][0]['id'][7:-1]

    return movie_id


def get_genres(_id):
    conn.request("GET", "/title/get-genres?tconst=" + _id, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)

    return data


def get_plot(_id):
    conn.request("GET", "/title/get-plots?tconst=" + _id, headers=headers)
    # This converts json into dictionary to use in python
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print(data)
    plot = data['plots'][0]['text']

    return plot


def search(query, collection):
    # searches for movie in database first
    # search only works for titles
    # ignores case, exact match
    results = collection.find_one({"title": {"$regex": '^' + query + '$', "$options": 'i'}})

    if results is None:
        data = movie_functions.get_data(query)
        _id = data['results'][0]['id'][7:-1]
        genres = movie_functions.get_genres(_id)
        genres = ", ".join(genres)

        movie = {"_id": data['results'][0]['id'][7:-1],
                 "title": data['results'][0]['title'],
                 "category": data['results'][0]['titleType'],
                 "genres": genres,
                 "rating": movie_functions.get_ratings(_id),
                 "web_url": 'https://www.imdb.com/title/' + _id,
                 "image_url": data['results'][0]['image']['url'],
                 "time": data['results'][0]['runningTimeInMinutes'],
                 "plot": movie_functions.get_plot(_id)
                 }

        # checks if movie id is already in database before trying to add it
        id_check = collection.find_one({'_id': movie['_id']})
        if id_check is None:
            collection.insert_one(movie)
    else:

        movie = {"_id": results['_id'],
                 "title": results['title'],
                 "category": results['category'],
                 "genres": results['genres'],
                 "rating": results['rating'],
                 "web_url": results['web_url'],
                 "image_url": results['image_url'],
                 "time": results['time'],
                 "plot": results['plot']
                 }

    return movie
