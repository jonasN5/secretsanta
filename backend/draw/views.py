from typing import override

from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from draw.draw_generator import generate_draw
from draw.models import Participant, Draw
from common.permissions import OwnerOnly
from draw.serializers import ParticipantSerializer, DrawSerializer


class ParticipantsViewSet(viewsets.ModelViewSet):
    """
    CRUD actions on Participant objects.
    """
    permission_classes = [IsAuthenticated, OwnerOnly]
    queryset = Participant.objects.only(*ParticipantSerializer.Meta.fields)
    serializer_class = ParticipantSerializer
    pagination_class = None  # Disable pagination for convenience;
    http_method_names = ['get', 'post', 'patch', 'delete']  # Disable PUT method

    @override
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DrawsView(ListAPIView):
    """
    List all draws for the current user (GET) and create a new draw (POST).
    """
    queryset = Draw.objects.only(*DrawSerializer.Meta.fields)
    serializer_class = DrawSerializer

    @override
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        # Generate a new draw
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        excluded_participants = serializer.validated_data.get('exclude', [])
        participants = Participant.objects.filter(owner=self.request.user).exclude(
            id__in=[p.id for p in excluded_participants])
        draw: Draw = generate_draw(participants, owner=self.request.user)

        return Response(DrawSerializer(instance=draw).data, status=status.HTTP_201_CREATED)
