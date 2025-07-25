from rest_framework import serializers
from .models import User, Conversation, Message

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested sender info

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sent_at', 'sender']


# --- Conversation Serializer ---
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participant_ids', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        participants = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation