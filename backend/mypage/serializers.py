from rest_framework import serializers
from .models import Review, Report, ExtraSetting

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'party', 'user', 'q1_rating', 'q2_rating', 'q3_rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']  # user는 요청한 유저로 자동 설정

    def validate(self, data):
        user = self.context['request'].user
        party = data.get('party')
        if Review.objects.filter(user=user, party=party).exists():
            raise serializers.ValidationError("이미 해당 파티에 리뷰를 작성하셨습니다.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)