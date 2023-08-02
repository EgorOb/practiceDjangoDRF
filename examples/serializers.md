## Сериализатор

Сериализаторы можно создать в любом удобном месте в коде вашего проекта, но есть ещё подход отнести под них отдельный
определенный файл такой как `serializers.py` что и будет сделано в приложении `app`.

Сериализатор создаётся как класс наследующийся от базового класса. 

Под базовым классом чаще всего бывает:

* `BaseSerializer` - Является базовым абстрактным классом, от которого наследуются другие сериализаторы в DRF.
Этот класс предоставляет основные функциональные возможности для сериализации и десериализации данных, но он не предоставляет 
никакой конкретной реализации для различных типов данных или моделей. Может понадобиться в случае необходимости 
создание своего типа сериализатора. 


* `Serializer` - Является основным классом сериализатора в DRF. Он предоставляет мощные функциональные возможности для 
сериализации и десериализации различных типов данных, включая словари, списки, модели Django и другие.
Serializer используется для создания сериализаторов, которые могут преобразовывать сложные структуры данных в форматы JSON 
или другие форматы для передачи через API.
Этот класс обычно используется для сериализации единичных объектов или сложных структур данных.


* `ListSerializer` - Является специальным классом сериализатора, который предоставляет дополнительные возможности для сериализации списков объектов.
Этот класс позволяет определить особое поведение для сериализации списка объектов, когда вам нужно производить дополнительные манипуляции с каждым объектом списка.
ListSerializer используется для сериализации списков объектов и может быть полезен, когда вам нужно контролировать сериализацию 
элементов списка или добавить дополнительные данные к каждому объекту.


* `ModelSerializer` - Предоставляет простой и удобный способ автоматической сериализации и десериализации моделей Django.
Он обрабатывает все поля модели, включая внешние ключи и связи многие-к-одному или многие-ко-многим.
С помощью ModelSerializer вы можете легко создавать API для вашей модели, которое позволяет выполнять операции CRUD 
(создание, чтение, обновление, удаление) с данными модели.
Кроме того, ModelSerializer автоматически создает валидаторы, основанные на вашей модели, и обрабатывает валидацию данных при десериализации.


* `HyperlinkedModelSerializer` - предоставляет те же функциональные возможности, что и ModelSerializer, но с 
добавленным функционалом гиперссылок (URL-ссылок) для связанных моделей.
Когда используется HyperlinkedModelSerializer, связанные модели представляются в виде URL-ссылок, а не как простые идентификаторы (Primary Keys). 
Это делает представление данных более удобным и навигируемым для клиентов.
При использовании HyperlinkedModelSerializer, клиенты могут получить доступ к связанным объектам, следуя гиперссылкам, 
что упрощает навигацию и обмен данными между различными частями вашего API.
Для работы с HyperlinkedModelSerializer необходимо настроить URL-маршруты для представления гиперссылок.


Базовые классы находятся в `rest_framework.serializers`
```python
from rest_framework.serializers import BaseSerializer, Serializer, \
    ListSerializer, ModelSerializer, HyperlinkedModelSerializer
```

Код сериализаторов можно посмотреть по пути `venv\Lib\site-packages\rest_framework\serializers.py`

### Методы и атрибуты объекта сериализатора

У объектов сериализаторов есть разные методы:

* `is_valid(raise_exception=False)`: Метод, который проверяет валидность данных, переданных в сериализатор. 
Возвращает True, если данные прошли валидацию, и False в противном случае.


* `save()`: Метод, используемый для создания или обновления объекта в базе данных 
на основе десериализованных данных (serializer.validated_data). 
Обычно используется c методами `create` и `update`. Метод save() получится 
использовать при определенных методах `create` и `update`.


* `validate(attrs)`: Метод для пользовательской валидации данных в сериализаторе. 
Он предназначен для выполнения дополнительных проверок и валидации данных, которые 
не связаны с отдельными полями. Когда объект сериализатора проходит первичную 
валидацию (включая проверку типов данных, валидацию полей и т. д.), метод `validate(attrs)` 
позволяет выполнить дополнительные проверки на основе всего набора переданных 
атрибутов (attrs). В этом методе можно определить сложную логику валидации, 
которая зависит от нескольких полей или требует взаимодействия с базой данных 
или другими сервисами.

