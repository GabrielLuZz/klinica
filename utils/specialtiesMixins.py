from specialty.models import Specialty


class SpecialtySave:
    def perform_create(self, serializer):
        specialty_data = self.validated_data.pop("specialty")

        for specialty in specialty_data:
            specialty, _ = Specialty.objects.get_or_create(**specialty)
            self.validated_data.specialty.add(specialty)

        serializer.save()





# # def create (self, validated_data):
#         specialty_data = validated_data.pop("specialty")
#         doctor = User.objects.create_user(**validated_data)

#         for specialty in specialty_data:
#             specialty, _ = Specialty.objects.get_or_create(**specialty)
#             doctor.specialty.add(specialty)
#         return doctor