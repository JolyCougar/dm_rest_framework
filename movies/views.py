from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer


class MovieListView(APIView):
    """ Output movies list """
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """ Output movie """
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
