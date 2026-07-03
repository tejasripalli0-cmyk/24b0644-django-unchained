from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Bounty


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class BountySerializer(serializers.ModelSerializer):
    """
    Serializer for the Bounty model.
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Bounty
        fields = (
            'id',
            'target_name',
            'reward',
            'status',
            'description',
            'location',
            'created_at',
            'owner',
        )
        read_only_fields = ('id', 'created_at', 'owner')

    def validate_reward(self, value):
        if value <= 0:
            raise serializers.ValidationError('Reward must be greater than zero.')
        return value

    def validate_target_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Target name cannot be empty.')
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Bounty.Status.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Status must be one of: {", ".join(valid_statuses)}.'
            )
        return value

