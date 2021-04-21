from django.contrib import auth
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework import status, permissions, serializers
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
from booklist.models import AppUser, Books


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            form_data = json.loads(request.body.decode())
            print(form_data)
            username = form_data['username']
            print(username)
            first_name = form_data['first_name']
            last_name = form_data['last_name']
            middle_name = form_data['middle_name']
            password = form_data['password']
            email = form_data['email']
            account_type = form_data['account_type']
        except Exception as e:
            username = request.POST.get('username')
            print(username)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            middle_name = request.POST.get('middle_name')
            password = request.POST.get('password')
            email = request.POST.get('email')
            account_type = request.POST.get('account_type')

        try:
            if AppUser.objects.filter(username=username).exists():
                data = {"response": "The username already exists",
                        "success": False}

                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            elif AppUser.objects.filter(email=email).exists():
                data = {"response": "The email already exists", "success": False}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = AppUser.objects.create(username=username, first_name=first_name, last_name=last_name,
                                              middle_name=middle_name, email=email, account_type=account_type)
                user.set_password(password)
                user.save()
                token = Token.objects.create(user=user).key
                user_details = AppUser.objects.get(username=username)
                print(user)
                user1 = {
                    "username": user_details.username,
                    "first_name": user_details.first_name,
                    "middle_name": user_details.middle_name,
                    "last_name": user_details.last_name,
                    "email": user_details.email,
                    "account_type": user_details.account_type,
                }
                data = {
                    "response": "user created successfully",
                    "Token": token,
                    "userDetails": user1,
                    "success": True
                }
                return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {"response": "cannot sign you up due to" +
                    str(e), "success": False}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwarks):
        try:
            try:
                form_data = json.loads(request.body.decode())
                username = form_data['username']
                password = form_data['password']
            except Exception as e:
                username = request.POST.get('username')
                password = request.POST.get('password')

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                user_details = AppUser.objects.get(username=username)
                user_data = {
                    "username": user_details.username,
                    "first_name": user_details.first_name,
                    "middle_name": user_details.middle_name,
                    "last_name": user_details.last_name,
                    "email": user_details.email,
                    "account_type": user_details.account_type,
                }
                data = {
                    "response": "login successful",
                    "success": True,
                    "token": token.key,
                    "User": user_data
                }
                # data_set = serializers.serialize('json',data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"response": "login failed", "success": False}
                # data_set = serializers.serialize('json', data)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {"response": e, "success": False}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        data = {'response': "successfully logged you out", "success": True}
        return Response(data, status=status.HTTP_200_OK)


class BooksView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = serializers.BooksSerializerAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"response": "successfully added", "success": True}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({"response": "invalid data", "success": False}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        booksList = Books.objects.all()
        serializer = serializers.BookSerializerShow(booksList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        book_id = kwargs['book_id']
        try:
            book_detail = Books.objects.get(book_id=book_id)
            serializer = serializers.BookSerializerShow(book_detail)
            return Response(serializer.data)
        except Books.DoesNotExist:
            return Response({"response": "Book does not exist", "success": False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        book_id = kwargs['book_id']
        try:
            book_detail = Books.objects.get(book_id=book_id)
        except Books.DoesNotExist:
            return Response({"response": "edit unsuccessful", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BookSerializerShow(
            book_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"response": "edit successful", "success": True}
            return Response(data, status=status.HTTP_205_RESET_CONTENT)

    def delete(self, request, *args, **kwargs):
        book_id = kwargs['book_id']
        try:
            book_detail = Books.objects.get(book_id=book_id)
        except Books.DoesNotExist:
            return Response({"response": "delete unsuccessful", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        book_detail.delete()
        data = {"response": "successfully deleted the book", "success": True}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
