from django.db import models
from where_to_go_v2 import settings

from tinymce.models import HTMLField
from django.utils.safestring import mark_safe


class PlaceName(models.Model):
    title = models.CharField('Заголовок', max_length=128)
    short_description = models.TextField('Короткое описание', blank=True)
    long_description = HTMLField('Полное описание', blank=True)
    longitude = models.FloatField(verbose_name='Долгота точки')
    latitude = models.FloatField(verbose_name='Широта точки')

    def __str__(self):
        return f'pk:{self.pk} {self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PlaceImage(models.Model):
    sequence_number = models.IntegerField("Порядковый номер:", db_index=True, default=0, blank=True)
    place = models.ForeignKey(PlaceName, on_delete=models.CASCADE, verbose_name="Место", related_name='pictures')
    picture = models.ImageField("Картинка", upload_to='img')

    def __str__(self):
        return f'{self.sequence_number} {self.place}'

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
        ordering = ['sequence_number']

    @property
    def photo_preview(self):
        if self.picture:
            return mark_safe('<img src="{}" height="200" />'.format(self.picture.url))
        return ""

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.picture.url)
