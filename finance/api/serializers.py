from rest_framework.fields import DecimalField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from finances.models import Account, Charge, UserProfile


class AccountListSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'number'
        ]


class AccountDetailSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'user',
            'number'
        ]


class ChargeListSerializer(ModelSerializer):
    class Meta:
        model = Charge
        fields = [
            'account',
            'value',
            'date'
        ]


class ChargeDetailSerializer(ModelSerializer):
    class Meta:
        model = Charge
        fields = [
            'account',
            'value',
            'date'
        ]


class UserListSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'address',
            'phone',
        ]


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'address',
        ]


class StatisticSerializer(Serializer):
    year = IntegerField()
    month = IntegerField()
    total = DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        super().create(self)

    def update(self, instance, validated_data):
        super().update(self, instance)
