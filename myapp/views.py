from django.shortcuts import render
from rest_framework.views import APIView

from content.models import Feed
from user.models import User


class Sub(APIView):
    def post(self,request):
        return render(request,"instagram/main.html")

    def get(self,request):
        return render(request,"instagram/main.html")

