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

    from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
    from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, OutstandingToken, BlacklistedToken
    # Обработчик JWT для получения токена
    token_view = TokenObtainPairView.as_view()
    # Передаём запрос на получение токена для пользователя
    request = factory.post('/token/', user_data, format='json')
    response = token_view(request)
    # Как только отработал обработчик создания токена, то в таблице Outstanding tokens БД создался действующий токен
    token_data = response.data
    # Токен доступа
    access_token1 = token_data.get("access")
    refresh_token1 = token_data.get("refresh")

    # Работать с действующими токенами можно так(как с объектом модели)
    print(OutstandingToken.objects.all())  # <QuerySet [
    # <OutstandingToken: Token for admin (64363557b94b4253bbd95f029df03e01)>
    # ]>

    # В действующем токене хранится информация только о токене обновления. Библиотека подразумевает, что токен доступа
    # сохранит или пользователь или приложение пользователя. Вспомните как GitHub выдаёт свои токены для подключения IDE

    # Проверка, что в объекте БД хранится токен обновления
    print(refresh_token1 == OutstandingToken.objects.first().token)  # True

    # Создадим ещё пару токенов, чтобы потом добавить их в черный список разными способами
    request = factory.post('/token/', user_data, format='json')
    access_token2 = token_view(request).data.get("access")

    request = factory.post('/token/', user_data, format='json')
    access_token3 = token_view(request).data.get("access")

    print(OutstandingToken.objects.all())  # <QuerySet [
    # <OutstandingToken: Token for admin (64363557b94b4253bbd95f029df03e01)>,
    # <OutstandingToken: Token for admin (123ebcc07c1e40f6968d005f181ec908)>,
    # <OutstandingToken: Token for admin (ad249807841b4112a2c49ff7ca016116)>
    # ]>

    # access_token1, 2, 3 были сохранены специально, чтобы можно было проверить доступ к API, так как писалось ранее
    # через токен обновления можно только получить новый токен, а не узнать текущий.

    # 1. Использование класса представления TokenBlacklistView
    token_blacklist_view = TokenBlacklistView.as_view()
    # Просто отправляем запрос с доступом и токен попадёт в черный список автоматически
    request = factory.post('/blacklist/', {'token': access_token1, 'refresh': refresh_token1}, format='json')

    # Запомним jti (JSON Token ID) чтобы потом проверить, что токен есть в базе данных черного списка. Делается это
    # заранее, так как если вызвать после блокировки, то вызовется исключение, что токен заблокирован
    data_token = RefreshToken(refresh_token1)  # декодируем токен и получаем информацию
    print(data_token)  # {'token_type': 'refresh', 'exp': 1693401757, 'iat': 1693315357,
    # 'jti': 'f3d227af785d426b8c2b506700269693', 'user_id': 1}

    # Отработаем представление
    response = token_blacklist_view(request)

    # Проверка, что токен теперь в БД черного списка

    print(BlacklistedToken.objects.first().token.jti == data_token['jti'])







    #
    # OutstandingToken.objects.all().delete()


