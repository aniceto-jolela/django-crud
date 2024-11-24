from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', null=True, blank=True)  # This will use Cloudinary for storage
    slug = models.SlugField(verbose_name='slug', max_length=255, blank=True, unique=True)

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

    def get_absolute_url(self):
        return reverse('users', kwargs={'pk': self.pk}) # update redirect to
