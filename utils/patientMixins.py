from addresses.models import Address
from users.serializers import User
from rest_framework.views import Response, status


class AddressSave:
    def perform_create(self, serializer):

        address = Address.objects.create(**self.request.data["address"])
        serializer.save(address=address)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cpf_already_exists = User.objects.filter(cpf=request.data["cpf"])

        if cpf_already_exists:
            return Response({"detail": "key cpf already exists"}, status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
