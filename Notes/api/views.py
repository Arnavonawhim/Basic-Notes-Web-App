from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Note
from .serializers import UserSerializer, NoteSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = UserSerializer(data=request.data)
        if user_data.is_valid():
            new_user = user_data.save()
            user_token = RefreshToken.for_user(new_user)
            return Response({
                'message': 'Account created',
                'user': user_data.data,
                'refresh': str(user_token),
                'access': str(user_token.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_name = request.data.get('username')
        user_password = request.data.get('password')
        
        if not user_name or not user_password:
            return Response({'error': 'Provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_user = authenticate(username=user_name, password=user_password)
        
        if current_user:
            user_token = RefreshToken.for_user(current_user)
            return Response({
                'message': 'Login Successful',
                'refresh': str(user_token),
                'access': str(user_token.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Username'}, status=status.HTTP_401_UNAUTHORIZED)


class NoteListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_notes = Note.objects.filter(user=request.user)
        notes_data = NoteSerializer(user_notes, many=True)
        return Response(notes_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        note_data = NoteSerializer(data=request.data)
        if note_data.is_valid():
            note_data.save(user=request.user)
            return Response({
                'message': 'Note created ',
                'note': note_data.data
            }, status=status.HTTP_201_CREATED)
        return Response(note_data.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_note(self, note_id, current_user):
        try:
            return Note.objects.get(id=note_id, user=current_user)
        except Note.DoesNotExist:
            return None

    def get(self, request, pk):
        current_note = self.get_note(pk, request.user)
        if not current_note:
            return Response({'error': 'Note was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        note_data = NoteSerializer(current_note)
        return Response(note_data.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        current_note = self.get_note(pk, request.user)
        if not current_note:
            return Response({'error': 'Note was not found'}, status=status.HTTP_404_NOT_FOUND)
        
        updated_data = NoteSerializer(current_note, data=request.data, partial=True)
        if updated_data.is_valid():
            updated_data.save()
            return Response({
                'message': 'Note updated',
                'note': updated_data.data
            }, status=status.HTTP_200_OK)
        return Response(updated_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        current_note = self.get_note(pk, request.user)
        if not current_note:
            return Response({'error': 'Note Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        current_note.delete()
        return Response({'message': 'Note deleted '}, status=status.HTTP_204_NO_CONTENT)