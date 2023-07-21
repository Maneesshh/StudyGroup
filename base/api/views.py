from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from base.models import Room, VideoStatus, User
from .serializers import RoomSerializer , VideoStatusSerializer
from base.constants import Status
from django.utils import timezone
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request,pk):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)

# @api_view(['POST'])
# def roomCallStatusActive(request):
#     print(request.data.get('roomId'))
         
#     room = Room.objects.get(id=request.data.get('roomId'))
#     host = User.objects.get(id=request.data.get('hostId')) 
#     try:
#             video_status = VideoStatus.objects.get(room=room)
#             # VideoStatus object exists, update the fields
#             video_status.host = host
#             video_status.status = Status.ACTIVE
#             video_status.save()
#     except VideoStatus.DoesNotExist:
#     # VideoStatus object does not exist, create a new one
#             video_status = VideoStatus.objects.create(room=room, host=host, status=Status.ACTIVE)
#             # video_status, created = VideoStatus.objects.get_or_create(
#             #     room=room,
#             #     host= host,
#             #     status = Status.ACTIVE
#             # ) 
#             # if not created:
#             #     # VideoStatus object already exists, update the fields
#             #     video_status.host = host
#             #     video_status.status = Status.ACTIVE
#             #     video_status.save() 
#             # VideoStatus.objects.create(
#             #     room = room,
#             #     host = host,
#             #     status = Status.ACTIVE,      
#             # )    
#             # if(room.call_status == Status.INACTIVE):
#             #     room.call_status = Status.ACTIVE
#             # room.save()
#     return Response(status=200) 

@api_view(['POST'])
def roomCallStatusActive(request):
    try:
        room_id = request.data.get('roomId')
        host_id = request.data.get('hostId')
        if not room_id or not host_id:
            raise ValidationError("roomId and hostId must be provided.")
        
        room = Room.objects.get(id=room_id)
        host = User.objects.get(id=host_id)
        
        try:
            video_status = VideoStatus.objects.get(room=room)
            # VideoStatus object exists, update the fields
            video_status.host = host.name
            video_status.status = Status.ACTIVE
            video_status.save()
        except ObjectDoesNotExist:
            video_status = VideoStatus.objects.create(room=room, host=host.name, status=Status.ACTIVE)
        
        return Response(status=200)
    
    except (ValidationError, ObjectDoesNotExist) as e:
        return Response({'error': str(e)}, status=400)
    
    except Exception as e:
        # Handle any other exceptions or errors that may occur
        # Log the error or return an appropriate response
        print(f"Error occurred: {str(e)}")
        return Response({'error': 'Internal Server Error'}, status=500)

@api_view(['POST'])
def roomCallStatusInactive(request):
    try:
       
        room_id = request.data.get('roomId')
        host_id = request.data.get('hostId')
       
        if not room_id or not host_id:
            raise ValidationError("roomId and hostId must be provided.")
        
        room = Room.objects.get(id=room_id)
        host = User.objects.get(id=host_id)
        
        try:
            video_status = VideoStatus.objects.get(room=room)
            # VideoStatus object exists, update the fields
            if video_status.host == host.name:
              video_status.host = host.name
              video_status.status = Status.INACTIVE
              video_status.ended = timezone.now()
              video_status.save()
            else:
                raise ValidationError("Only can change status.")
                  
        except ObjectDoesNotExist:
            return Response(status=404)
        
        return Response(status=200)
    
    except (ValidationError, ObjectDoesNotExist) as e:
        return Response({'error': str(e)}, status=400)
    
    except Exception as e:
        # Handle any other exceptions or errors that may occur
        # Log the error or return an appropriate response
        print(f"Error occurred: {str(e)}")
        return Response({'error': 'Internal Server Error'}, status=500)

@api_view(['GET'])
def getVideoStatus(request,pk):
    try: 
        room = get_object_or_404(Room, id=pk)
        video = VideoStatus.objects.get(room=room)
        if video is None:
           return Response(status=404) 
        serializer = VideoStatusSerializer(video, many=False)
        return JsonResponse(serializer.data)
    except VideoStatus.DoesNotExist:
        return Response(status=404)


