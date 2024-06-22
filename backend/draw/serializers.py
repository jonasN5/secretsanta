from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer as DRFAuthRegisterSerializer
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from draw.models import Participant, Draw, DrawPair


class RegisterSerializer(DRFAuthRegisterSerializer):

    def validate_username(self, username):
        """Override the username validation to allow for none unique usernames."""
        username = get_adapter().clean_username(username, shallow=True)
        return username

    def save(self, request):
        """Override the save method to catch IntegrityError if the email already exists."""
        try:
            user = super().save(request)
            return user
        except IntegrityError as e:
            raise serializers.ValidationError(detail='A User with this email already exists.')


class ParticipantSerializer(ModelSerializer):
    blacklisted = serializers.PrimaryKeyRelatedField(many=True, queryset=Participant.objects.all(), required=False)
    email = serializers.EmailField(required=True)
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Participant
        fields = ['id', 'email', 'username', 'blacklisted', 'owner']


class DrawPairSerializer(ModelSerializer):
    class Meta:
        model = DrawPair
        fields = ['santa', 'santee']


class DrawSerializer(serializers.Serializer):
    # A list of participants that should be excluded from the draw.
    exclude = serializers.PrimaryKeyRelatedField(many=True, queryset=Participant.objects.all(), required=False,
                                                 write_only=True)
    id = serializers.IntegerField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    pairs = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Draw
        fields = ['id', 'owner', 'created_at']
        read_only_fields = ['owner', 'pairs']

    def get_pairs(self, obj: Draw) -> list[dict]:
        return DrawPairSerializer(many=True).to_representation(obj.pairs.all())
