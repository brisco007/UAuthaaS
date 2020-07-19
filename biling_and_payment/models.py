from django.db import models
import uuid
from django.utils import timezone
# Create your models here.
class Forfait(models.Model):
    #fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=26,unique=True)
    valeur = models.DecimalField(max_digits=8,decimal_places=2)
    expire_days = models.PositiveIntegerField(default = 1)
    #methods
    def __str__(self):
        return self.nom + " = "+ str(self.valeur)+" Mo, " + "il a une validité de "+str(self.expire_days)+" jours"

class CompteUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solde = models.DecimalField(max_digits=7,decimal_places=2)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now=True)
    date_activation = models.DateTimeField(default = timezone.now)
    date_expiration = models.DateTimeField(default = timezone.now)
    nom_forfait = models.CharField(max_length=25,default="aucun forfait")
    userId =  models.UUIDField(editable=True)
    def __str__(self):
        return "compte de "+ str(self.userId) + ", "+ "forfait : " +self.nom_forfait+", solde: "+str(self.solde)+" Mo, "+ "compte actif" if self.actif else "compte de "+str(self.userId)+" inactif"
