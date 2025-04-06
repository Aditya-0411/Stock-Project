from .models import *
from rest_framework import serializers
from .models import Stocklog
from .models import StockReport
from django.contrib.auth.models import User, Group
from .models import Blogs

class StockTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTarget
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                
class StockSerializer(serializers.ModelSerializer):
    
    stock_targets = serializers.SerializerMethodField('get_all_stock_details')

    def get_all_stock_details(self, instance):
        serializer = StockTargetSerializer(StockTarget.objects.filter(stock=instance.id) , many=True, read_only=True)
        return serializer.data
    
    class Meta:
        model = Stock
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)            
                

class StockLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocklog
        fields = '__all__'




class StockReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockReport
        fields = ['id', 'user', 'stock', 'report_file', 'created_at']

class StockReportLogSerializer(serializers.ModelSerializer):
    report_link = serializers.SerializerMethodField()

    class Meta:
        model = StockReportLog
        fields = '__all__'

    def get_report_link(self, obj):
        return obj.get_report_link()


#CHANGED!!!!!
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')



class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model= Blogs
        fields = '__all__'
