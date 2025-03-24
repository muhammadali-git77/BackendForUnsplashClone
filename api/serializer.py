from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Photo, Profile
from django.conf import settings

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]


# User serializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)  # Nested serializer (optional)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)  # `profile` maydonini ajratib olish

        # Asosiy user ma'lumotlarini yangilash
        instance = super().update(instance, validated_data)

        # Profile ma'lumotlarini yangilash
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            profile.avatar = profile_data.get("avatar", profile.avatar)
            profile.save()

        return instance
    
    # Product serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = "__all__"  

    def get_download_url(self, obj):
        """Rasmni yuklab olish uchun to‘liq URL qaytaradi"""
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(f"/download/{obj.id}/")  # Yangi yuklab olish URL
        return None
    
    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user  # Kirgan userni avtomatik qo'shish
        return super().create(validated_data)

