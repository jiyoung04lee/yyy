from rest_framework import serializers
from detailview.models import Participation

class StandbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['id', 'party', 'user', 'is_standby']
        read_only_fields = ['id', 'user']

    def update(self, instance, validated_data):
        """
        Standby 상태 업데이트 (토글 시 사용)
        """
        instance.is_standby = validated_data.get('is_standby', instance.is_standby)
        instance.save()
        return instance
