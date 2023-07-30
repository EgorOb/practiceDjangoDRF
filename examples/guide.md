## Общее

Работа будет построена на составлении 


Для работы rest_framework должен быть объявлен в settings.py в INSTALLED_APPS
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```
![img.png](img.png)

Если вы собираетесь использовать доступный для просмотра API, вы, вероятно, также захотите добавить представления входа 
в систему и выхода из системы REST. Добавьте следующее в корневой urls.py файл. 

```python
urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

![img_1.png](img_1.png)

Про настройку словаря REST_FRAMEWORK (задаваемом в settings.py) можно почитать в файле `settings.md`

Общая последовательность при создании точки входа состоит из следующих частей:
* `Создание сериализатора`. Сериализаторы позволяют преобразовывать сложные данные, такие как наборы запросов и экземпляры моделей, 
в собственные типы данных Python, которые затем могут быть легко преобразованы в JSON, XML или другие типы содержимого. 
Сериализаторы также обеспечивают десериализацию, позволяя преобразовывать разобранные данные обратно в сложные типы после 
предварительной проверки входящих данных.
* `Создание представления`.
* `Создание точки подключения к API`.

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
from app.models import Blog, Author
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
    
data = {
        'blog': "1",
        'headline': 'Hello World',
        'body_text': 'This is my first blog post.',
        'pub_date': '2023-07-19T12:00:00Z',
        'authors': [1, 2, 3],
    }

serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True
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

data = {
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
if serializer.is_valid():
    print(repr(serializer.save()))  # <Entry: Hello World>
    """То что мы указали в данных 'blog': "1" не вызовет обновление данных, 
    создастся новая строка в БД. 
    Для обновления данных есть немного другая запись"""
```

То что мы указали в данных 'blog': "1" не вызовет обновление данных, создастся 
новая строка в БД. Для обновления данных есть немного другая запись.

Далее рассмотрим обновление данных

Если экземпляр сериализатора создан с существующим объектом из базы данных 
(например, `serializer = MySerializer(instance=my_instance)`), и обновляемые данные 
проходят валидацию, то DRF выполняет обновление существующего объекта в базе данных 
с использованием метода `update()` сериализатора. 

Именно наличие `instance` при инициализации сериализатора определяет будет ли 
обновление или создание нового объекта.

Допустим объявим сразу и `create` и `update`, а решение будем принимать исходя 
из наличия `id` блога в принимаемых данных.

```python
my_instance = MyModel.objects.get(pk=1)
serializer = MySerializer(instance=my_instance, data={'name': 'John', 'age': 30})
if serializer.is_valid():
    instance = serializer.save()
```




При работе с Serializer можно работать не только с полями БД, но и собственными
моделями не связанными с БД, если необходимо создать сериализатор для своих моделей








### ModelSerializer

```python
from rest_framework import serializers
from app.models import Entry

class EntryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
```

### HyperlinkedModelSerializer

```python
from rest_framework import serializers
from app.models import Entry

class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
```

### Настройка класса Meta у ModelSerializer и HyperlinkedModelSerializer
