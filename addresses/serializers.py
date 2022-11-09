from rest_framework import serializers
from addresses.models import Address


class AddressesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        fields=["id", "cep", "state", "street", "number"]
        read_only_fields=["id"]
