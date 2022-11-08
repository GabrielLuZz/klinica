from rest_framework import serializers
from .models import Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "name"]
        read_only_fields = ["id"]