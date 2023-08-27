import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework.test import APIRequestFactory
    from rest_framework import status  # Импортируем статусы HTTP
    from rest_framework.permissions import IsAuthenticated
    from rest_framework_simplejwt.authentication import JWTAuthentication

    from rest_framework import serializers
    from app.models import Entry, Blog, Author
    from datetime import date


    class EntrySerializer(serializers.Serializer):
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
        headline = serializers.CharField()
        body_text = serializers.CharField()
        pub_date = serializers.DateTimeField()
        mod_date = serializers.DateField(default=date.today())
        authors = serializers.PrimaryKeyRelatedField(
            queryset=Author.objects.all(),
            many=True)
        number_of_comments = serializers.IntegerField(default=0)
        number_of_pingbacks = serializers.IntegerField(default=0)
        rating = serializers.FloatField(default=0)

        def create(self, validated_data):
            # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
            # Необходимо будет из данных как-то удалить authors и создать объект, а затем заполнить authors
            # Или передавать каждый параметр без authors
            authors = validated_data["authors"]
            validated_data.pop("authors")  # Удаляем авторов из словаря
            instance = Entry(**validated_data)  # Создаём объект
            instance.save()  # Сохраняем в БД
            instance.authors.set(authors)  # Заполняем все в связи многое ко многому
            return instance

        def update(self, instance, validated_data):
            for tag, value in validated_data.items():
                if tag != 'authors':
                    setattr(instance, tag, value)
                else:
                    instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
            instance.save()  # Сохранение изменений в БД
            return instance


    class MyView(APIView):
        permission_classes = [IsAuthenticated]
        authentication_classes = [JWTAuthentication]

        def get(self, request):
            queryset = Entry.objects.all()  # Получаем все объекты модели
            serializer = EntrySerializer(queryset,
                                         many=True)  # Множество объектов для сериализации

            return Response(serializer.data)


    # Создаем объект RequestFactory
    factory = APIRequestFactory()

    user_data = {
        "username": "admin",
        "password": "123"
    }

    from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
    # Обработчик JWT для получения токена
    token_view = TokenObtainPairView.as_view()
    # Передаём запрос на получение токена для пользователя
    request = factory.post('/token/', user_data, format='json')
    response = token_view(request)
    token_data = response.data
    # Токен доступа
    access_token = token_data.get("access")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyOTczNTkzLCJpYXQiOjE2OTI5NzMyOTMsImp0aSI6IjViNWRhZDA0Yjg0ODQxOTRiODdiOGFhM2EyN2E0MTI5IiwidXNlcl9pZCI6MX0.8Ea7HDi5IyZqiQxwXjo6u50MZQW5rnoKO0xRPc-ifNc'
    # Проверка токена
    request = factory.post('/token/verify/', {"token": access_token}, format='json')
    refresh_view = TokenVerifyView.as_view()
    response = refresh_view(request)
    print(response.status_code)  # 200