Пример дополнительной пользовательской валидации
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if len(name) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")

        if age < 18:
            raise serializers.ValidationError("Age must be at least 18.")

        return attrs
```

* `validate_empty_values(data)`: Метод, который выполняет валидацию для пустых значений полей. 
Это позволяет определить, какие поля могут быть пустыми и какие не могут.


* `get_fields()`: Метод, который возвращает словарь всех полей, объявленных в сериализаторе. 
Эти поля определяют, какие данные будут сериализованы и десериализованы.


* `bind(field_name, parent)`: Метод, который привязывает сериализатор к определенному контексту, 
такому как представление или запрос. Этот метод вызывается автоматически при создании 
объекта сериализатора.


* `get_value(dictionary)`: Метод, который получает значение для заданного атрибута из исходных 
данных, которые были переданы сериализатору.


* `fail(key)`: Метод, который вызывается, когда происходит ошибка валидации данных. 
Он используется для создания сообщений об ошибках.


* `get_attribute(instance)`: Метод, который получает атрибут из исходных данных, 
на которых производится сериализация или десериализация.


* `get_default()`: Метод, который возвращает значение по умолчанию для поля, если 
оно не было передано в исходных данных.


* `get_initial()`: Метод, который возвращает значение по умолчанию для поля, которое 
будет использоваться в исходных данных, если значение не было передано.


* `get_validators()`: Метод, который возвращает список всех валидаторов, применяемых 
к полю.


* `mani_init()`: Метод, который выполняется при инициализации сериализатора. 
Он позволяет настроить сериализатор перед его использованием.


* `run_validators(value)`: Метод, который выполняет все валидаторы для заданного поля.


* `run_validation(data)`: Метод, который выполняет все валидации для заданного поля, 
включая валидации по умолчанию, пользовательские валидации и валидации связанных полей. 
Этот метод вызывается во время процесса десериализации, когда данные из запроса 
или другого источника передаются в сериализатор для преобразования в объекты Python 
(при создании) или обновления существующих объектов (при обновлении). 
Метод `run_validation(data)` выполняет различные проверки, валидации и преобразования 
данных, чтобы убедиться, что они соответствуют ожидаемому формату и типам полей в сериализаторе.

Методы переопределяемые для создания своих сериализаторов:

* `to_representation(instance)`: Метод, который преобразует объект модели (instance) 
в словарь или другой формат данных, который будет использоваться при сериализации. 
Этот метод обычно вызывается для каждого объекта в QuerySet, когда выполняется 
сериализация списка объектов. 


* `to_internal_value(data)`: Метод, который преобразует входные данные (data), 
полученные из запроса, во внутренний формат данных, используемый в сериализаторе 
(serializer.validated_data). Этот метод обычно вызывается перед валидацией данных.

Методы переопределяемые для возможности создания и обновления элеменов в БД:

* `create(validated_data)`: Метод, который создает объект модели на основе 
валидированных данных (validated_data). Обычно используется с serializer.save() 
для создания нового объекта.


* `update(instance, validated_data)`: Метод, который обновляет существующий объект 
модели (instance) на основе валидированных данных (validated_data). Обычно используется 
с serializer.save() для обновления объекта.

У объектов сериализаторов есть разные атрибуты:

* `data`: Атрибут, который хранит сериализованные данные, готовые для отправки 
в ответе API. Эти данные представлены в виде Python-словаря (или другого подходящего 
для формата данных), соответствующего структуре вашего сериализатора. В `data` 
содержит данные, которые уже были сериализованы и готовы для отправки клиенту.


* `validated_data`: Атрибут, который хранит десериализованные и валидированные данные, 
полученные из входных данных (например, из запроса). После прохождения валидации, 
данные из входного запроса преобразуются в правильные типы Python и проходят проверку 
на соответствие заданным правилам валидации. В `validated_data` хранятся только 
данные, прошедшие валидацию.


* `initial_data`: Атрибут, который хранит необработанные данные, полученные из запроса, 
до их десериализации. Эти данные могут быть изменены в процессе валидации или десериализации.


* `errors`: Атрибут, который хранит словарь с ошибками валидации. Если данные 
не прошли валидацию, здесь будут содержаться соответствующие ошибки.


* `context`: Атрибут, который хранит контекст, переданный в сериализатор из представления. 
Этот контекст может содержать дополнительную информацию, которая может быть полезна при сериализации.


* `instance`: Атрибут, который хранит объект модели, который был создан или 
обновлен после вызова serializer.save().

И другие атрибуты

### Примеры использования сериализаторов

Ниже рассмотрим пару примеров создания сериализаторов разными классами на примере 
одной задачи, `создать сериализатор API, позволяющего получить все записи блогов`.

### Serializer

Ниже приведен пример для случая сериализации, без возможности создания или обновления
объекта БД.

```python
from rest_framework import serializers
from app.models import Blog, Author, Entry
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    # Для работы с поле много ко многому указываем many=True
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

