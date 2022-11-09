from django.shortcuts import render
from rest_framework.generics import UpdateAPIView
from addresses.serializers import Address, AddressesSerializer
from rest_framework.authentication import TokenAuthentication
from utils.authenticationMixins import IsReceptionistOrAdm
from rest_framework.views import Response, status


# Create your views here.
class UpdateAddressView(UpdateAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressesSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsReceptionistOrAdm]
