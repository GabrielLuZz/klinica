from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Specialty
from .serializers import SpecialtySerializer


class ListSpecialtyView(ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class CreateSpecialtyView(CreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class DetailSpecialtyView(RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer