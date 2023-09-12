import os
import time

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
    from rest_framework.pagination import PageNumberPagination

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
        pagination_class = PageNumberPagination()
        pagination_class.page_size_query_param = 'page_size'  # Одно из условий в документации, чтобы можно было
        # вытаскивать размер страницы из запроса
        queryset = Entry.objects.all()

        def get(self, request):
              # Получаем все объекты модели
            page = self.pagination_class.paginate_queryset(self.queryset, request, view=self)  # Выполните пагинацию
            if page is not None:
                serializer = EntrySerializer(page, many=True)
                return self.pagination_class.get_paginated_response(serializer.data)

            serializer = EntrySerializer(self.queryset,
                                         many=True)  # Множество объектов для сериализации

            return Response(serializer.data)

    # Создаем объект RequestFactory
    factory = APIRequestFactory()

    view = MyView.as_view()
    # Получение первых 10 записей блогов
    request = factory.get('/my-view/?page=1&page_size=10')
    response = view(request)
    print(response.data)  # OrderedDict([('count', 25), ('next', 'http://testserver/my-view/?page=2&page_size=10'),
    # ('previous', None), ('results', [OrderedDict([...]), ...])])
    print(len(response.data['results']))  # 10

    # Получение вторых 10 записей блогов
    request = factory.get('/my-view/?page=2&page_size=10')
    response = view(request)
    print(response.data)  # OrderedDict([('count', 25), ('next', 'http://testserver/my-view/?page=3&page_size=10'),
    # ('previous', 'http://testserver/my-view/?page_size=10'), ('results', [OrderedDict([...]), ...])])
    print(len(response.data['results']))  # 10

    # Получение остатка записей
    request = factory.get('/my-view/?page=3&page_size=10')
    response = view(request)
    print(response.data)  # OrderedDict([('count', 25), ('next', None),
    # ('previous', 'http://testserver/my-view/?page=2&page_size=10'), ('results', [OrderedDict([...]), ...])])
    print(len(response.data['results']))  # 5



