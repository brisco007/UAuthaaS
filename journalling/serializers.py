#we will use the django rest for these elements
from rest_framework import serializers
from .models import Journal

class JournalSerialiser(serializers.HyperlinkedModelSerializer):
    '''
    here i will create the methods to manipulate forfaits, and in the models, i will write
    the methods to modify forfaits just before database modification
    '''
    class Meta:
        model = Journal
        fields = ("id","recordedOn","record","userId")
