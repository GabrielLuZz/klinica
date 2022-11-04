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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance.patient.id == request.user.id:
            return Response({"detail": "You do not have permission to perform this action"}, status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)


        self.perform_update(serializer)
        return Response(serializer.data)
