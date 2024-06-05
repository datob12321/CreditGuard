from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        ccv = serializers.IntegerField()
        model = Card
        fields = '__all__'
        # exclude = ['user']

    def validate(self, data):

        ccv = serializers.IntegerField()

        if data['ccv'] > 18:
            raise serializers.ValidationError('it should be less than 18')


class MySerializer(serializers.Serializer):
    ccv = serializers.IntegerField()
    card_number = serializers.IntegerField()

    def validate(self, data):
        if data['ccv'] < 100 or data['ccv'] > 900:
            raise serializers.ValidationError('it must be between 100 and 900!')

        if len(str(data['card_number'])) != 16:
            raise serializers.ValidationError('it must has 16 characters!')
        return data

