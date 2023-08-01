import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь

    from rest_framework import serializers

    def validate_title(value):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value

    class BlogPostSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=100, required=False,
                                      validators=[validate_title])
        content = serializers.CharField()


    data = {'title': 'about',
            'content': '123'}
    serializer = BlogPostSerializer(data=data)
    print(serializer.is_valid())  # False
    print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
    print(serializer.validated_data)  # {}

    data = {'content': '123'}
    serializer = BlogPostSerializer(data=data)
    print(serializer.is_valid())  # True
    print(serializer.errors)  # {}
    print(serializer.validated_data)  # OrderedDict([('content', '123')])
