import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь
    from datetime import date

    class EntrySerializer(serializers.Serializer):
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)
        headline = serializers.CharField()
        body_text = serializers.CharField()
        pub_date = serializers.DateTimeField()
        mod_date = serializers.DateField(default=date.today())
        authors = serializers.PrimaryKeyRelatedField(read_only=True,
                                                     many=True)
        number_of_comments = serializers.IntegerField(default=0)
        number_of_pingbacks = serializers.IntegerField(default=0)
        rating = serializers.FloatField(default=0)

        def create(self, validated_data):
            instance = Entry(**validated_data)  # Создаём объект
            instance.save()  # Сохраняем в БД (получим ошибку, так как в validated_data нет blog,
            # ввиду read_only=True)
            # django.db.utils.IntegrityError: NOT NULL constraint failed: app_entry.blog_id
            return instance

        def update(self, instance, validated_data):
            # При обновлении нет разницы, так как поля blog и authors не обновляются
            for tag, value in validated_data.items():
                setattr(instance, tag, value)
            instance.save()  # Сохранение изменений в БД
            return instance

    data = {
        'id': 1,
        'blog': "1",
        'headline': 'Hello World',
        'body_text': 'This is my first blog post.',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': [1, 2, 3],
    }

    # Обновление
    my_instance = Entry.objects.get(pk=data["id"])
    serializer = EntrySerializer(instance=my_instance, data=data)

    if serializer.is_valid():
        print(repr(serializer.save()))  # <Entry: Hello World>

    # Создание
    serializer = EntrySerializer(data=data)  # запись для создания объекта
    if serializer.is_valid():
        print(repr(serializer.save()))  # Получаем ошибку