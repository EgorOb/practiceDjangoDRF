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
        # Получение всех записей, или если был передан ключ с записью, то вывод
        # только одной записи
        def get(self, request):
            if request.GET.get('pk'):
                instance = Entry.objects.get(pk=request.GET.get('pk'))
                serializer = EntrySerializer(instance)
            else:
                queryset = Entry.objects.all()  # Получаем все объекты модели
                serializer = EntrySerializer(queryset,
                                             many=True)  # Множество объектов для сериализации

            return Response(serializer.data)

        # Создание новой записи
        def post(self, request):
            serializer = EntrySerializer(data=request.data)  # Используем сериализатор для обработки данных
            if serializer.is_valid():
                # Если данные валидны, сохраняем их или выполняем необходимые действия
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Обновление записи(чтобы обновлять, нужно знать где обновить, поэтому
        # в этот передадим значения в заголовке, а не параметрах запроса)
        def put(self, request):
            try:
                instance = Entry.objects.get(pk=request.data.get('id'))  # Получаем существующий объект
            except Entry.DoesNotExist:
                return Response({'message': 'Object not found'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = EntrySerializer(instance,
                                         data=request.data)  # Используем сериализатор для обновления данных
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        # Удаление записи
        def delete(self, request):
            try:
                instance = Entry.objects.get(pk=pk)  # Получаем существующий объект
            except Entry.DoesNotExist:
                return Response({'message': 'Object not found'},
                                status=status.HTTP_404_NOT_FOUND)

            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    # Данные для работы
    data = {
        'id': 1,
        'blog': "1",
        'headline': 'Hello World',
        'body_text': 'This is my first blog post.',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': [1, 2, 3],
    }

    # Создаем объект RequestFactory
    factory = APIRequestFactory()

    # Создаем экземпляр представления
    view = MyView.as_view()

    # Создаем объект get запроса (получение информации по ключу 1,
    # как пример передаётся прямо в параметрах запроса)
    request = factory.get('/my-view/?pk=1')  # Можно было бы написать маршрут
    # /my-view/1 (что было бы по принципу rest), но request самостоятельно
    # не парсит адрес, это делает сам Django, но только если вы
    # зарегистрировали данный маршрут допустим как path('/my-view/<pk:int>', ...)
    # тогда бы в get вашего обработчика можно было передать pk как входной параметр
    response = view(request)
    print(response.data)  # {
    # 'blog': 1,
    # 'headline': 'Изучение красот Мачу-Пикчу',
    # 'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд...',
    # 'pub_date': '2022-04-01T21:00:00Z', 'mod_date': '2023-07-17',
    # 'authors': [1, 9], 'number_of_comments': 2,
    # 'number_of_pingbacks': 10, 'rating': 0.0
    # }

    # Создаем объект get запроса (получение всей информации)
    request = factory.get('/my-view/')
    response = view(request)
    print(response.data)  # [
    # OrderedDict([
    # ('blog', 1),
    # ('headline', 'Изучение красот Мачу-Пикчу'),
    # ('body_text', 'Древний город Мачу-Пикчу, скрытый ... наследии.'),
    # ('pub_date', '2022-04-01T21:00:00Z'),
    # ('mod_date', '2023-07-17'),
    # ('authors', [1, 9]),
    # ('number_of_comments', 2),
    # ('number_of_pingbacks', 10),
    # ('rating', 0.0)]),
    # OrderedDict(...),
    # ...]

    # # Создаем объект post запроса (добавление данных)
    # request = factory.post('/my-view/', data=data)
    # response = view(request)
    # print(response.data)  # {'blog': 1, 'headline': 'Hello World',
    # # 'body_text': 'This is my first blog post.',
    # # 'pub_date': '2023-07-19T12:00:00Z',
    # # 'mod_date': '2023-08-18', 'authors': [1, 2, 3],
    # # 'number_of_comments': 0, 'number_of_pingbacks': 0, 'rating': 0.0}
    # print(Entry.objects.latest('id'))  # <Entry: Hello World>

    # Создаем объект put запроса (обновление данных)
    request = factory.put('/my-view/', data=data)
    response = view(request)
    print(response.data)  # {'message': 'PUT request received'}

    # Создаем объект delete запроса
    request = factory.delete('/my-view/', data={'id': 26})
    response = view(request)
    print(response.data)  # {'message': 'DELETE request received'}

