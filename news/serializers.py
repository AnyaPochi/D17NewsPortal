from .models import *
from rest_framework import serializers

class NewsSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['title', 'type', ]










