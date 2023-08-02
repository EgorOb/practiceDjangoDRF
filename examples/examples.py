import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == "__main__":
    from rest_framework import serializers
    from app.models import Entry, Blog, Author, AuthorProfile
    # Проверьте куски кода здесь

    from rest_framework import serializers, validators
    from app.models import Entry, Blog, Author
    from datetime import date


    class EntrySerializer(serializers.Serializer):
        blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
        headline = serializers.CharField()
        body_text = serializers.CharField()
        pub_date = serializers.DateTimeField()
        mod_date = serializers.DateField(default=date.today())
        authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                     many=True)
        number_of_comments = serializers.IntegerField(default=0)
        number_of_pingbacks = serializers.IntegerField(default=0)
        rating = serializers.FloatField(default=0)

        def validate(self, data):
            errors = {}
            unique_validator = validators.UniqueValidator(queryset=Entry.objects.all())
            try:
                unique_validator(data, self.fields['headline'])
            except serializers.ValidationError as e:
                # Добавляем свои собственные ошибки, если есть конфликты уникальности
                errors['non_field_errors'] = e.detail

            # Вызываем валидатор UniqueTogetherValidator с переданными данными
            unique_together_validator = serializers.UniqueTogetherValidator(
                queryset=Entry.objects.all(),
                fields=['number_of_comments', 'body_text']
            )
            try:
                unique_together_validator(data, self)
            except serializers.ValidationError as e:
                # Добавляем свои собственные ошибки, если есть конфликты уникальности
                errors['non_field_errors'] = e.detail

            # Дополнительная логика проверок и валидаций здесь
            # ...

            unique_year_validator = serializers.UniqueForYearValidator(
                    queryset=Entry.objects.all(),
                    field='rating',
                    date_field='pub_date'
                )
            try:
                unique_year_validator(data, self)
            except serializers.ValidationError as e:
                # Добавляем свои собственные ошибки, если есть конфликты уникальности
                for field, error in e.detail.items():
                    errors[field] = error

            if errors:
                raise serializers.ValidationError(errors)

            return data


    data = {
        'blog': "1",
        'headline': 'Изучение красот Мачу-Пикчу',
        'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                     'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                     'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                     'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                     'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                     'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': [1],
        'number_of_comments': 2,
        'rating': 0.0,
    }
    serializer = EntrySerializer(data=data)
    print(serializer.is_valid())  # False
    print(serializer.errors)  # {'headline': [ErrorDetail(string='This field must be unique.', code='unique')]}
