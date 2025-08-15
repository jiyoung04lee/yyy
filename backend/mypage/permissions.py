from rest_framework import permissions

class IsAuthenticatedAndAdminReadOnly(permissions.BasePermission):
    """
    로그인 유저만 생성 가능, 조회/수정/삭제는 관리자만 가능
    """
    def has_permission(self, request, view):
        # 작성(POST)은 로그인 유저만 가능
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        # 나머지(GET, PUT, PATCH, DELETE)는 관리자만 가능
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    객체의 user 필드가 요청 유저와 같을 때만 허용
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
