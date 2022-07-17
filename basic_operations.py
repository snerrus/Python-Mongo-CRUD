import bson # <- Put this line near the start of the file if you prefer.
import datetime   # This will be needed later
import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from a .env file:
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

# Connect to your MongoDB cluster:
client = MongoClient(MONGODB_URI)

# List all the databases in the cluster:
for db_info in client.list_database_names():
   print(db_info)

# Get a reference to the 'sample_mflix' database:
db = client['sample_mflix']

# List all the collections in 'sample_mflix':
collections = db.list_collection_names()
for collection in collections:
   print(collection)

# Import the `pprint` function to print nested data:
from pprint import pprint

# Get a reference to the 'movies' collection:
movies = db['movies']

# Get the document with the title 'Blacksmith Scene':
pprint(movies.find_one({'title': 'Blacksmith Scene'}))

# Insert a document for the movie 'Parasite':
insert_result = movies.insert_one({
      "title": "Sooryavanshi",
      "year": 2020,
      "plot": "Akshay's movie "
      "performed cop role",
      "released": datetime.datetime(2021, 2,7,0,0,0),
   })

# Save the inserted_id of the document you just created:
parasite_id = insert_result.inserted_id
print("_id of inserted document: {parasite_id}".format(parasite_id=parasite_id))

# Look up the document you just created in the collection:
print(movies.find_one({'_id': bson.ObjectId(parasite_id)}))

# Look up the documents you've created in the collection:
for doc in movies.find({
   'year': {
      '$lt': 1920
   }, 
   'genres': 'Romance'
}):
   pprint(doc)

# Update the document with the correct year:
update_result = movies.update_one({ '_id': parasite_id }, {
   '$set': {"year": 2000}
})

# Print out the updated record to make sure it's correct:
pprint(movies.find_one({'_id': bson.ObjectId(parasite_id)}))

# Update *all* the Parasite movie docs to the correct year:
update_result = movies.update_many({"title": "Parasite"}, {"$set": {"year": 2019}})

update_result = movies.delete_many(
   {"title": "Parasite",}
)