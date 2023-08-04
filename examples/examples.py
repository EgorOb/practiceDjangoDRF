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

        def validate(self, attrs):

            for key, val in attrs.items():
                if key in ['blog', 'authors']:
                    pass

        class Meta:
            model = Entry
            fields = '__all__'

    data = {
        'blog': 'http://example.com/blogs/1/',  # Гиперссылка на блог с id=1
        'headline': 'Hello',
        'body_text': 'World',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': ['http://example.com/authors/1/', 'http://example.com/authors/2/'], # Гиперссылки на авторов с id=1 и id=2
        'number_of_comments': 2,
        'rating': 0.0,
    }

    serializer = EntryHyperlinkedModelSerializer(data=data)
    print(serializer.is_valid())  # True  Хотя при проходе через http://example.com/authors/1/ ничего не обработается,
    # но обработчик получил значения из БД.
    print(serializer.validated_data)  # OrderedDict([('headline', 'Hello'), ('body_text', 'World'),
    # ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
    # ('number_of_comments', 2), ('rating', 0.0), ('blog', <Blog: Путешествия по миру>),
    # ('authors', [<Author: alexander89>, <Author: ekaterina_blog>])])

