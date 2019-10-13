from mongoengine import *

# Create your models here.

class Poem(Document):
    """docstring for Poem"""
    meta = {
        'collection':'poem_date'
    }
    poem_id = SequenceField(required=True, primary_key = True)
    author = StringField()
    title = StringField()

