import django_filters
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from .models import Card
from .serializers import CardSerializer, MySerializer
# Create your views here.


# class CardViewSet(viewsets.ViewSet):
#
#     permission_classes = [IsAuthenticated]
#     filterset_fields = ['title']
#
#     def list(self, request):
#         queryset = Card.objects.all()
#         serialized = CardSerializer(queryset, many=True)
#         return Response(serialized.data)
#
#     def create(self, request):
#
        # ccv = request.GET.get('ccv')
        # card_number = request.GET.get('card_number')
        # data = {'ccv': ccv, 'card_number': card_number}
        #
        # df = MySerializer(data=data)
        # if df.is_valid():
        #     valid_ccv = df.data['ccv']
        #     valid_card_number = df.data['card_number']
        #     is_valid = True
        #
        #     for i in range(0, len(str(valid_card_number))-3, 4):
        #         pair = {'x': str(valid_card_number)[i:i+2],
        #                 'y': str(valid_card_number)[i+2:i+4]}
        #         is_odd = int(pair['x']) ** (int(pair['y']) ** 3) % valid_ccv % 2 == 1
        #         if is_odd:
        #             is_valid = False
        #         print(f'{pair['x']}, {pair['y']}')
        #         print('odd - ', is_odd)
        #     number_list = list(str(valid_card_number))
        #     valid_card_number = ''
        #     for i in range(4, len(number_list)-4):
        #         number_list[i] = '*'
        #
        #     for i in range(len(number_list)):
        #         valid_card_number += number_list[i]
        #     print(valid_card_number)
        #     card = Card.objects.create(user=request.user, card_number=valid_card_number, is_valid=is_valid,
        #                                )
#
#             return Response(df.data)
#         return Response({'message': 'Some errors!'})



class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.none()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post',]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_backends += [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title']
    ordering_fields = ['created_at']
    #search_fields = ['title']
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
        # user = request.user
        #
        # data = request.data
        # data1 = {'title': data['title'], 'censored_number': data['censored_number']}
        # try:
        #     data1['is_valid'] = data['is_valid']
        # except Exception as e:
        #     print(e)
        # data1['user'] = request.user
        # print(data1)
        #
        ccv = request.data['ccv']
        card_number = request.data['card_number']
        title = request.data['title']
        data = {'ccv': ccv, 'card_number': card_number, 'title': title}

        df = MySerializer(data=data)
        if df.is_valid():
            valid_ccv = df.data['ccv']
            valid_card_number = df.data['card_number']
            is_valid = True

            for i in range(0, len(str(valid_card_number)) - 3, 4):
                pair = {'x': str(valid_card_number)[i:i + 2],
                        'y': str(valid_card_number)[i + 2:i + 4]}
                is_odd = int(pair['x']) ** (int(pair['y']) ** 3) % valid_ccv % 2 == 1
                if is_odd:
                    is_valid = False
                print(f'{pair['x']}, {pair['y']}')
                print('odd - ', is_odd)
            number_list = list(str(valid_card_number))
            valid_card_number = ''
            for i in range(4, len(number_list) - 4):
                number_list[i] = '*'

            for i in range(len(number_list)):
                valid_card_number += number_list[i]
            print(valid_card_number)
            card = Card.objects.create(user=request.user, censored_number=valid_card_number,
                                       is_valid=is_valid, title=title)
            card.save()
            serializer = CardSerializer(card, many=False)
            return Response({'new card': serializer.data})
        return Response({'message': 'Validation error!'})

    # def filter_queryset(self, queryset):
    #     title = self.request.query_params.get('title')
    #     card = Card.objects.filter(title__icontains=title).all()
    #     serializer = CardSerializer(card, many=True)
    #     return Response(serializer.data)



# @api_view(['GET', 'POST'])
# def index(request):
#     if request.method == 'GET':
#         cards = Card.objects.all()
#         serializer = CardSerializer(cards, many=True)
#         content = {
#             'language': 'python',
#             'framework': 'django',
#             'version': '5.1.2',
#             'editor': 'pycharm',
#             'cards': serializer.data
#                    }
#         return Response(content)
#     elif request.method == 'POST':
#         content = request.data
#         print(content['country'])
#         return Response(content)
