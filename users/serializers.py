from rest_framework import serializers
from users.models import User
from addresses.serializers import AddressesSerializer


class PatientSerializer(serializers.ModelSerializer):

    address=AddressesSerializer()

    class Meta:
        model=User
        fields=["id", "username", "last_login", "password", "cpf", "birth_date", "is_doctor", "is_recepcionist", "address"]
        read_only_fields = ["id", "is_doctor", "is_recepcionist", "is_superuser"]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        unique_fields = ["username", "cpf"]


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", "cpf", "birth_date", "is_doctor", "crm", "clinic" ]
        read_only_fields = ["id"]
        write_only_fields = ["password"]
        unique_fields = ["username", "cpf"]
