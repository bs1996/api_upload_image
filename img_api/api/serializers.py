from .models import Tiers, Customer, Images
from rest_framework import serializers


class TiersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tiers
        fields = ['id', 'name', 'thumbnail_size', 'original_file', 'expiring_links']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'account_type']


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Images
        fields = ['link1', 'link2', 'link3', 'link4']

