from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Photo
from .serializer import PostSerializer,UserSerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Photo.objects.all()

    def get_permissions(self):
        """GET requestlar uchun hamma kirishi mumkin, boshqa amallar faqat login qilganlarga"""
        if self.action in ['list', 'retrieve']:  
            return [AllowAny()]  # Hamma kirib rasmlarni ko‘ra oladi
        return [IsAuthenticated()]  # Faqat login qilganlar yuklay oladi

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


from django.shortcuts import get_object_or_404
from django.http import FileResponse

def download_image(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return FileResponse(photo.image.open(), as_attachment=True)

    
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Faqat o‘z profilini o‘zgartirish imkoniyati
