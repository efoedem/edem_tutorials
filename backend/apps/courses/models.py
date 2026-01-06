from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Cloudinary will use this field to store your images permanently
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)

    # Adding price so it shows up on your cards (e.g., 200ghc)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_taught'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title