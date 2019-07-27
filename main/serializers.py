from rest_framework.serializers import ModelSerializer
from .models import *





# start get api

class GymsSerializer(ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'



class HoursSerializers(ModelSerializer):
    class Meta:
        model = Hour
        fields = '__all__'



class TicketsSerializers(ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'




class CitiesSerializers(ModelSerializer):
    class ProvincesSerializers(ModelSerializer):
        class Meta:
            model = Province
            fields = '__all__'
    province_id = ProvincesSerializers(read_only=True)
    class Meta:
        model = City
        fields = ('name','province_id')



class ProvincesSerializers(ModelSerializer):
    class CitesSerializers(ModelSerializer):
        class Meta:
            model = City
            fields = '__all__'
    cities = CitesSerializers(many=True,read_only=True)
    class Meta:
        model = Province
        fields = ('name','cities')







class AreasSerializers(ModelSerializer):
    class CitesSerializers(ModelSerializer):
        class ProvincesSerializers(ModelSerializer):
            class Meta:
                model = Province
                fields = '__all__'
        province_id = ProvincesSerializers()
        class Meta:
            model = City
            fields = '__all__'
    city_id = CitesSerializers(read_only=True)

    class Meta:
        model = Area
        fields = '__all__'



#end get api