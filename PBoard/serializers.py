from rest_framework import serializers
from .models import Rubric

class RubricSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source='get_post_count', read_only=True)
    
    class Meta:
        model = Rubric
        fields = ('id', 'name','post_count')