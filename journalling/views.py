from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from .serializers import JournalSerialiser
from .models import Journal

#viewsets of forfaits and compte users

class JournalView(APIView):
    def get(self,request):        
        journalList = Journal.objects.all().order_by("userId")
        serializedjournals = JournalSerialiser(journalList,many=True)
        return Response(serializedjournals.data,status=status.HTTP_200_OK)
        
    def post(self,request):
            serializedJournal = JournalSerialiser(data=request.data)
            if serializedJournal.is_valid():
                serializedJournal.save()
                return Response(serializedJournal.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializedJournal.errors,status=status.HTTP_400_BAD_REQUEST)
            
class JournalDetailsView(APIView):
    def get_object(self,id):
        try:
            return Journal.objects.get(pk=id)
        except Journal.DoesNotExist:
            raise Http404

    def get(self,request,id):        
        journal = self.get_object(id)
        serializedJournal = JournalSerialiser(journal)
        return Response(serializedJournal.data,status=status.HTTP_200_OK)    
    
    def put(self,request,id):
        journal = self.get_object(id)
        serializedJournal = JournalSerialiser(journal,data=request.data)
        if serializedJournal.is_valid():
            serializedJournal.save()
            return Response(serializedJournal.data,status=status.HTTP_200_OK)
        else:
            return Response(serializedJournal.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,id):
        journal = self.get_object(id)
        journal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)