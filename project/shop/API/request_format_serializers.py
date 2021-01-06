from rest_framework import serializers as sz


class MyClosetSerializer(sz.Serializer):
    item = sz.IntegerField()

    class Meta:
        field = [
            'item'
        ]
