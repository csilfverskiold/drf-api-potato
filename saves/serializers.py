from django.db import IntegrityError
from rest_framework import serializers
from saves.models import Save


class SaveSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Save
        fields = ['id', 'created_at', 'owner', 'recipe']

    def create(self, validated_data):  # Handles creating duplicate saves
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