# Можно передавать объекты БД
serializer = EntrySerializer(Entry.objects.get(pk=3))
print(serializer.data)  # {'blog': 1, 'headline': 'Знакомство с Парижем', 'body_text':
# 'Париж - город любви, искусства и изысканности. \nЗнакомство с Парижем - это погружение в его узкие улочки,
# исторические \nдостопримечательности и культурную сцену. Прогулка по набережной Сены, \nпосещение Эйфелевой башни,
# музея Лувр и собора Парижской Богоматери - \nэто всего лишь некоторые из знаковых мест, которые стоит посетить.
# \nПарижские кафе, булочные и рестораны предлагают богатство французской \nкухни и возможность насладиться неповторимой
# атмосферой этого \nудивительного города.', 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'authors': [2, 4, 6], 'number_of_comments': 7, 'number_of_pingbacks': 5, 'rating': 4.7}

# Чтобы сериализовать в Json можно воспользоваться JSONRenderer или как пример стандартной библиотекой json
from rest_framework.renderers import JSONRenderer
print(JSONRenderer().render(serializer.data))
import json
print(json.dumps(serializer.data, ensure_ascii=False).encode())  # Результат аналогичный выше

# Для десериализации из Json можно воспользоваться JSONParser или как пример стандартной библиотекой json
data_json = JSONRenderer().render(serializer.data)
import io
from rest_framework.parsers import JSONParser
stream = io.BytesIO(data_json)
data = JSONParser().parse(stream)  # JSONParser читает объекты потока
print(data)  # {'blog': 1, 'headline': 'Знакомство с Парижем', 'body_text': 'Париж - город любви, искусства и изысканности.
# \nЗнакомство с Парижем - это погружение в его узкие улочки, исторические \nдостопримечательности и культурную сцену.
# Прогулка по набережной Сены, \nпосещение Эйфелевой башни, музея Лувр и собора Парижской Богоматери - \nэто всего лишь
# некоторые из знаковых мест, которые стоит посетить. \nПарижские кафе, булочные и рестораны предлагают богатство французской
# \nкухни и возможность насладиться неповторимой атмосферой этого \nудивительного города.',
# 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17', 'authors': [2, 4, 6], 'number_of_comments': 7,
# 'number_of_pingbacks': 5, 'rating': 4.7}

print(json.loads(data_json.decode()))  # Результат аналогичный выше

