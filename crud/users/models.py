from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile!'

    def save(self, *args, **kwargs):
        # Generate slug if not already set
        if not self.slug:
            base_slug = slugify(self.user.username)
            self.slug = base_slug

            # Ensure uniqueness
            counter = 1
            while Profile.objects.filter(slug=self.slug).exists():
                self.slug = f'{base_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs) # Call the original save method

        # Optional: Handle image resizing if needed
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            resize = (300, 300)
            img.thumbnail(resize)
            img.save(self.image.path)
            return 'has been updated correctly (300x300)!'

    def get_absolute_url(self):
        return reverse('users', kwargs={'pk': self.pk}) # update redirect to
