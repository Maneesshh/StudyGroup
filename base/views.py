from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message, User, Media
from django.urls import resolve
from django.contrib.auth import authenticate, login, logout

from .forms import RoomForm, UserForm, MyUserCreationForm
# for forgotpw
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from base.models import User


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email address.')
            return redirect('reset-password')

        # Generate the password reset token
        token = default_token_generator.make_token(user)

        # Build the reset password email
        reset_url = request.build_absolute_uri(
            f'/reset-password/confirm/{user.pk}/{token}/'
        )
        mail_subject = 'Reset your password'
        message = f'Please click the following link to reset your password:\n\n{reset_url}'
        send_mail(mail_subject, message, 'from@example.com', [email])

        messages.success(request, 'Password reset email has been sent.')
        return redirect('login')

    return render(request, 'base/forgot_password.html')
# forgotpw completed

 # handle user login


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username or password does not exist")

    context = {'page': page}
    return render(request, 'base/login_registration.html', context)

# handle user logout


def logoutUser(request):
    logout(request)
    return redirect('login')

# handle user registration


def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'User register successfully')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_registration.html', context)


# home page
@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )
    topics = Topic.objects.all()[0:4]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)

# room view


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()

    if request.method == 'POST':
        file = request.FILES.get('file')
        msg = request.POST.get('body')

        if file is None and msg is "":
            messages.warning(request, 'message is empty')

        message = Message.objects.create(
            user=request.user,
            room=room,
            body=msg
        )
        if file:
            media = Media.objects.create(
                message=message,
                media_name=file.name,
                media_type=file_type(file),
                media_size=file.size,
                media_path=file
            )

        room.participants.add(request.user)
        return redirect('room', pk=room.id)

     # Retrieve messages with associated media
    messages_with_media = Message.objects.filter(
        room=room, media__isnull=False)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants, 'messages_with_media': messages_with_media}
    return render(request, 'base/room.html', context)

# profile view


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'topics': topics, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)

# create room


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        messages.success(request, 'room created successfully')
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

# update room


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        messages.success(request, 'room updated successfully')
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

# delete room


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'room deleted successfully')
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

# deleted message


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'message deleted successfully')
        return redirect('room', pk=message.room.id)
    return render(request, 'base/delete.html', {'obj': message})

# update user


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'user updated successfully')
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', {'form': form})

# To get topics


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

# to get activity


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)

# redirect to chat room


def chatRoom(request, room):

    context = {'roomId': room}
    return render(request, 'GroupChat/room.html', context)

# to identify file type


def file_type(file):
    file_type = file.content_type
    if file_type.startswith('image'):
        return 'Image'
    elif file_type == 'application/pdf':
        return 'PDF'
    elif file_type == 'application/msword' or file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return 'DOC'
    elif file_type == 'application/xml' or file_type == 'text/xml':
        return 'XML'
    elif file_type == 'application/vnd.ms-excel' or file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return 'Excel'
    elif file_type.startswith('video'):
        return 'Video'
    else:
        return 'Unknown'


def check_remote_user_active(request, user_id):
    try:
        user = User.objects.get(id=user_id)  # Assuming you have the user ID
        is_active = user.is_active
        return JsonResponse({'is_active': is_active})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'})
