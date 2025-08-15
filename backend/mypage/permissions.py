from rest_framework import permissions
from detailview.models import Participation

class IsAuthenticatedAndParticipant(permissions.BasePermission):
    """
    로그인한 유저이면서, 해당 파티에 실제로 참여한 경우에만 허용
    GET, PUT, PATCH, DELETE는 기본적으로 막고,
    POST만 참여 여부 확인 후 허용
    """
    def has_permission(self, request, view):
        # POST만 허용 (생성)
        if request.method == 'POST':
            if not (request.user and request.user.is_authenticated):
                return False

            party_id = request.data.get('party')
            if not party_id:
                return False

            return Participation.objects.filter(
                user=request.user,
                party_id=party_id
            ).exists()

        # 나머지 메서드는 관리자만 가능
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    객체의 user 필드가 요청 유저와 같을 때만 허용
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
