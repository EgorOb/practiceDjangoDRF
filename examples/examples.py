import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь
    from datetime import datetime
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
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), read_only=True)
        headline = serializers.CharField()
        body_text = serializers.CharField()
        pub_date = serializers.DateTimeField()
        mod_date = serializers.DateField(default=datetime.now())
        authors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        number_of_comments = serializers.IntegerField(default=0)
        number_of_pingbacks = serializers.IntegerField(default=0)
        rating = serializers.FloatField(default=0)

        def create(self, validated_data):
            return Entry.objects.create(**validated_data)

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

    # data = {
    #     'blog': 1,
    #     'headline': 'Hello World',
    #     'body_text': 'This is my first blog post.',
    #     'pub_date': '2023-07-19T12:00:00Z',
    # }

    data = dict(*Entry.objects.filter(id=1).values())
    serializer = EntrySerializer(data=data)
    serializer.is_valid()
    serializer.data
    # serializer = EntrySerializer(data=data)
    # serializer.is_valid()
    # serializer.save()
    # print()