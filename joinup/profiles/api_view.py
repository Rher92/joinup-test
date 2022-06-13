from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


from .serializers import ProfileCreateSerializer, ProfileSerializer, ProfileUpdateSerializer
from .models import Profile


class ProfileUserViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        """Return serializer based on action."""
        action_mappings = {
            'create': ProfileCreateSerializer,
            'update': ProfileUpdateSerializer
        }
        return action_mappings.get(self.action, ProfileSerializer)

    def get_serializer_context(self):
        """Add company to serializer context."""
        context = super().get_serializer_context()
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(
            ProfileSerializer(profile).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        profile = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(ProfileSerializer(profile).data)

    def perform_update(self, serializer):
        return serializer.save()
    
    @action(detail=False)
    def verify_email(self, request):
        username = request.GET.get('username')
        profile = get_object_or_404(Profile, user__username=username)
        profile.email_validated = True
        profile.save()
        return Response({'Response': 'email validated'}, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def verify_phone(self, request):
        username = request.GET.get('username')
        profile = get_object_or_404(Profile, user__username=username)
        profile.phone_validated = True
        profile.save()
        return Response({'Response': 'phone validated'}, status=status.HTTP_200_OK)
