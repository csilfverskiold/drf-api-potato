from rest_framework import serializers
from .models import Recipe
from likes.models import Like
from saves.models import Save


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    save_id = serializers.SerializerMethodField()

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                'Image size too large! Please choose an image less than 2MB!'
                )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Please choose an image height less than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Please choose an image width less than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):  # Checks and displays user like or not
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, recipe=obj
            ).first()
            return like.id if like else None
        return None

    def get_save_id(self, obj):  # Checks and displays user save or not
        user = self.context['request'].user
        if user.is_authenticated:
            save = Save.objects.filter(
                owner=user, recipe=obj
            ).first()
            return save.id if save else None
        return None

    class Meta:
        model = Recipe
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'category', 'ingredient', 'instruction',
            'image', 'like_id', 'save_id',
        ]
