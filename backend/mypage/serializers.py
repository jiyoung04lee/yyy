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
    
    
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'party', 'reporter', 'reported_user', 'category', 'content', 'status', 'created_at']
        read_only_fields = ['id', 'reporter', 'status', 'created_at']

    def validate(self, data):
        reporter = self.context['request'].user
        reported_user = data.get('reported_user')
        party = data.get('party')

        if reporter == reported_user:
            raise serializers.ValidationError("자기 자신은 신고할 수 없습니다.")

        if Report.objects.filter(party=party, reporter=reporter, reported_user=reported_user).exists():
            raise serializers.ValidationError("이미 해당 유저를 신고하셨습니다.")

        return data

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)

class ExtraSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraSetting
        fields = [
            'id', 'user', 'grade', 'college', 'personality',
            'mbti_i_e', 'mbti_n_s', 'mbti_f_t', 'mbti_p_j'
        ]
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # user는 변경 불가
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
