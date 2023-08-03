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


    serializer = EntryHyperlinkedModelSerializer()
    print(serializer)
    """EntryHyperlinkedModelSerializer():
        url = HyperlinkedIdentityField(view_name='entry-detail')
        headline = CharField(max_length=255)
        body_text = CharField(style={'base_template': 'textarea.html'})
        pub_date = DateTimeField(required=False)
        mod_date = DateField(read_only=True)
        number_of_comments = IntegerField(required=False)
        number_of_pingbacks = IntegerField(required=False)
        rating = FloatField(required=False)
        blog = HyperlinkedRelatedField(queryset=Blog.objects.all(), view_name='blog-detail')
        authors = HyperlinkedRelatedField(allow_empty=False, many=True, queryset=Author.objects.all(), view_name='author-detail')"""

    # Создание новой строки в БД
    data = {
        'blog': "1",
        'headline': 'Hello',
        'body_text': 'World',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': [1, 2],
        'number_of_comments': 2,
        'rating': 0.0,
    }

    serializer = EntryHyperlinkedModelSerializer(data=data)
    print(serializer.is_valid())  # False
    print(serializer.errors)  # {'blog': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')],
    # 'authors': [ErrorDetail(string='Incorrect type. Expected URL string, received int.', code='incorrect_type')]}

    # В этом кроется основное отличие от ModelSerializer, так как в HyperlinkedModelSerializer для связанных полей
    # передаются не id, а url по которым обрабатываются данные объекты

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
    print(serializer.is_valid())  # False
    # Однако даже сейчас будет ошибка так как нет обработчика корректно отрабатывающего по приведенным ссылкам.
    # Гиперссылки/URL должны указывать на конкретные представления (view) в вашем приложении,
    # которые обрабатывают соответствующие запросы.
    print(serializer.errors)  # {'blog': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')],
    # 'authors': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')]}
