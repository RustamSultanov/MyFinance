from datetime import datetime, timedelta

from django.db.models import Sum
from django.db.models.functions import Extract
from pytz import UTC
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAccountOwnerOrReadOnly, IsChargeOwner, IsHimself
from .serializers import (
    AccountDetailSerializer, AccountListSerializer, ChargeListSerializer, ChargeDetailSerializer,
    UserListSerializer, UserDetailSerializer, StatisticSerializer, FullUserDetailSerializer
)
from ..models import Account, Charge, UserProfile


class AccountList(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return Account.objects.filter(user=self.request.user)
        elif self.request.query_params.get('search', None) is not None:
            user = self.request.query_params.get('search', None)
            return Account.objects.filter(user__username=user)


class AccountDetail(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer
    lookup_field = 'number'
    permission_classes = [IsAccountOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()


class ChargeList(ListCreateAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['account__number']

    def get_queryset(self):
        if self.request.user.is_staff:
            if len(self.request.query_params) == 0:
                return Charge.objects.filter(account__user=self.request.user)
            elif self.request.query_params.get('search', None) is not None:
                account = self.request.query_params.get('search', None)
                return Charge.objects.filter(account__number=account)
        else:
            return Charge.objects.filter(account__user=self.request.user)


class ChargeDetail(RetrieveUpdateDestroyAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsChargeOwner]


class StatisticsList(APIView):
    serializer_class = StatisticSerializer
    lookup_field = 'number'

    @staticmethod
    def get(request, number=None):
        content = {}
        if len(request.query_params) == 0:

            content = (Charge.objects
                       .filter(account__number=number)
                       .annotate(month=Extract('transactedAt', 'month'))
                       .values('month').annotate(total=Sum('value'))
                       .annotate(year=Extract('transactedAt', 'year'))
                       .values('year', 'month', 'total')
                       .order_by('year', 'month')
                       .values_list('year', 'month', 'total'))

        elif (request.query_params.get('date_from', None) and request.query_params.get('date_to', None)) is not None:

            date_from = (datetime.strptime(request.query_params.get('date_from'), '%Y-%m-%d')
                         .replace(tzinfo=UTC))
            date_to = ((datetime.strptime(request.query_params.get('date_to'), '%Y-%m-%d') + timedelta(days=1))
                       .replace(tzinfo=UTC))

            content = (Charge.objects
                       .filter(account__number=number, transactedAt__range=[date_from, date_to])
                       .annotate(month=Extract('transactedAt', 'month'))
                       .values('month').annotate(total=Sum('value'))
                       .annotate(year=Extract('transactedAt', 'year'))
                       .values('year', 'month', 'total')
                       .order_by('year', 'month')
                       .values_list('year', 'month', 'total'))

        return Response(content, status=200)


class UserList(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username']

    def get_queryset(self):
        if len(self.request.query_params) == 0:
            return UserProfile.objects.filter(username=self.request.user)
        elif self.request.query_params.get('search', None) is not None:
            user = self.request.query_params.get('search')
            return UserProfile.objects.filter(username=user)


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'
    permission_classes = [IsHimself]

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            self.serializer_class = FullUserDetailSerializer
        serializer.save(user=self.request.user)
