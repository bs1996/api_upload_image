from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Tiers, Customer, Images
from rest_framework import viewsets
from .serializers import ImagesSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from .image_data import image_data, image_link, convert_to_binary
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta
from rest_framework import permissions
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Create your views here.


@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))
        print(request.POST)
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is None:
            return HttpResponse("Invalid credentials.")
        login(request, user)
        current_user = request.user.id
        customer = Customer.objects.filter(user_id=current_user)
        if customer.exists():
            response = HttpResponse("logged successfully")
            response.set_cookie('login', '1')
        else:
            response = HttpResponse("User doesn't exist")
        return response


class ImagesViewSet(viewsets.ModelViewSet):

    serializer_class = ImagesSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Images.objects.filter(User_id=user.id)
        return queryset





@api_view(['GET'])
def Image(request, id, number, type):
    current_user = request.user
    image, height = image_link(current_user, number, type)
    return render(request, 'thumbnail.html', {'image': image, 'height': height})


class ImageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        current_user = request.user
        image = request.FILES['file'] if 'file' in request.FILES else False
        if image:
            links = image_data(current_user, image)
            return Response({'message': 'Successful', 'list': links})

        return Response({'message': 'Something went wrong'})


class GenerateLinkView(APIView):
    def post(self, request, number, time):
        current_user = request.user
        customer = Customer.objects.filter(user_id=current_user.id)
        account_type = customer[0].account_type_id
        account = Tiers.objects.filter(id=account_type)
        expire_link = account[0].expiring_links
        add_image = Images.objects.filter(number=number)
        link = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/' \
                          + str(add_image[0].number) + '/bin/'
        if expire_link:
            if time >= 300 and time <=30000:
                images = Images.objects.filter(number=number)
                image = images[0].image
                url = image.url
                convert_to_binary(url, number)
                token = AccessToken.for_user(request.user)
                token.set_exp(lifetime=timedelta(seconds=time))
                return Response({'link': link, 'token': str(token)})
            else:
                return Response({'message': 'expiration time should be between 300 and 30000 seconds'})

        else:
            return Response({'message': 'expiring links are not enabled for this account'})


class ValidateLinkView(APIView):
    def get(self, request, id, number):
        token = request.query_params.get('token')
        try:
            AccessToken(token).check_exp()
        except InvalidToken as e:
            return Response({'error': str(e)}, status=400)
        except TokenError as e:
            return Response({'error': str(e)}, status=400)
        image = Images.objects.filter(number=number)
        img_url = image[0].image.url
        img_name = image[0].image.name
        new_name = 'images/' + str(number) + 'bin.png'
        img_url2 = img_url.replace(img_name, new_name)
        height = '100%'
        return render(request, 'binary.html', {'url': img_url2, 'height': height})
