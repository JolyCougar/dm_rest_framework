from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .service import get_client_ip, MovieFilter
from .models import Movie, Actor, Review
from .serializers import (MovieListSerializer, MovieDetailSerializer,
                          ReviewCreateSerializer, CreateRatingSerializer,
                          ActorListSerializer, ActorDetailSerializer)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """ Output movies list """
    filter_backends = (DjangoFilterBackend,)
    filter_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """ Add Review to movie """
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """ Add Review to movie """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """ List actors and directors """
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer

# class MovieListView(generics.ListAPIView):
#     """ Output movies list """
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F("ratings__star")) / models.Count(models.F("ratings"))
#         )
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """ Output movie """
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """ Add Review to movie """
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """ Add rating to movie """
#
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorListView(generics.ListAPIView):
#     """ List actors and directors """
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorDetailView(generics.RetrieveAPIView):
#     """ List actors and directors """
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
