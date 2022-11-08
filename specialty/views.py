from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Specialty
from .serializers import SpecialtySerializer

from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication


class ListSpecialtyView(ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class CreateSpecialtyView(CreateAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class DetailSpecialtyView(RetrieveUpdateDestroyAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]