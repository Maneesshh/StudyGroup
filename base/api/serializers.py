from rest_framework.serializers import ModelSerializer
from base.models import Room, VideoStatus

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class VideoStatusSerializer(ModelSerializer):
    class Meta:
        model = VideoStatus
        fields = '__all__'
