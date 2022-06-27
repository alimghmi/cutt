from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from core import utils
from core.models import Link


class ReadLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Link
        fields =  ['id', 'origin', 'slug', 'active', 'updated_at', 'created_at']
        read_only_field = fields


class WriteLinkSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Link
        fields = ['id', 'user', 'origin', 'slug', 'active']

    def create(self, validated_data):
        if not validated_data.get('slug', None):
            validated_data['slug'] = utils.generate_shorten_link(model=self.Meta.model)

        return super().create(validated_data)


class ReadUserSerializer(serializers.ModelSerializer):

    links = ReadLinkSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'links']
        read_only_fields = fields


class WriteUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data.pop('password', None)
            
        return super().update(instance, validated_data)
