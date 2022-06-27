from django.http import Http404
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import (IsAuthenticated,
                                        IsAdminUser)

from core.stats import get_stats
from core.utils import get_client_ip
from core.models import (Link, Viewer, Visitor)
from core.serializers import (ReadUserSerializer, WriteLinkSerializer, 
                                ReadLinkSerializer, 
                                WriteUserSerializer)



class APIRoot(APIView):

    def get(self, request):
        return Response({
            'users': reverse('user-list', request=request),
            'links': reverse('link-list', request=request)
        })


class LinkViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadLinkSerializer
        else:
            return WriteLinkSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.prefetch_related('links')
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadUserSerializer
        else:
            return WriteUserSerializer


class RedirectAPI(APIView):

    def get_object(self, slug):
        try:
            return Link.objects.get(slug=slug, active=True)
        except Link.DoesNotExist:
            raise Http404

    def get_visitor(self, request):
        ip = get_client_ip(request)
        try:
            return Visitor.objects.get(ip=ip)
        except Visitor.DoesNotExist:
            return Visitor.objects.create(ip=ip)
        
    def submit_view(self, link, visitor):
        return Viewer.objects.create(visitor=visitor, link=link)

    def get(self, request, slug):
        link = self.get_object(slug)
        visitor = self.get_visitor(request)
        self.submit_view(link, visitor)
        return redirect(link.origin)


class StatsAPI(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        stats = get_stats(self.request.user, slug)
        return Response(data=stats)


class SignupAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = WriteUserSerializer