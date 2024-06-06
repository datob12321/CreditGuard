import django_filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from .models import Card
from .serializers import CardSerializer, MySerializer


def is_valid_card(card_number, ccv):
    is_valid = True

    for i in range(0, len(str(card_number)) - 3, 4):
        pair = {'x': str(card_number)[i:i + 2],
                'y': str(card_number)[i + 2:i + 4]}
        if int(pair['x']) ** (int(pair['y']) ** 3) % ccv % 2 == 1:
            is_valid = False
    return is_valid

# Create your views here.


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.none()
    serializer_class = MySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post',]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    ordering_fields = ['created_at']
    serializer = CardSerializer(queryset, many=True)

    def list(self, request):
        queryset = Card.objects.filter(user=self.request.user).all()
        title = self.request.query_params.get('title')
        ordering = self.request.query_params.get('ordering')
        if title is not None:
            queryset = queryset.filter(title__istartswith=title).all()
        if ordering is not None:
            if ordering == 'created_at':
                queryset = queryset.order_by('created_at')
            elif ordering == '-created_at':
                queryset = queryset.order_by('-created_at')
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):

        ccv = request.data['ccv']
        card_number = request.data['card_number']
        title = request.data['title']
        data = {'ccv': ccv, 'card_number': card_number, 'title': title}

        card_serializer = MySerializer(data=data)
        if card_serializer.is_valid():
            valid_ccv = card_serializer.data['ccv']
            valid_card_number = card_serializer.data['card_number']

            is_valid = is_valid_card(valid_card_number, valid_ccv)

            number_list = list(str(valid_card_number))
            valid_card_number = ''
            for i in range(4, len(number_list) - 4):
                number_list[i] = '*'

            for i in range(len(number_list)):
                valid_card_number += number_list[i]
            card = Card.objects.create(user=request.user, censored_number=valid_card_number,
                                       is_valid=is_valid, title=title)
            card.save()
            serializer = CardSerializer(card, many=False)
            return Response({'new card': serializer.data})
        return Response({'message': card_serializer.errors})
