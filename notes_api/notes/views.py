#from django.http import JsonResponse
from .models import Note, Tag
from .serializers import NoteSerializer, TagSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

#from django.shortcuts import render
#from django.contrib.auth.decorators import login_required


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def note_list(request, format=None):
    if request.method == 'GET':
        search_query = request.GET.get('search', None)
        notes = Note.objects.filter(owner=request.user).order_by('-updated_at')

        if search_query:
            notes = notes.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )

        serializer = NoteSerializer(notes, context={'request': request}, many=True)
        return Response(serializer.data)



    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail(request, pk, format=None):
    
    note = Note.objects.filter(pk=pk, owner=request.user).first()
    if note is None:
       return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = NoteSerializer(note, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if note.owner != request.user:
            return Response({"detail": "You do not have permission to edit this note."}, status=status.HTTP_403_FORBIDDEN)

        serializer = NoteSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if note.owner != request.user:
            return Response({"detail": "You do not have permission to delete this note."}, status=status.HTTP_403_FORBIDDEN)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tag_list(request):
    tags = Tag.objects.filter(owner=request.user)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

