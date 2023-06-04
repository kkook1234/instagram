import os
from uuid import uuid4

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from myproject.settings import MEDIA_ROOT
from .models import User
from django.contrib.auth.hashers import make_password

class Join(APIView):
    def get(self,request):
        return render(request,"user/join.html")

    def post(self, request):
        # TODO 회원가입
        email=request.data.get('email',None)
        nickname=request.data.get('nickname',None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)
        User.objects.create(email=email,
                           nickname=nickname,
                           name=name,
                           password=make_password(password),
                           profile_image='default_profile.jpg')
        return Response(status=200)

class Login(APIView):
        def get(self, request):
            return render(request, "user/login.html")

        def post(self,request):
            #TODO 로그인
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            user=User.objects.filter(email=email).first()

            if user is None:
                return Response(status=404,data=dict(massage="회원정보가 잘못되었습니다."))

            if user.check_password(password):
                # TODO 로그인을 했다.세션 or 쿠키
                request.session['email']=email # 세션에 이용자 이메일 저장
                return Response(status=200)
            else:
                return Response(status=404, data=dict(massage="비밀번호가 잘못되었습니다."))


class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request,"user/login.html")

class UploadProfile(APIView):
        def post(self, request):
            file = request.FILES['file']
            email=request.data.get('email')

            uuid_name=uuid4().hex
            save_path = os.path.join(MEDIA_ROOT, uuid_name)

            with open(save_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            profile_image = uuid_name

            user=User.objects.filter(email=email).first()

            user.profile_image=profile_image
            user.save()


            return Response(status=200)
