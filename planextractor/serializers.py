from rest_framework import serializers
from .models import FloorPlan

class FloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlan
        fields = '__all__'
