from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# for slug
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(null=True,blank=True,verbose_name='Аватар', upload_to='Accounts\\media\\avatars')
    slug = models.SlugField(verbose_name='URL', unique=True,null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.avatar.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


def profile_slug_generator(sender, instance, *args, **kwargs):
    slug = slugify(instance.user.username)
    exists = Profile.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s" %(slug)
    instance.slug = slug

# def profile_autocreater(sender, instance, *args, **kwargs):
#     profile = Profile(user = instance)
#     profile.save()

pre_save.connect(profile_slug_generator, sender=Profile)
# pre_save.connect(profile_autocreater, sender=User,)