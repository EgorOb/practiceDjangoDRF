import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь

    from rest_framework import serializers
    from app.models import Entry, Blog

    # поле blog через PrimaryKeyRelatedField
    class EntrySerializer(serializers.Serializer):
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

    serializer = EntrySerializer(Entry.objects.get(id=4))
    print(serializer.data)  # {'blog': 1}

    # поле blog через StringRelatedField
    class EntrySerializer(serializers.Serializer):
        blog = serializers.StringRelatedField()

    serializer = EntrySerializer(Entry.objects.get(id=4))
    print(serializer.data)  # {'blog': 'Путешествия по миру'}