"""Также можно передавать непосредственно данные, но механизм сериализатора устроен так, что если передаются данные,
то их необходимо предварительно валидировать и затем произойдут дальнейшие необходимые запросы в БД
Если данные не валидны, то атрибут validated_data будет пустым"""
data = {
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True. Без вызова is_valid не получится получить validated_data или errors
print(serializer.validated_data)  # OrderedDict([('blog', <Blog: Путешествия по миру>),
# ('headline', 'Hello World'), ('body_text', 'This is my first blog post.'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
# ('mod_date', datetime.date(2023, 7, 30)),
# ('authors', [<Author: alexander89>, <Author: ekaterina_blog>, <Author: maxim_writer>]),
# ('number_of_comments', 0), ('number_of_pingbacks', 0), ('rating', 0)])
print(serializer.data)  # {'blog': 1, 'headline': 'Hello World',
# 'body_text': 'This is my first blog post.', 'pub_date': '2023-07-19T12:00:00Z',
# 'mod_date': '2023-07-30', 'authors': [1, 2, 3], 'number_of_comments': 0,
# 'number_of_pingbacks': 0, 'rating': 0.0}

"""В data ключ 'blog' c неверной валидацией, так как ожидается ссылка на отношение к ключу строки таблицы БД. Валидация
проверяет существование ключа, поэтому ключ 0, -1, 100(так как его просто не существует записи в БД по такому ключу)
не пройдут валидацию"""
data = {
    'blog': "rr",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'blog': [ErrorDetail(string='Incorrect type. 
# Expected pk value, received str.', code='incorrect_type')]}
print(serializer.validated_data)  # {}
#  Так как валидация не прошла, то и данные с БД не были подтянуты при сериализации. Данные показывает, те, что были на входе
print(serializer.data)  # {'blog': 'rr', 'headline': 'Hello World',
# 'body_text': 'This is my first blog post.', 'pub_date': '2023-07-19T12:00:00Z',
# 'authors': [1, 2, 3]}
```

Если необходимо иметь возможность создания или обновления объекта БД(или вашей модели) после валидации, 
то необходимо переопределить методы`create(self, validated_data)` или 
`update(self, instance, validated_data)` в которых необходимо описать какой объект 
возвращается в случае создания и обновления.

#### Создание объекта в БД

Если экземпляр сериализатора создан с использованием данных из запроса или 
другого источника (например, `serializer = MySerializer(data=request.data)`), 
и эти данные проходят валидацию (метод `is_valid()` возвращает `True`), 
то DRF выполняет создание нового объекта в базе данных с использованием метода 
`create()` сериализатора.

```python
from rest_framework import serializers
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

    def create(self, validated_data):
        # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
        # Необходимо будет из данных как-то удалить authors и создать объект, а затем заполнить authors
        # Или передавать каждый параметр без authors
        authors = validated_data["authors"]
        validated_data.pop("authors")  # Удаляем авторов из словаря
        instance = Entry(**validated_data)  # Создаём объект
        instance.save()  # Сохраняем в БД
        instance.authors.set(authors)  # Заполняем все в связи многое ко многому
        return instance
        """
        Если бы не было связей много ко многому, то можно было бы записать так вместо всех строк
        return Entry.objects.create(**validated_data)"""

data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
if serializer.is_valid():
    print(repr(serializer.save()))  # <Entry: Hello World>
    """То что мы указали в данных 'id': "1" не вызовет обновление данных, 
    создастся новая строка в БД. 
    Для обновления данных есть немного другая запись"""
```

То что мы указали в данных 'blog': "1" не вызовет обновление данных, создастся 
новая строка в БД. Для обновления данных есть немного другая запись.

#### Обновление объекта в БД

Если экземпляр сериализатора создан с существующим объектом из базы данных 
(например, `serializer = MySerializer(instance=my_instance)`), и обновляемые данные 
проходят валидацию, то DRF выполняет обновление существующего объекта в базе данных 
с использованием метода `update()` сериализатора. 

Именно наличие `instance` при инициализации сериализатора определяет что будет 
обновление, а не создание нового объекта.

Допустим объявим сразу и `create` и `update`, а решение будем принимать исходя 
из наличия `id` блога в принимаемых данных.

```python
from rest_framework import serializers
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

    def create(self, validated_data):
        # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
        # Необходимо будет из данных как-то удалить authors и создать объект, а затем заполнить authors
        # Или передавать каждый параметр без authors
        authors = validated_data["authors"]
        validated_data.pop("authors")  # Удаляем авторов из словаря
        instance = Entry(**validated_data)  # Создаём объект
        instance.save()  # Сохраняем в БД
        instance.authors.set(authors)  # Заполняем все в связи многое ко многому
        return instance
        """
        Если бы не было связей много ко многому, то можно было бы записать так вместо всех строк
        return Entry.objects.create(**validated_data)"""

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        """Или можно руками внести все поля где будут изменения (удобно, когда необходимо явно указать какие поля 
        изменяются вне зависимости от параметров поля)
        instance.headline = validated_data.get('headline', instance.headline)
        instance.body_text = validated_data.get('body_text', instance.body_text)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.mod_date = validated_data.get('mod_date', instance.mod_date)
        instance.number_of_comments = validated_data.get('number_of_comments', instance.number_of_comments)
        instance.number_of_pingbacks = validated_data.get('number_of_pingbacks', instance.number_of_pingbacks)
        instance.rating = validated_data.get('rating', instance.rating)"""
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

my_instance = Entry.objects.get(pk=data["id"])  # объявляем объект для редактирования
serializer = EntrySerializer(instance=my_instance, data=data)  # Запись для обновления строки в БД. instance передаём
# вместе с data, при сериализации id не будет участвовать (так как не определён в классовых атрибутах EntrySerializer),
# он существует в data только для более удобного создания instance.

# serializer = EntrySerializer(data=data)  # запись для создания объекта
if serializer.is_valid():
    print(repr(serializer.save()))  # <Entry: Hello World>
```

#### Валидация
У Serializer есть встроенная валидация полей по типу поля, однако, если это необходимо, то можно дописать своих валидаторов

Есть несколько подходов:

* `Валидация на уровне поля`. Вы можете задать пользовательскую валидацию на уровне полей, добавив методы 
validate_<field_name> в ваш подкласс Serializer.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value

data = {'title': 'about Django',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.validated_data)  # OrderedDict([('title', 'about Django'), ('content', '123')])

# Проверка пользовательской валидации
data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
print(serializer.validated_data)  # {}

# Пользовательская валидация применяется после стандартной валидации типов, поэтому они друг друга не перекрывают

```

Если ваше `<field_name>` объявлено в вашем сериализаторе с параметром `required=False`, то пользовательские проверки 
не будут проводиться для этого поля, если поле не включено в передаваемых данных.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value


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
```

* `Передача валидатора полю через параметр поля validators`. Отдельные поля сериализатора могут включать валидаторы, 
например, путем объявления их в экземпляре поля. Добавление валидаторов идёт через параметр `validators` который принимает
список, а значит к одному полю можно последовательно применить несколько валидаторов. На параметр `required=False` реагирует
аналогично как при валидации на уровне поля.

```python
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
```

Также для полей есть возможность передать встроенный валидатор `UniqueValidator`. Этот валидатор может быть использован для обеспечения 
ограничения `unique=True` для полей модели. Находится он в `rest_framework.validators`.
Он принимает один обязательный аргумент и необязательный аргумент `messages`:

`queryset`(обязательный) - Это набор запросов, в отношении которого должна быть обеспечена уникальность.

`message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

`lookup` - Поиск, используемый для нахождения существующего экземпляра с проверяемым значением. По умолчанию 'exact'.

```python
from rest_framework import serializers, validators
from app.models import Entry, Blog, Author
from datetime import date


class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField(validators=[
        validators.UniqueValidator(queryset=Entry.objects.all())
    ])  # headline должно быть уникальным среди всех записей Entry, можно сделать допустим фильтрацию
    # и сделать уникальным для определенное время
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)


data = {
    'blog': "1",
    'headline': 'Изучение красот Мачу-Пикчу',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'headline': [ErrorDetail(string='This field must be unique.', code='unique')]}
```

* `Валидация на уровне объекта`. Чтобы выполнить любую другую проверку, требующую доступа к нескольким полям, добавьте 
метод под названием `validate()` в ваш подкласс Serializer. Этот метод принимает единственный аргумент, который 
является словарем значений полей. При необходимости он должен вызывать сигнал `serializers.ValidationError` 
или просто возвращать проверенные значения.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate(self, attrs):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in attrs['title'].lower():
            raise serializers.ValidationError("Blog post is not about Django")
        if attrs['content'].isdigit():
            raise serializers.ValidationError("content is not digits")
        return attrs


data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
print(serializer.validated_data)  # {}
```

Если необходимо вывести все ошибки или вывести конкретные ошибки по ключу поля, то можно вывести словарь с ошибками.
Также в части полей с параметрами `required=False` - то `validate()` вызывается всегда, поэтому при передаче необходимо
проверять что поле есть в атрибутах.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    content = serializers.CharField()

    def validate(self, attrs):
        """
        Проверка того, что заголовок содержит слово Django
        """
        errors = {}

        title = attrs.get('title')
        if title and 'django' not in title.lower():
            errors['title'] = "Blog post is not about Django"
        if attrs['content'].isdigit():
            errors['content'] = "content is not digits"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')],
# 'content': [ErrorDetail(string='content is not digits', code='invalid')]}
print(serializer.validated_data)  # {}

data = {'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'content': [ErrorDetail(string='content is not digits', code='invalid')]}
```

* `Передача валидаторов через class Meta`. В Django Rest Framework (DRF) можно настроить валидаторы через `class Meta` 
внутри сериализатора, используя атрибуты `validators` и `extra_kwargs`.

1. Атрибут `validators` в `class Meta`: `validators` позволяет задать список функций-валидаторов для полей сериализатора. 
Эти валидаторы будут вызываться вместе с другими встроенными валидаторами DRF при валидации данных.

В `validators` можно передать как пользовательские, так и встроенные валидаторы. Среди встроенных валидаторов применяемым к
классам сериализатора (`class Meta`) можно передать:
  * `rest_framework.serializers.UniqueTogetherValidator` - Этот валидатор можно использовать для наложения ограничений 
unique_together на экземпляры модели. `UniqueTogetherValidator` используется для проверки уникальности комбинации 
значений нескольких полей вместе. Это полезно, когда вы хотите, чтобы комбинация значений в нескольких полях была уникальной. 
Например, вы можете использовать этот валидатор, чтобы гарантировать, что комбинация значений в полях "username" и "email" 
уникальна в вашей модели пользователей. `UniqueTogetherValidator` имеет два обязательных аргумента и один необязательный аргумент `messages`:

`queryset`(обязательный) - Это набор запросов, в отношении которого должна быть обеспечена уникальность.

`fields`(обязательный) - Список или кортеж имен полей, которые должны составлять уникальный набор. 
Они должны существовать как `поля в классе сериализатора`.

`message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

  * `rest_framework.serializers.UniqueForDateValidator`, `rest_framework.serializers.UniqueForMonthValidator`, 
`rest_framework.serializers.UniqueForYearValidator` - Эти валидаторы могут быть использованы для наложения ограничений 
`unique_for_date` , `unique_for_month` и `unique_for_year` на экземпляры модели. Они принимают следующие аргументы:

`queryset`(обязательный) - Это набор запросов, в отношении которого должна быть обеспечена уникальность.

`field`(обязательный) - Имя поля, по которому будет проверяться уникальность в заданном диапазоне дат. 
Оно должно существовать как `поле в классе сериализатора`.

`date_field`(обязательный) - Имя поля, которое будет использоваться для определения диапазона дат для ограничения уникальности. 
Оно должно существовать как `поле в классе сериализатора`.

`message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

```python
# Рассмотрим пример с применением нескольких различных валидаторов 
from rest_framework import serializers, validators
from app.models import Entry, Blog, Author
from datetime import date

def authors_validate(value):
    # В концепции class Meta будет передавать все доступные поля
    if len(value['authors']) < 2:
        raise serializers.ValidationError({'authors': "Число авторов должно быть более 1"})
    return value

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField(validators=[
        validators.UniqueValidator(queryset=Entry.objects.all())
    ])  # Валидация на уникальный headline для таблицы Entry
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

    class Meta:
        validators = [
            # Пользовательская валидация на число авторов
            authors_validate,
            # Валидация на совместное уникальное значение по полям number_of_comments и body_text таблицы Entry
            serializers.UniqueTogetherValidator(
                queryset=Entry.objects.all(),
                fields=['number_of_comments', 'body_text']
            ),
            # Валидация на уникальное значение поля rating при годе взятом из поля pub_date таблицы Entry
            serializers.UniqueForYearValidator(
                queryset=Entry.objects.all(),
                field='rating',
                date_field='pub_date'
            )
        ]

# Далее будет рассмотрено постепенное изменение входных данных, чтобы убрать ошибки
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

# Убираем ошибку неуникального headline. Допустим headline='Изучение'
data = {
    'blog': "1",
    'headline': 'Изучение',
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
print(serializer.errors)  # {'authors': [ErrorDetail(string='Число авторов должно быть более 1', code='invalid')]}

# Убираем ошибку минимального количества авторов. Допустим authors=[1,2]
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.0,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'rating': [ErrorDetail(string='This field must be unique for the "pub_date" year.', code='unique')]}

# Убираем ошибку неуникального рейтинга в году поля pub_date. Допустим rating=0.01
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.01,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'non_field_errors': [ErrorDetail(string='The fields number_of_comments, body_text must make a unique set.', code='unique')]}

# Убираем последнюю ошибку связанную с неуникальностью пары связки полей number_of_comments и body_text.
# Достаточно изменить что-то одно из полей, чтобы сделать их связку уникальной, допустим number_of_comments=3
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 3,
    'rating': 0.01,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.errors)  # {}
```
При использовании встроенных валидаторов в Django Rest Framework, каждый валидатор будет вызываться независимо, и если 
он вызывает ошибку, процесс валидации завершится, и остальные валидаторы `не будут выполнены`. 
Это обеспечивает определенную логику работы валидаторов и предотвращает лишнюю нагрузку при нахождении первой ошибки.

На практике редко требуется условие выведения всех ошибок валидаторов за раз. Но если это необходимо, то можно решить данную задачу
определением всех валидаторов в методе validate сериализатора.


```python

```



#### Немного про `read_only=True` и `write_only=True` для связанных полей

Для связанных полей есть определенные комбинации как можно использовать поля

Если используется `read_only=True`, то `queryset` не используется. Данная конструкция не позволит изменить связанные ключи
и удобна для обновления(update()) данных БД, но при создании объекта(create()) произойдёт ошибка так как нужны ключи 
создаваемых полей. Это можно поправить в APIView, ViewSet и т.д.

```python
from rest_framework import serializers
from app.models import Entry
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(read_only=True)
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
    print(repr(serializer.save()))  # Получаем ошибку django.db.utils.IntegrityError: NOT NULL constraint failed: app_entry.blog_id
```

`write_only=True` обязывает использовать десериализацию входных полей. Удобно когда обязательно нужно изменять значения.
Допустим 
```python
blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)
```

#### Работа с объекта Python не связанных с моделями БД

При работе с Serializer можно работать не только с полями БД, но и собственными
моделями(классами) не связанными с БД, если необходимо создать сериализатор для своих моделей.

Допустим пусть есть модель комментарий.

```python
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

    def __str__(self):
        return f"{self.email}, {self.content}, {self.created}"
```
Как видно это просто python класс никак не связанный с БД.

Теперь создадим для него сериализатор, повторяющий поля нашего класса

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField(default=datetime.now())

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance
```

Ранее при объявлении объекта сериализатора при инициализации передавали данные в параметр `data`.
Теперь мы можем передать объект нашего класса прямо при инициализации(с объектом БД так не работает, так как объект должен
быть итеррируемым)

Тогда общий код будет следующим:

```python
from rest_framework import serializers
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

    def __str__(self):
        return f"{self.email}, {self.content}, {self.created}"


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField(default=datetime.now())

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

comment = Comment(email='example@example.com', content='foo bar')

serializer = CommentSerializer(comment)

print(serializer.data)  # {'email': 'example@example.com', 'content': 'foo bar',
# 'created': '2023-08-01T14:13:44.554445Z'}

# Сериализация в json и десериализация аналогична примерам выше

# Аналогично и использование параметра data при инициализации

# Создание нового объекта
serializer = CommentSerializer(data={'email': '123@123.com',
                                     'content': '123'}
                               )
print(serializer.is_valid())  # True
print(serializer.save())  # 123@123.com, 123, 2023-08-01 14:26:02.352685

# Редактирование объекта
print(comment)  # объект до редактирования example@example.com, foo bar, 2023-08-01 14:26:02.352685
serializer = CommentSerializer(instance=comment,
                               data={'email': '123@123.com',
                                     'content': '123'}
                               )

print(serializer.is_valid())  # True
print(serializer.save())  # 123@123.com, 123, 2023-08-01 14:26:02.352685
print(comment)  # объект после редактирования 123@123.com, 123, 2023-08-01 14:26:02.352685
```


### ModelSerializer

`ModelSerializer` - это обычный `Serializer`, за исключением того, что:

* Набор полей по умолчанию заполняется автоматически.
* Набор валидаторов по умолчанию заполняется автоматически.
* Предусмотрены реализации по умолчанию `.create()` и `.update()`.

Процесс автоматического определения набора полей сериализатора
на основе полей модели достаточно сложно, но вы почти наверняка
не нужно копаться в реализации.

Если класс `ModelSerializer` ***не*** генерирует набор полей,
вам нужно, вы должны либо явно объявить дополнительные/отличающиеся поля на
класс сериализатора или просто используйте класс сериализатора.

`ModelSerializer` и `HyperlinkedModelSerializer` отличаются от `Serializer`, так как и них основная донастройка производится
в `class Meta`

```python
from rest_framework import serializers
from app.models import Entry

class EntryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
```

### HyperlinkedModelSerializer

Тип `ModelSerializer`, который вместо этого использует гиперссылки.
первичных ключевых отношений. 

Конкретно:
* Поле «url» включено вместо поля «id».
* Отношения с другими экземплярами представляют собой гиперссылки, а не первичные ключи.


```python
from rest_framework import serializers
from app.models import Entry

class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
```

### Настройка класса Meta у ModelSerializer и HyperlinkedModelSerializer
