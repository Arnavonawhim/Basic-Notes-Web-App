from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Note
from .serializers import UserSerializer, NoteSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new account",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username (3-20 characters, letters, numbers, underscores only)'),'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password (min 8 chars, must include uppercase, lowercase, number, special char)'),},
        ),
        responses={
            201: openapi.Response(description="Account was created",
                examples={"application/json": {"message": "Account created","user": {"id": 1,"username": "john_doe","email": "john@example.com"},"refresh": "eyJ0eXAiOiJKV1QiLCJh...","access": "eyJ0eXAiOiJKV1QiLCJh..."}}
            ),
            400: openapi.Response(
                description="Bad request - validation errors",
                examples={"application/json": { "username": ["Make Username above 3 chrar"],"password": ["Password must contain at least one uppercase letter"]}
                }
            ),
        }
    )
    def post(self, request):
        user_data = UserSerializer(data=request.data)
        if user_data.is_valid():
            new_user = user_data.save()
            user_token = RefreshToken.for_user(new_user)
            return Response({'message': 'Account created','user': user_data.data,'refresh': str(user_token),'access': str(user_token.access_token),},
            status=status.HTTP_201_CREATED)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login with username and password to get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),},
        ),
        responses={200: openapi.Response(
                description="Login successful",
                examples={"application/json": {"message": "Login Successful","refresh": "eyJ0eXAiOiJKV1QiLCJh...","access": "eyJ0eXAiOiJKV1QiLCJh..."}
                }
            ),
            400: openapi.Response(
                description="Missing credentials",
                examples={"application/json": {"error": "Provide both username and password"}}
            ),
            401: openapi.Response(
                description="Invalid credentials",
                examples={"application/json": {"error": "Wrong Username"}}),
        }
    )
    def post(self, request):
        user_name = request.data.get('username')
        user_password = request.data.get('password')
        if not user_name or not user_password:
            return Response({'error': 'Provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
        current_user = authenticate(username=user_name, password=user_password)
        if current_user:
            user_token = RefreshToken.for_user(current_user)
            return Response({'message': 'Login Successful','refresh': str(user_token),'access': str(user_token.access_token),}, 
            status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Username'}, status=status.HTTP_401_UNAUTHORIZED)


class NoteListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get all notes for the authenticated user",
        responses={
            200: openapi.Response(
                description="List of notes",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "user": "john_doe",
                            "title": "My First Note",
                            "content": "This is the content",
                            "image": "http://example.com/media/api_images/image.jpg",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        }
                    ]
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={"application/json": {"detail": "Authentication credentials were not provided."}}
            ),
        },
        security=[{'Bearer': []}]
    )
    def get(self, request):
        user_notes = Note.objects.filter(user=request.user)
        notes_data = NoteSerializer(user_notes, many=True)
        return Response(notes_data.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={'title': openapi.Schema(type=openapi.TYPE_STRING, description='Note title'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Note content'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Optional image'),},
        ),
        responses={201: openapi.Response(description="Note created successfully",
                examples={"application/json": {"message": "Note created ",
                        "note": {
                            "id": 1,
                            "user": "john_doe",
                            "title": "My First Note",
                            "content": "This is the content",
                            "image": None,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"}}
                }
            ),
            400: openapi.Response(
                description="Bad request - validation errors",
                examples={
                    "application/json": {"title": ["This field is required."]}
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={
                    "application/json": {"detail": "Authentication credentials were not provided."}
                }
            ),
        },
        security=[{'Bearer': []}]
    )
    def post(self, request):
        note_data = NoteSerializer(data=request.data)
        if note_data.is_valid():
            note_data.save(user=request.user)
            return Response({'message': 'Note was created ','note': note_data.data},status=status.HTTP_201_CREATED)
        return Response(note_data.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_note(self, note_id, current_user):
        try:
            return Note.objects.get(id=note_id, user=current_user)
        except Note.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Get a specific note by ID",
        responses={200: openapi.Response(description="Note details",
                examples={"application/json": {
                        "id": 1,
                        "user": "john_doe",
                        "title": "My First Note",
                        "content": "This is the content",
                        "image": None,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"}}
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={"application/json": {"detail": "Authentication credentials were not provided."}
                }
            ),
            404: openapi.Response(
                description="Note not found",
                examples={"application/json": {"error": "Note was not found"}}),
        },
        security=[{'Bearer': []}]
    )
    def get(self, request, pk):
        current_note = self.get_note(pk, request.user)
        if not current_note:
            return Response({'error': 'Note was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        note_data = NoteSerializer(current_note)
        return Response(note_data.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a specific note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Note title'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Note content'),
                'image': openapi.Schema(type=openapi.TYPE_FILE, description='Optional image'),
            },
        ),
        responses={
            200: openapi.Response(
                description="Note updated successfully",
                examples={
                    "application/json": {
                        "message": "Note updated",
                        "note": {
                            "id": 1,
                            "user": "john_doe",
                            "title": "Updated Title",
                            "content": "Updated content",
                            "image": None,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T12:00:00Z"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request - validation errors",
                examples={
                    "application/json": {
                        "title": ["This field may not be blank."]
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            404: openapi.Response(
                description="Note not found",
                examples={"application/json": {"error": "Note was not found"}}
            ),
        },
        security=[{'Bearer': []}]
    )
    def put(self, request, pk):
        current_note = self.get_note(pk, request.user)
        if not current_note:
            return Response({'error': 'Note was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        updated_data = NoteSerializer(current_note, data=request.data, partial=True)
        if updated_data.is_valid():
            updated_data.save()
            return Response({'message': 'Note updated','note': updated_data.data},
            status=status.HTTP_200_OK)
        return Response(updated_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific note",
        responses={
            204: openapi.Response(
                description="Note deleted successfully",
                examples={"application/json": {"message": "Note deleted "}}
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={"application/json": {"detail": "Authentication credentials were not provided."}}
            ),
            404: openapi.Response(
                description="Note not found",
                examples={"application/json": { "error": "Note Not Found"}}
            ),
        },
        security=[{'Bearer': []}]
    )
    def delete(self, request, pk):
        current_note = self.get_note(pk, request.user)
        if not current_note:
            return Response({'error': 'Note Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        current_note.delete()
        return Response({'message': 'Note deleted '}, status=status.HTTP_204_NO_CONTENT)