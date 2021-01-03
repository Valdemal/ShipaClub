from django.db import models

#Новости
class News(models.Model):
    title = models.CharField(max_length=75,verbose_name='Заголовок',unique=True)
    content = models.TextField(max_length=2000, verbose_name='Содержание')
    published = models.DateTimeField(auto_now_add=True, db_index = True,verbose_name='Опубликовано')
    image = models.ImageField(null=True,blank=True,verbose_name='Изображение', upload_to='Mainpage\\media')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
        ordering = ['-published']