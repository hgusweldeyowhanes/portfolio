from main import models
from rest_framework import serializers
from django.utils import timezone
class ProjectSerializer(serializers.ModelSerializer):
    technologies_list = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    is_ml_project = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Project
        fields = "_all_"

    def get_technologies_list(self,obj):
        return obj.technologies_list()
    def get_duration(self,obj):
        return f"{(timezone.now()-obj.created).days // 30} months ago"
class SkillsSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    level_class = serializers.SerializerMethodField()
    libraries_list = serializers.SerializerMethodField()
    class Meta:
        model = models.Skills
        fields = "_all_"
    def get_level_class(self,obj):
        return obj.get_level_display_class()
    def get_libraries_list(self,obj):
        return obj.libraries_list()
    
class ExperienceSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    is_ai_ml_role = serializers.BooleanField(read_only=True)
    algorithms_list = serializers.SerializerMethodField()
    protocols_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Experience
        fields = '__all__'
    
    def get_duration(self, obj):
        return obj.duration()
    
    def get_algorithms_list(self, obj):
        return [alg.strip() for alg in obj.algorithms_used.split(',')] if obj.algorithms_used else []
    
    def get_protocols_list(self, obj):
        return [proto.strip() for proto in obj.protocols_used.split(',')] if obj.protocols_used else []