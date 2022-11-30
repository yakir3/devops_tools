from rest_framework import serializers
from .models import ApolloApp, ApolloInstance

"""models 类序列化器"""
class ApolloAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApolloApp
        fields = '__all__'
        # allow_blank = ['']
        read_only_fields = ['id', 'create_date']
    # def create(self, validated_data):
    #     return ApolloApp.objects.create(**validated_data)
    # def update(self, instance, validated_data):
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.save()
    #     return instance

class ApolloInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApolloInstance
        fields = '__all__'
        read_only_fields = ['id', 'create_date']

class ApolloAuthorizedSerializer(serializers.Serializer):
    app_id = serializers.CharField(max_length=30)
    user = serializers.CharField(max_length=20)
    permission = serializers.CharField(max_length=30)
    env = serializers.CharField(max_length=20)
    namespace = serializers.CharField(max_length=20)
