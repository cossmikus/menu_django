from django.shortcuts import render

# Create your views here.
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import User
# from .serializers import UserSerializer

# # Create your views here.

# #get all users
# @api_view(['GET'])
# def getUsers(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# #get single user
# @api_view(['GET'])
# def getUser(request, pk):
#     user = User.objects.get(id=pk)
#     serializer = UserSerializer(user, many=False)
#     return Response(serializer.data)

# #add user
# @api_view(['POST'])
# def addUser(request):
#     serializer = UserSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# #update user
# @api_view(['PUT'])
# def updateUser(request, pk):
#     user = User.objects.get(id=pk)
#     serializer = UserSerializer(instance=user, data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# #delete user
# @api_view(['DELETE'])
# def deleteUser(request, pk):
#     user = User.objects.get(id=pk)
#     user.delete()

#     return Response('Item successfully deleted!')
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, The_Admin, The_Trainer, The_Client
from .serializers import (
    UserSerializer,
    AdminSerializer,
    TrainerSerializer,
    ClientSerializer,
    ScheduleSerializer,
    UserSerializerNames
)
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login

# import jwt
# import jwt


@api_view(["GET"])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(["POST"])
def addUser(request):
    # Hash the password before saving
    request.data["password"] = make_password(request.data["password"])

    # Initialize the User serializer with request data
    user_serializer = UserSerializer(data=request.data)

    if user_serializer.is_valid():
        # Save the User instance
        user = user_serializer.save()

        # Based on the user_role, create the corresponding role instance
        user_role = request.data["user_role"]
        if user_role == "admin":
            The_Admin.objects.create(user=user)
        elif user_role == "trainer":
            The_Trainer.objects.create(user=user)
        elif user_role == "client":
            The_Client.objects.create(user=user)

        return Response(user_serializer.data)
    else:
        return Response(user_serializer.errors, status=400)


@api_view(["PUT"])
def updateUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def deleteUser(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response("Item successfully deleted!")


@api_view(["GET"])
def getAdmin(request):
    admin = The_Admin.objects.all()
    serializer = AdminSerializer(admin, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getTrainer(request):
    trainer = The_Trainer.objects.all()
    serializer = TrainerSerializer(trainer, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getClient(request):
    client = The_Client.objects.all()
    serializer = ClientSerializer(client, many=True)
    return Response(serializer.data)


from django.contrib.auth.hashers import check_password
from rest_framework import status
from .models import User
import jwt

@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        # Find user by email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # If user does not exist, return error response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the password matches
    if check_password(password, user.password):
        token_payload = {
            "user_id": user.id,
            "user_role": user.user_role
        }
        print(user.id)
        token = jwt.encode(token_payload, settings.SECRET_KEY)

        # Return success response with token
        return Response({"token": token})
        # Password matches, return success response
        #return Response("User authenticated successfully")
    else:
        # Password doesn't match, return error response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
from rest_framework import status
from django.conf import settings


@api_view(["GET"])
def getTrainerNames(request):
    # Authenticate the user using JWT
    # Check user's role from the JWT token's payload
    try:
        # Decode token to get the payload
        token = request.headers.get('Authorization', None).split(' ')[1]  # Extract the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        user_role = payload.get('user_role', '')

        # Check if the user role is either 'client' or 'admin'
        if user_role in ['client', 'admin', 'trainer']:
            # Fetch trainers from User model where user_role is 'trainer'
            trainers = User.objects.filter(user_role='trainer', name='azamat')
            # Prepare response data
            data = [{
                'name': trainer.name,  # Assuming username field exists
                'email': trainer.email,
                'trainer_id': trainer.id
            } for trainer in trainers]
            return Response(data)
        else:
            # If the user role is not 'client' or 'admin', respond with permission denied
            return Response({'error': 'You do not have permission to view this information.'}, status=status.HTTP_403_FORBIDDEN)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Authentication token is expired.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.DecodeError:
        return Response({'error': 'Error decoding token.'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(["GET"])
def getClientsInfo(request):
    # Retrieve all clients
    clients = The_Client.objects.all()
    
    # Retrieve user ids associated with clients
    user_ids = [client.user_id for client in clients]

    # Retrieve users based on the user ids
    users = User.objects.filter(id__in=user_ids)

    # Serialize the data
    serializer = UserSerializerNames(users, many=True)
    
    return Response(serializer.data)

    
from rest_framework import status
from .models import Schedule, The_Trainer, The_Client, User


@api_view(["POST"])
def addSchedule(request):
    trainer_id = request.data.get("trainer")
    client_id = request.data.get("client")
    # date = request.data.get("date")
    # time = request.data.get("time")
    # description = request.data.get("description")

    # Check if the trainer exists
    try:
        trainer = The_Trainer.objects.get(pk=trainer_id)
    except The_Trainer.DoesNotExist:
        return Response({"error": f"The trainer with id {trainer_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the client exists
    try:
        client = The_Client.objects.get(pk=client_id)
    except The_Client.DoesNotExist:
        return Response({"error": f"The client with id {client_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    # Create the serializer instance with the request data
    serializer = ScheduleSerializer(data=request.data)

    # Validate the serializer data
    if serializer.is_valid():
        # Save the validated data to create the schedule
        serializer.save(trainer=trainer, client=client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def getAllSchedules(request):
    schedules = Schedule.objects.all()
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getScheduleTrainer(request, pk):
    # Retrieve schedules based on the trainer id
    schedules = Schedule.objects.filter(trainer=pk)
    # Serialize the data
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getScheduleClient(request, pk):
    # Retrieve schedules based on the client id
    schedules = Schedule.objects.filter(client=pk)
    # Serialize the data
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)
