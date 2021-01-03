from django.db import models
from .validators import MinMaxValueValidator
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#Модели
class Estimation(models.Model):
    value = models.FloatField(verbose_name='Значение оценки',validators=[MinMaxValueValidator(1,10)])
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Оценивший')
    post = models.ForeignKey('Post',on_delete=models.CASCADE, verbose_name='Публикация')

    class Meta:
        verbose_name_plural = 'Оценки'
        verbose_name = 'Оценка'


class Post(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название',unique=True)
    photo = models.ImageField(verbose_name='Картинка', upload_to='Pboard\\media\\posts')
    user_score = models.FloatField(null=True, blank=True,verbose_name='Оценка пользователя',validators=[MinMaxValueValidator(1,10)])
    info = models.TextField(null=True, blank=True,max_length=500, verbose_name='Сведения')
    published = models.DateTimeField(auto_now_add=True, db_index = True,verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null = True, on_delete= models.PROTECT, verbose_name= 'Рубрика') 
    author = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE,verbose_name='Автор',)
    show_authorship = models.BooleanField(verbose_name='Показывать автора', default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.photo.delete(save=False)
        super().delete(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Публикации'
        verbose_name = 'Публикация'
        ordering = ['-published']#последовательность полей, по которым по умолчанию будет выполняться сортировка записей.

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True,unique=True, verbose_name='Название')
    image = models.ImageField(null=True,verbose_name='Логотип рубрики', upload_to='Pboard\\media\\rubric')
    
    def __str__(self):
        return self.name
    
    
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def get_post_count(self):
        return self.post_set.count()

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name',]

def author_estimate(sender, **kwargs):
    post = kwargs['instance']
    if post.user_score is not None:
        try:
            est = Estimation.objects.get(post_id=post.pk,user_id=post.author.pk)
            est.value = post.user_score
            est.save()
        except ObjectDoesNotExist:
            est = Estimation.objects.create(value=post.user_score,user=post.author,post=post)
            est.save()


post_save.connect(author_estimate,sender=Post)