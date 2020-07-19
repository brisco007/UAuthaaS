from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from .serializers import ForfaitSerialiser, CompteUserSerialiser
from .models import Forfait, CompteUser

# viewsets of forfaits and compte users


class ForfaitView(APIView):
    serializer_class = ForfaitSerialiser
    def get(self, request):
        forfaitList = Forfait.objects.all().order_by('nom')
        serializedForfaits = ForfaitSerialiser(forfaitList, many=True)
        return Response(serializedForfaits.data, status=status.HTTP_200_OK)

    def post(self, request):
            serializedForfait = ForfaitSerialiser(data=request.data)
            if serializedForfait.is_valid():
                serializedForfait.save()
                return Response(serializedForfait.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializedForfait.errors, status=status.HTTP_400_BAD_REQUEST)


class ForfaitDetailsView(APIView):
    def get_object(self, id):
        try:
            return Forfait.objects.get(pk=id)
        except Forfait.DoesNotExist:
            raise Http404

    def get(self, request, id):
        forfait = self.get_object(id)
        serializedForfait = ForfaitSerialiser(forfait)
        return Response(serializedForfait.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        forfait = self.get_object(id)
        serializedForfait = ForfaitSerialiser(forfait, data=request.data)
        if serializedForfait.is_valid():
            serializedForfait.save()
            return Response(serializedForfait.data, status=status.HTTP_200_OK)
        else:
            return Response(serializedForfait.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        forfait = self.get_object(id)
        forfait.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompteUserView(APIView):
    def get(self, request):
        comptesList = CompteUser.objects.all().order_by('userId')
        serializedComptes = CompteUserSerialiser(comptesList, many=True)
        return Response(serializedComptes.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializedCompte = CompteUserSerialiser(data=request.data)
        if serializedCompte.is_valid():
            serializedCompte.save()
            return Response(serializedCompte.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializedCompte.errors, status=status.HTTP_400_BAD_REQUEST)


class CompteUserDetailsUserView(APIView):
    def get_object(self, userid):
        try:
            return CompteUser.objects.filter(userId=userid).first()
        except CompteUser.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        compte = self.get_object(userid)
        serializedCompte = CompteUserSerialiser(compte)
        return Response(serializedCompte.data, status=status.HTTP_200_OK)

    def put(self, request, userid):
        compte = self.get_object(userid)
        serializedCompte = CompteUserSerialiser(compte)
        serializedCompte.update(compte, request.data)
        return Response(serializedCompte.data, status=status.HTTP_200_OK)
        """    serializedCompte = CompteUserSerialiser(compte,data=request.data)
        if serializedCompte.is_valid():
          
        else:
            return Response(serializedCompte.errors,status=status.HTTP_400_BAD_REQUEST)
        """

    def delete(self,request,userid):
        compte = self.get_object(id)
        compte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
              
class CompteUserDetailsView(APIView):
    def get_object(self,id):
        try:
            return CompteUser.objects.get(pk=id)
        except CompteUser.DoesNotExist:
            raise Http404

    def get(self,request,id):        
        compte= self.get_object(id)
        serializedCompte = CompteUserSerialiser(compte)
        return Response(serializedCompte.data,status=status.HTTP_200_OK)    
    
    def put(self,request,id):
        compte = self.get_object(id)
        serializedCompte = CompteUserSerialiser(compte,data=request.data)
        if serializedCompte.is_valid():
            serializedCompte.save()
            return Response(serializedCompte.data,status=status.HTTP_200_OK)
        else:
            return Response(serializedCompte.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,id):
        compte = self.get_object(id)
        compte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
              
        
