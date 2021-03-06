from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from osp.models import UserInformation
from osp.serializers.user_information import UserInformationSerializer

class UserInformationView(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    serializer_class = UserInformationSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = UserInformation.objects.filter(user_id=user.id)
        return queryset

    def create(self, request):
        user = self.request.user
        serializer = UserInformationSerializer(data=request.data)

        if UserInformation.objects.filter(user_id=user.id).exists():
            return Response("Information already filled", status=status.HTTP_409_CONFLICT)
        
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
