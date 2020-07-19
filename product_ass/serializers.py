from rest_framework.serializers import Serializer, CharField, BooleanField


class ServiceSerializer(Serializer):
    bearerOnly = BooleanField(default=True)
    clientId = CharField()
    name = CharField(required=True)
    description = CharField()
    rootUrl = CharField()
    secret = CharField(required=False)

    def validate(self, data):
        return data
