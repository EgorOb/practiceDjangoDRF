import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь
    from datetime import date
    from django.utils import timezone
    # class EntrySerializer(serializers.Serializer):
    #     blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    #     headline = serializers.CharField()
    #     body_text = serializers.CharField()
    #     pub_date = serializers.DateTimeField()
    #
    #
    # data = {
    #     'blog': 1,
    #     'headline': 'Hello World',
    #     'body_text': 'This is my first blog post.',
    #     'pub_date': '2023-07-19T12:00:00Z',
    # }
    #
    # serializer = EntrySerializer(data=data)
    # print(serializer)
    # print(serializer.is_valid())
    # print(serializer.data)
    # print(serializer.errors)
    class EntrySerializer(serializers.Serializer):
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
        headline = serializers.CharField()
        body_text = serializers.CharField()
        pub_date = serializers.DateTimeField()
        mod_date = serializers.DateField(default=date.today())
        authors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        number_of_comments = serializers.IntegerField(default=0)
        number_of_pingbacks = serializers.IntegerField(default=0)
        rating = serializers.FloatField(default=0)

        # def create(self, validated_data):
        #     return Entry.objects.create(**validated_data)
        #
        # def update(self, instance, validated_data):
        #     instance.headline = validated_data.get('headline', instance.headline)
        #     instance.body_text = validated_data.get('body_text', instance.body_text)
        #     instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        #     instance.mod_date = validated_data.get('mod_date', instance.mod_date)
        #     instance.number_of_comments = validated_data.get('number_of_comments', instance.number_of_comments)
        #     instance.number_of_pingbacks = validated_data.get('number_of_pingbacks', instance.number_of_pingbacks)
        #     instance.rating = validated_data.get('rating', instance.rating)
        #     instance.save()
        #     return instance

    data = {
        'blog': "1",
        'headline': 'Hello World',
        'body_text': 'This is my first blog post.',
        'pub_date': '2023-07-19T12:00:00Z',
    }

    # data = dict(*Entry.objects.filter(id=1).values())
    serializer = EntrySerializer(data=data)
    print(serializer.is_valid())  # True
    print(serializer.validated_data)  # OrderedDict([('blog', <Blog: Путешествия по миру>), ('headline', 'Hello World'),
    # ('body_text', 'This is my first blog post.'), ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
    # ('mod_date', datetime.date(2023, 7, 28)), ('number_of_comments', 0), ('number_of_pingbacks', 0), ('rating', 0)])
    print(serializer.data)  # {'blog': 1, 'headline': 'Hello World', 'body_text': 'This is my first blog post.',
    # 'pub_date': '2023-07-19T12:00:00Z', 'mod_date': '2023-07-28', 'number_of_comments': 0, 'number_of_pingbacks': 0,
    # 'rating': 0.0}

    """В data ключ 'blog' c неверной валидацией, так как ожидается ссылка на отношение к ключу строки таблицы БД. Валидация
    проверяет существование ключа, поэтому ключ 0, -1, 100(так как его просто не существует записи в БД по такому ключу)
    не пройдут валидацию"""
    data = {
        'blog': "rr",
        'headline': 'Hello World',
        'body_text': 'This is my first blog post.',
        'pub_date': '2023-07-19T12:00:00Z',
    }

    serializer = EntrySerializer(data=data)
    print(serializer.is_valid())  # False
    print(serializer.errors)  # {'blog': [ErrorDetail(string='Incorrect type. Expected pk value, received str.', code='incorrect_type')]}
    print(serializer.validated_data)  # {}
    #  Так как валидация не прошла, то и данные с БД не были подтянуты при сериализации. Данные показывает, те, что были на входе
    print(serializer.data)  # {'blog': rr, 'headline': 'Hello World', 'body_text': 'This is my first blog post.',
    # 'pub_date': '2023-07-19T12:00:00Z'}




    # serializer = EntrySerializer(data=data)
    # serializer.is_valid()
    # serializer.save()
    print()