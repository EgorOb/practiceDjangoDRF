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


    # class EntrySerializer(serializers.Serializer):
    #     blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    #     headline = serializers.CharField()
    #     body_text = serializers.CharField()
    #     pub_date = serializers.DateTimeField()
    #     mod_date = serializers.DateField(default=date.today())
    #     authors = serializers.PrimaryKeyRelatedField(
    #         queryset=Author.objects.all(),
    #         many=True)
    #     number_of_comments = serializers.IntegerField(default=0)
    #     number_of_pingbacks = serializers.IntegerField(default=0)
    #     rating = serializers.FloatField(default=0)
    #
    #     def create(self, validated_data):
    #         # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
    #         # Необходимо будет из данных как-то удалить authors и создать объект, а затем заполнить authors
    #         # Или передавать каждый параметр без authors
    #         authors = validated_data["authors"]
    #         validated_data.pop("authors")  # Удаляем авторов из словаря
    #         instance = Entry(**validated_data)  # Создаём объект
    #         instance.save()  # Сохраняем в БД
    #         instance.authors.set(authors)  # Заполняем все в связи многое ко многому
    #         return instance
    #
    #     def update(self, instance, validated_data):
    #         for tag, value in validated_data.items():
    #             if tag != 'authors':
    #                 setattr(instance, tag, value)
    #             else:
    #                 instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
    #         instance.save()  # Сохранение изменений в БД
    #         return instance
    #
    #
    # class MyView(APIView):
    #     permission_classes = [IsAuthenticated]
    #     authentication_classes = [JWTAuthentication]
    #
    #     def get(self, request):
    #         queryset = Entry.objects.all()  # Получаем все объекты модели
    #         serializer = EntrySerializer(queryset,
    #                                      many=True)  # Множество объектов для сериализации
    #
    #         return Response(serializer.data)

    # Создаем объект RequestFactory
    factory = APIRequestFactory()

    user_data = {
        "username": "admin",
        "password": "123"
    }

    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, OutstandingToken, BlacklistedToken
    from django.contrib.auth.models import User

    class CustomTokenObtainPairView(TokenObtainPairView):
        def post(self, request, *args, **kwargs):
            # Получаем пользователя по имени пользователя или email (в зависимости от ваших настроек)
            user = User.objects.get(username=request.data['username'])

            if user and user.is_active:
                # Если пользователь не заблокирован, продолжаем создавать токен
                return super().post(request, *args, **kwargs)
            else:
                return Response({'detail': 'Учетная запись заблокирована.'}, status=status.HTTP_401_UNAUTHORIZED)

    OutstandingToken.objects.all().delete()  # Очистка БД от передыдущих токенов в системе
    # Обработчик JWT для получения токена
    token_view = CustomTokenObtainPairView.as_view()
    # Передаём запрос на получение токена для пользователя
    request = factory.post('/token/', user_data, format='json')
    response = token_view(request)
    print(response.status_code)  # 200
    print(response.data)  # {"refresh": ..., "access": ...}

    # Теперь заблокируем пользователя
    user = User.objects.get(username=user_data['username'])
    user.is_active = False
    user.save()

    request = factory.post('/token/', user_data, format='json')
    response = token_view(request)
    print(response.status_code)  # 401
    print(response.data)  # {'detail': 'Учетная запись заблокирована.'}

    # Разблокируем пользователя
    user.is_active = True
    user.save()

    request = factory.post('/token/', user_data, format='json')
    response = token_view(request)
    print(response.status_code)  # 200
    print(response.data)  # {"refresh": ..., "access": ...}



    # # Узнать время создания 'iat' и время окончания 'exp'
    # # Получение времени жизни для токена обновления в секундах
    # print(data_token_refresh['exp'] - data_token_refresh['iat'])  # 30
    # # Получение времени жизни для доступа обновления в секундах
    # print(data_token_access['exp'] - data_token_access['iat'])  # 10
    # # Или можно узнать по атрибуту
    # print(data_token_refresh.lifetime, data_token_access.lifetime)  # 0:00:30 0:00:10
    #
    # import time
    # # Получение данных до истечения срока жизни токена доступа
    # view = MyView.as_view()
    #
    # # Создаем запрос и установливаем заголовок Authorization
    # request = factory.get('/my-view/')
    # request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"
    #
    # # Отправляем запрос с заголовком Authorization
    # response = view(request)
    # # Проверяем результат
    # print(response.status_code)  # 200
    #
    # # Ожидание некоторого времени для истечения срока
    # time.sleep(10)
    # # Новый запрос доступа
    # request = factory.get('/my-view/')
    # request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"
    #
    # # Отправляем запрос с заголовком Authorization
    # response = view(request)
    # # Проверяем результат
    # print(response.status_code)  # 401
    # print(response.data)  # {'detail': ErrorDetail(string='Given token not valid for any token type', code='token_not_valid'),
    # # 'code': ErrorDetail(string='token_not_valid', code='token_not_valid'),
    # # 'messages': [{'token_class': ErrorDetail(string='AccessToken', code='token_not_valid'),
    # # 'token_type': ErrorDetail(string='access', code='token_not_valid'),
    # # 'message': ErrorDetail(string='Token is invalid or expired', code='token_not_valid')}]}
    #
    # # Получаем новый токен за счёт обновления токена доступа
    # request = factory.post('/token/refresh/', {"refresh": refresh_token}, format='json')
    # refresh_view = TokenRefreshView.as_view()
    # response = refresh_view(request)
    # token_data = response.data
    #
    # # Новый токен доступа и токен обновления(так как стоит установка обновлять токен доступа после каждого запроса обновления)
    # access_token_new = token_data.get("access")
    # refresh_token_new = token_data.get("refresh")
    # print(access_token_new == access_token, refresh_token_new == refresh_token)  # False False
    #
    # # Так как токен обновления обновлен и стоит условие, что он попадает в черный список, значит от не действителен и не
    # # позволит заново обновить по прошлому токену обновления
    # request = factory.post('/token/refresh/', {"refresh": refresh_token}, format='json')
    # refresh_view = TokenRefreshView.as_view()
    # response = refresh_view(request)
    # print(response.data)  # {'detail': ErrorDetail(string='Token is blacklisted', code='token_not_valid'),
    # # 'code': ErrorDetail(string='token_not_valid', code='token_not_valid')}
    #
    # # Так же в БД можно посмотреть, что добавились токены в черный список(прошлый действующий токен refresh_token)
    # print(BlacklistedToken.objects.all())  # <QuerySet [<BlacklistedToken: Blacklisted token for admin>]>
    #
    # # Если ещё подождать пока истечет срок действия токена обновления, то уже придётся делать новый запрос
    # # на токен(TokenObtainPairView)
    # time.sleep(15)
    # request = factory.post('/token/refresh/', {"refresh": refresh_token_new}, format='json')
    # refresh_view = TokenRefreshView.as_view()
    # response = refresh_view(request)
    # print(response.data)  # {'detail': ErrorDetail(string='Token is invalid or expired', code='token_not_valid'),
    # # 'code': ErrorDetail(string='token_not_valid', code='token_not_valid')}
