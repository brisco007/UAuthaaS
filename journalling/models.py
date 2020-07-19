from django.db import models
import uuid
# Create your models here.
class Journal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.CharField(max_length=254)
    userId = models.UUIDField(default=uuid.uuid4, editable=True)
    recordedOn = models.DateTimeField(auto_now=True)
    #methods
    def __str__(self):
        return "["+str(self.recordedOn)+"]" + " : "+ str(self.userId)+" did " + str(self.record)
