from rest_framework import serializers
from .models import Review, Report, ExtraSetting

from detailview.models import Participation  # 파티 참여 테이블

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'party', 'user', 'q1_rating', 'q2_rating', 'q3_rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def validate(self, data):
        user = self.context['request'].user
        party = data.get('party')

        # 1. 파티 참여 여부 확인
        if not Participation.objects.filter(user=user, party=party).exists():
            raise serializers.ValidationError("참여한 파티에만 리뷰를 작성할 수 있습니다.")

        # 2. 중복 작성 방지
        if Review.objects.filter(user=user, party=party).exists():
            raise serializers.ValidationError("이미 이 파티에 리뷰를 작성하셨습니다.")

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

        # 1. 파티 참여 여부 확인
        if not Participation.objects.filter(user=reporter, party=party).exists():
            raise serializers.ValidationError("참여한 파티에서만 신고가 가능합니다.")

        # 2. 자기 자신 신고 방지
        if reporter == reported_user:
            raise serializers.ValidationError("자기 자신은 신고할 수 없습니다.")

        # 3. 중복 신고 방지
        if Report.objects.filter(party=party, reporter=reporter, reported_user=reported_user).exists():
            raise serializers.ValidationError("이미 해당 유저를 신고하셨습니다.")

        return data

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)
    

class ExtraSettingFromJsonSerializer(serializers.Serializer):
    extra = serializers.DictField()

    def create(self, validated_data): #json의 키값들 확인 후 변경될 텍스트들 (현재는 임시로)
        extra_data = validated_data.get('extra', {})
        return ExtraSetting.objects.create(
            user=self.context['request'].user,
            grade=extra_data.get('grade', ''),  
            college=extra_data.get('college', ''),
            personality=extra_data.get('personality', ''),
            mbti_i_e=extra_data.get('mbti', {}).get('i_e', ''),
            mbti_n_s=extra_data.get('mbti', {}).get('n_s', ''),
            mbti_f_t=extra_data.get('mbti', {}).get('f_t', ''),
            mbti_p_j=extra_data.get('mbti', {}).get('p_j', ''),
        )

    def update(self, instance, validated_data):
        extra_data = validated_data.get('extra', {})
        instance.grade = extra_data.get('grade', instance.grade)
        instance.college = extra_data.get('college', instance.college)
        instance.personality = extra_data.get('personality', instance.personality)
        instance.mbti_i_e = extra_data.get('mbti', {}).get('i_e', instance.mbti_i_e)
        instance.mbti_n_s = extra_data.get('mbti', {}).get('n_s', instance.mbti_n_s)
        instance.mbti_f_t = extra_data.get('mbti', {}).get('f_t', instance.mbti_f_t)
        instance.mbti_p_j = extra_data.get('mbti', {}).get('p_j', instance.mbti_p_j)
        instance.save()
        return instance