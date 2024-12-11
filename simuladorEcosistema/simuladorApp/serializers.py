from rest_framework import serializers
from simuladorApp.models import ParametrosSimulacion

class ParametroSimulacionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ParametrosSimulacion
        fields = '__all__'
        