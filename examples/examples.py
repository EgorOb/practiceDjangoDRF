import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь

    from rest_framework import serializers
    from app.models import Entry


    class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Entry
            fields = '__all__'

    data = {
        'blog': 'http://example.com/blogs/1/',  # Гиперссылка на блог с id=1
        'headline': 'Hello',
        'body_text': 'World',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': ['http://example.com/authors/1/', 'http://example.com/authors/2/'],
        # Гиперссылки на авторов с id=1 и id=2
        'number_of_comments': 2,
        'rating': 0.0,
    }

    from django.test import RequestFactory

    # Создаем экземпляр RequestFactory
    factory = RequestFactory()

    # Создаем фейковый GET-запрос
    request = factory.get('/my-api-url/')  # Нужен путь на реальный обработчик DRF обрабатывающий данный сериализатор

    serializer = EntryHyperlinkedModelSerializer(data=data, context={'request': request})
    print(serializer.is_valid())  # True

    # Получение данных для сериализации
    print(serializer.data)
