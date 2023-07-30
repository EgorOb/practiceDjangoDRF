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
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(),
                                                  write_only=True)
        headline = serializers.CharField()
        body_text = serializers.CharField()
        pub_date = serializers.DateTimeField()
        mod_date = serializers.DateField(default=date.today())
        authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                     many=True, write_only=True)
        number_of_comments = serializers.IntegerField(default=0)
        number_of_pingbacks = serializers.IntegerField(default=0)
        rating = serializers.FloatField(default=0)

        def create(self, validated_data):
            # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
            # Необходимо будет из данных как-то удалить authors и создать объект, а затем запонить authors
            # Или передавать каждый параметр без authors
            authors = validated_data["authors"]
            validated_data.pop("authors")  # Удаляем авторов из словаря
            instance = Entry(**validated_data)  # Создаём объект
            instance.save()  # Сохраняем в БД
            instance.authors.set(authors)  # Заполняем все всязи многое ко многому
            return instance
            """
            Если бы не было связей много ко многому, то можно было бы записать так вместо всех строк
            return Entry.objects.create(**validated_data)"""

        def update(self, instance, validated_data):
            instance.headline = validated_data.get('headline', instance.headline)
            instance.body_text = validated_data.get('body_text', instance.body_text)
            instance.pub_date = validated_data.get('pub_date', instance.pub_date)
            instance.mod_date = validated_data.get('mod_date', instance.mod_date)
            instance.number_of_comments = validated_data.get('number_of_comments', instance.number_of_comments)
            instance.number_of_pingbacks = validated_data.get('number_of_pingbacks', instance.number_of_pingbacks)
            instance.rating = validated_data.get('rating', instance.rating)
            instance.save()
            return instance

    data = {
        'blog': "1",
        'headline': 'Hello World',
        'body_text': 'This is my first blog post.',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': [1, 2, 3],
    }

    my_instance = MyModel.objects.get(pk=1)
    serializer = MySerializer(instance=my_instance,
                              data={'name': 'John', 'age': 30})


    serializer = EntrySerializer(data=data)
    if serializer.is_valid():
        print(repr(serializer.save()))  # <Entry: Hello World>
        """То что мы указали в данных 'blog': "1" не вызовет обновление данных, 
        создастся новая строка в БД. 
        Для обновления данных есть немного другая запись"""