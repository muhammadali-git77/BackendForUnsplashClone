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


def download_image(request, photo_id):
    """Fayl yuklab olish uchun endpoint"""
    photo = get_object_or_404(Photo, id=photo_id)
    
    if not photo.image:
        return HttpResponse("Fayl topilmadi", status=404)

    file_path = photo.image.path  # Faylning real yo'li
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")  
        response['Content-Disposition'] = f'attachment; filename="{photo.image.name}"'
        return response
 
    
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Faqat o‘z profilini o‘zgartirish imkoniyati
