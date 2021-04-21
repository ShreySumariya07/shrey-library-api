from rest_framework import serializers
from booklist.models import AppUser, Books


class AppRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['username', 'first_name', 'last_name',
                  'middle_name', 'email', 'account_type']


class AppLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['username', 'first_name', 'last_name',
                  'middle_name', 'email', 'account_type']


class BooksSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['title', 'genre', 'author',
                  'publication', 'description', 'image', 'pdf']


class BookSerializerShow(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = '__all__'
