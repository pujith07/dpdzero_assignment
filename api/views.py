from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,permissions
from api.models import User_Data,Stored_data
from api.serializers import UserData_Serializer,Stored_data_Serializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import Http404


@api_view(['POST'])
def register_user(request):
    serializer = UserData_Serializer(data=request.data)
    if serializer.is_valid():
        user_data = serializer.validated_data
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        user.save()
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "User successfully registered!",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            "status": "error",
            "code": "INVALID_REQUEST",
            "message": "Invalid request. Please provide all required fields: username, email, password, full_name."
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def generate_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "status": "success",
                "message": "Access token generated successfully.",
                "data": {
                    "access_token": token.key,
                    "expires_in": 3600 
                }
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "status": "error",
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid credentials. The provided username or password is incorrect."
        },
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
def store_data(request):
    # Check if the request contains the 'Authorization' header with the token
    if not request.user.is_authenticated:
        return Response(
            {
                "status": "error",
                "code": "INVALID_TOKEN",
                "message": "Invalid access token provided"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    key = request.data.get('key')
    value = request.data.get('value')

    if not key:
        return Response(
            {
                "status": "error",
                "code": "INVALID_KEY",
                "message": "The provided key is not valid or missing."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if not value:
        return Response(
            {
                "status": "error",
                "code": "INVALID_VALUE",
                "message": "The provided value is not valid or missing."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    
    Stored_data.objects.create(key=key, value=value)

    return Response(
        {
            "status": "success",
            "message": "Data stored successfully."
        },
        status=status.HTTP_201_CREATED
    )

class DataDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Require authentication for access

    def get_data_object(self, key):
        try:
            return Stored_data.objects.get(key=key)
        except Stored_data.DoesNotExist:
            return Http404

    def get(self, request, key):
        data_object = self.get_data_object(key)
        if not data_object:
            return Response(
                {"status": "error", "code": "KEY_NOT_FOUND", "message": "The provided key does not exist in the database."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = Stored_data_Serializer(data_object)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, key):
        if not request.user.is_authenticated:
            return Response(
                {"status": "error", "code": "UNAUTHORIZED", "message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data_object = self.get_data_object(key)
        if not data_object:
            return Response(
                {"status": "error", "code": "KEY_NOT_FOUND", "message": "The provided key does not exist in the database."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer =Stored_data_Serializer(data_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Data updated successfully."}, status=status.HTTP_200_OK)
        return Response(
            {"status": "error", "code": "INVALID_REQUEST", "message": "Invalid request. Please provide valid data."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, key):
        if not request.user.is_authenticated:
            return Response(
                {"status": "error", "code": "UNAUTHORIZED", "message": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data_object = self.get_data_object(key)
        if not data_object:
            return Response(
                {"status": "error", "code": "KEY_NOT_FOUND", "message": "The provided key does not exist in the database."},
                status=status.HTTP_404_NOT_FOUND
            )

        data_object.delete()
        return Response({"status": "success", "message": "Data deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
