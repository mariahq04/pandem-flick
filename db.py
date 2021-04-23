import pymongo
from pymongo import MongoClient


class DB:
    def __init__(self):
        # sets up connection to cluster
        self.cluster = MongoClient(
            "mongodb+srv://pfAdmin:ZZ68174@cluster0.pdcfd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

        # assigns database
        self.db = self.cluster["PandemFlickBot"]

        # assigns collection (a minidatabase within the larger database)
        self.collection = self.db["movies"]

        # post resemble a python dictionary when working with them in python
        # they always have an id tag that you use to access posts (_id)

    # inserts a single item into movies collection
    # need: update to add more than one entry at a time
    def insert(self, x):
        self.collection.insert_one(x)

    # searches collection, ignores case
    # returns python dictionary
    def find(self, query):

        results = self.collection.find({"title": {"$regex": query, "$options": 'i'}})

        return results
