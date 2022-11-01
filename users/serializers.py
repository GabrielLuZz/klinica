from rest_framework import serializers
from users.models import User


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["username", "cpf", "birth_date", "is_doctor", "is_recepcionist"]
        read_only_fields = ["id"]
        write_only_fields = ["password"]
        unique_fields = ["username", "cpf"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", "cpf", "birth_date", "is_doctor", "crm", "clinic" ]
        read_only_fields = ["id"]
        write_only_fields = ["password"]
        unique_fields = ["username", "cpf"]
