from rest_framework import serializers

from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
    """ List movies serializer """

    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """ Add review """

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """ View review """

    class Meta:
        model = Review
        fields = ("name", "text", "parent")


class MovieDetailSerializer(serializers.ModelSerializer):
    """ Detail movie serializer """
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)
