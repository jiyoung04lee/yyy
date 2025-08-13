from rest_framework import serializers
from .models import Party

class PartyListSerializer(serializers.ModelSerializer):
    place_id = serializers.IntegerField(source="place.id", read_only=True)
    place_name = serializers.CharField(source="place.name", read_only=True) # 장소명
    place_photo = serializers.ImageField(source="place.photo", read_only=True) # 장소사진
    applied_count = serializers.IntegerField(read_only=True) # 신청인원
    max_participants = serializers.IntegerField(read_only=True) # 신청가능인원
    # 좌표 내려주기
    place_x_norm = serializers.FloatField(source="place.x_norm", read_only=True)
    place_y_norm = serializers.FloatField(source="place.y_norm", read_only=True)

    class Meta:
        model = Party
        fields = (
            "id",
            "title",
            "start_time",
            "place_name",
            "place_photo",
            "applied_count",
            "max_participants",
        )
        
class PartyDetailSerializer(serializers.ModelSerializer): # 추후에 지도이미지(혹은 API)와 유저 프로필도 추가 예정
    place_photo = serializers.ImageField(source="place.photo", read_only=True)
    place_name = serializers.CharField(source="place.name", read_only=True)

    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    applied_count = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = (
            "id",
            "title",
            "start_time",
            "description",
            "tags",
            "place_name",
            "place_photo",
            "applied_count",
            "max_participants",
        )

    def get_applied_count(self, obj):
        return obj.participations.count()
    
