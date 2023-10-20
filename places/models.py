from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField

from where_to_go_v2 import settings


class PlaceName(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок', unique=True)
    short_description = models.TextField('Короткое описание', blank=True)
    long_description = HTMLField('Полное описание', blank=True)
    longitude = models.FloatField(verbose_name='Долгота точки')
    latitude = models.FloatField(verbose_name='Широта точки')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'pk:{self.pk} {self.title}'


class PlaceImage(models.Model):
    sequence_number = models.IntegerField('Порядковый номер:', db_index=True, default=0, blank=True)
    place = models.ForeignKey(PlaceName, on_delete=models.CASCADE, verbose_name='Место', related_name='pictures')
    picture = models.ImageField( upload_to='img', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
        ordering = ['sequence_number']

    def __str__(self):
        return f'{self.sequence_number} {self.place}'

    @property
    def show_photo_preview(self):
        if self.picture:
            return format_html('<img src="{}" max-height="200" max-length="200" />', self.picture.url)
        return ""

    @property
    def get_absolute_image_url(self):
        return '{0}{1}'.format(settings.MEDIA_URL, self.picture.url)


class TourGuide(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    tour_name = models.CharField(max_length=128, verbose_name='Название экскурсии')
    description = models.TextField(verbose_name='Описание тура')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость экскурсии')

    places = models.ManyToManyField('PlaceName', verbose_name='Места', related_name='tour_guides')

    class Meta:
        verbose_name = 'Экскурсовод'
        verbose_name_plural = 'Экскурсоводы'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.tour_name}'
