from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    """ Category """
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """ Actors and director"""
    name = models.CharField("Name", max_length=100)
    age = models.PositiveIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Actor and director"
        verbose_name_plural = "Actors and directors"


class Genre(models.Model):
    """ Genres """
    name = models.CharField("name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    """ Movie """
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default="")
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveIntegerField("Year", default=2019)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="director", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="actor", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    world_premiere = models.DateField("World Premiere", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="Write count in dollars")
    fees_in_usa = models.PositiveIntegerField("Fees in USA", default=0,
                                              help_text="Write count in dollars")
    fees_in_world = models.PositiveIntegerField("Fees in World", default=0,
                                                help_text="Write count in dollars")
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShot(models.Model):
    """ Images from Movie """
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="movies_shot/")
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Image from Movie"
        verbose_name_plural = "Images from Movie"


class RatingStar(models.Model):
    """ Rating star """
    value = models.PositiveSmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    """ Rating """
    ip = models.CharField("IP", max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name="Star", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Review(models.Model):
    """ Reviews"""
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Text", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Parent", on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


