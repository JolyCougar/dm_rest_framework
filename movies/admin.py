from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShot, Actor, Rating, RatingStar, Review
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """ Forms with widget ckeditor """
    description = forms.CharField(label="Description", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Category """
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """ Reviews on movies page"""
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class MovieShortsInLine(admin.TabularInline):
    model = MovieShot
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="120" height="120"')

    get_image.short_description = "Image"


@admin.register(Movie)
class MoviesAdmin(admin.ModelAdmin):
    """ Movies """
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year",)
    search_fields = ("title", "category__name",)
    inlines = [MovieShortsInLine, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["published", "unpublished"]
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def unpublished(self, request, queryset):
        """ Unpublished movie """
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 record has update"
        else:
            message_bit = f"{row_update} records has update"
        self.message_user(request, f"{message_bit}")

    def published(self, request, queryset):
        """ Published movie """
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 record has update"
        else:
            message_bit = f"{row_update} records has update"
        self.message_user(request, f"{message_bit}")

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="120" height="120"')

    published.short_description = "Publish"
    published.allowed_permissions = ('change',)

    unpublished.short_description = "Unpublish"
    unpublished.allowed_permissions = ('change',)

    get_image.short_description = "Poster preview"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Reviews """
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """ Genres """
    list_display = ("name", "url",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """ Actors """
    list_display = ("name", "age", "get_image",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Rating """
    list_display = ("star", "movie", "ip",)


@admin.register(MovieShot)
class MovieShot(admin.ModelAdmin):
    """ Images from Movie """
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "image"


admin.site.register(RatingStar)
admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
