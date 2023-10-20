from django.contrib import admin
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib.admin.widgets import FilteredSelectMultiple
from places.models import PlaceName, PlaceImage, TourGuide
from django.db import models


class PicsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    readonly_fields = ["show_photo_preview"]

    def show_photo_preview(self, obj):
        return obj.show_photo_preview

    show_photo_preview.short_description = 'Photo Preview'
    show_photo_preview.allow_tags = True


@admin.register(PlaceName)
class PostAdmin(SortableAdminBase, admin.ModelAdmin):
    fields = ["title", "short_description", "long_description", "latitude", "longitude"]
    list_display = ['title']
    inlines = [PicsInline, ]


@admin.register(PlaceImage)
class PicAdmin(admin.ModelAdmin):
    ordering = ['sequence_number']
    readonly_fields = ["show_photo_preview"]

    def show_photo_preview(self, obj):
        return obj.show_photo_preview

    show_photo_preview.short_description = 'Photo Preview'
    show_photo_preview.allow_tags = True


class TourGuideAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'tour_name', 'cost', 'description')

    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('Места', is_stacked=False)}
    }


admin.site.register(TourGuide, TourGuideAdmin)
