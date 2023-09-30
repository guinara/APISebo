import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
APIKey = 'qCLhKKgjcuhDM16reW2cdjAYmBHO9csVC8gUU8eyM63nq1Gl2MpUPNZNO0zyTWQY'
uri='mongodb+srv://user:password415@sebopdw.0dlksoe.mongodb.net/'

# Create a new client and connect to the server
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
