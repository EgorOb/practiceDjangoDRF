Код представлений можно посмотреть по пути `venv\Lib\site-packages\rest_framework\views.py`

Код представлений можно посмотреть по пути `venv\Lib\site-packages\rest_framework\generics.py`

DRF предоставляет 4 различных типа представлений для работы с данными:

* `APIView`: Это базовый класс представления, который предоставляет полный контроль 
над логикой обработки запросов и формирования ответов. Вы определяете методы для 
каждого HTTP-метода (например, get, post, put, delete) и обрабатываете данные вручную.


* `GenericAPIView`: Этот класс предоставляет базовую логику для обработки различных 
операций, таких как получение списка объектов, создание объекта, обновление объекта 
и удаление объекта. Вы используете классы-миксины (например, 
ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView), чтобы определить 
конкретное поведение.


* `ViewSets`: ViewSets предоставляют более декларативный способ определения 
различных операций на объектах. Вы определяете методы, такие как 
list, create, retrieve, update, partial_update и destroy, и DRF автоматически 
маршрутизирует запросы на соответствующие методы. Возможно использование декораторов, 
чтобы настроить поведение.


* `ModelViewSet`: Это расширение ViewSets, которое автоматически предоставляет 
стандартные операции CRUD (create, retrieve, update, destroy) для модели. 
Он связывает представления с конкретной моделью, позволяя обрабатывать запросы 
с минимальным кодом.

## 1. APIView

APIView представляет собой низкоуровневую абстракцию которую удобно использовать 
когда:

* Нужно полное управление над обработкой запросов и ответов.
* Хотите более гибко настраивать логику для конкретных HTTP-методов.
* Логика обработки запросов сложнее стандартных CRUD-операций.

### 1.1 get, post, put, delete

Простейшее представление выглядит следующим образом. Аналогично по описанию с
представлением Django

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class MyView(APIView):
    def get(self, request):
        data = {'message': 'Hello from MyView!'}
        return Response(data)
```
 Для полноценной проверки нужно будет зарегистрировать url, запустить сервер и проверить. 
 Однако можно пойти другим путём и провести проверку без запуска сервера и регистрации,
правда данным путём не получится проверить все тонкости если это касается специфики вашего API.

Для проверки воспользуемся `APIRequestFactory` из `rest_framework.test` он аналогичен
`RequestFactory` из `django.test`, только оптимизирован для работы с объектами DRF.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory


class MyView(APIView):
    def get(self, request):
        data = {'message': 'Hello from MyView!'}
        return Response(data)


# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

# Создаем объект get запроса
request = factory.get('/my-view/')

# Вызываем представление и получаем ответ
response = view(request)

# Проверяем результат
print(response.data)  # {'message': 'Hello from MyView!'}
```
Аналогично можно создать запросы для post, put, delete

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP

class MyView(APIView):
    def get(self, request):
        data = {'message': 'Hello, World!'}
        return Response(data)

    def post(self, request):
        data = {'message': 'POST request received'}
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request):
        data = {'message': 'PUT request received'}
        return Response(data)

    def delete(self, request):
        data = {'message': 'DELETE request received'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

# Создаем объект get запроса
request = factory.get('/my-view/')
response = view(request)
print(response.data)  # {'message': 'Hello from MyView!'}

# Создаем объект post запроса
request = factory.post('/my-view/')
response = view(request)
print(response.data)  # {'message': 'POST request received'}

# Создаем объект put запроса
request = factory.put('/my-view/')
response = view(request)
print(response.data)  # {'message': 'PUT request received'}

# Создаем объект delete запроса
request = factory.delete('/my-view/')
response = view(request)
print(response.data)  # {'message': 'DELETE request received'}
```

При чистой работе с APIView нет встроенного механизма для работы с сериализаторами, поэтому
работу с сериализаторами необходимо прописывать самостоятельно. Сериализатор можно использовать
любой что был написан ранее хоть с использованием Serializer или ModelSerializer и т.д.

Для примера рассмотрим пример использования сериализатора API, позволяющего 
получить все записи блогов на базе Serializer 

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    # Получение всех записей, или если был передан ключ с записью, то вывод
    # только одной записи
    def get(self, request):
        if request.GET.get('pk'):
            instance = Entry.objects.get(pk=request.GET.get('pk'))
            serializer = EntrySerializer(instance)
        else:
            queryset = Entry.objects.all()  # Получаем все объекты модели
            serializer = EntrySerializer(queryset,
                                         many=True)  # Множество объектов для сериализации

        return Response(serializer.data)

    # Создание новой записи
    def post(self, request):
        serializer = EntrySerializer(data=request.data)  # Используем сериализатор для обработки данных
        if serializer.is_valid():
            # Если данные валидны, сохраняем их или выполняем необходимые действия
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Обновление записи(чтобы обновлять, нужно знать где обновить, поэтому
    # в этот раз передадим значения в заголовке, а не параметрах запроса)
    def put(self, request):
        try:
            instance = Entry.objects.get(pk=request.data.get('id'))  # Получаем существующий объект
        except Entry.DoesNotExist:
            return Response({'message': 'Object not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = EntrySerializer(instance,
                                     data=request.data)  # Используем сериализатор для обновления данных
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    # Удаление записи
    def delete(self, request):
        try:
            instance = Entry.objects.get(pk=request.data.get('id'))  # Получаем существующий объект
        except Entry.DoesNotExist:
            return Response({'message': 'Object not found'},
                            status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'message': f"Object id={request.data.get('id')} deleted"},
                        status=status.HTTP_204_NO_CONTENT)


# Данные для работы
data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

# Создаем объект get запроса (получение информации по ключу 1,
# как пример передаётся прямо в параметрах запроса)
request = factory.get('/my-view/?pk=1')  # Можно было бы написать маршрут
# /my-view/1 (что было бы по принципу rest), но request самостоятельно
# не парсит адрес, как это делает сам Django (в случае регистрации данного маршрута 
# допустим как path('/my-view/<pk:int>', ...), тогда бы в get вашего обработчика 
# можно было передать pk как входной параметр)
response = view(request)
print(response.data)  # {
# 'blog': 1,
# 'headline': 'Изучение красот Мачу-Пикчу',
# 'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд...',
# 'pub_date': '2022-04-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'authors': [1, 9], 'number_of_comments': 2,
# 'number_of_pingbacks': 10, 'rating': 0.0
# }

# Создаем объект get запроса (получение всей информации)
request = factory.get('/my-view/')
response = view(request)
print(response.data)  # [
# OrderedDict([
# ('blog', 1),
# ('headline', 'Изучение красот Мачу-Пикчу'),
# ('body_text', 'Древний город Мачу-Пикчу, скрытый ... наследии.'),
# ('pub_date', '2022-04-01T21:00:00Z'),
# ('mod_date', '2023-07-17'),
# ('authors', [1, 9]),
# ('number_of_comments', 2),
# ('number_of_pingbacks', 10),
# ('rating', 0.0)]),
# OrderedDict(...),
# ...]

# Создаем объект post запроса (добавление данных)
request = factory.post('/my-view/', data=data)
response = view(request)
print(response.data)  # {'blog': 1, 'headline': 'Hello World',
# 'body_text': 'This is my first blog post.',
# 'pub_date': '2023-07-19T12:00:00Z',
# 'mod_date': '2023-08-18', 'authors': [1, 2, 3],
# 'number_of_comments': 0, 'number_of_pingbacks': 0, 'rating': 0.0}
print(Entry.objects.latest('id'))  # <Entry: Hello World>

# Создаем объект put запроса (обновление данных)
request = factory.put('/my-view/', data=data)
response = view(request)
print(response.data)  # {'blog': 1, 'headline': 'Hello World', 'body_text': 'This is my first blog post.',
# 'pub_date': '2023-07-19T12:00:00Z', 'mod_date': '2023-08-22', 'authors': [1, 2, 3],
# 'number_of_comments': 0, 'number_of_pingbacks': 0, 'rating': 0.0}

# Создаем объект delete запроса
request = factory.delete('/my-view/', data={'id': 26})
print(Entry.objects.latest('id').id)  # 26
response = view(request)
print(response.data)  # {'message': 'Object id=26 deleted'}
print(Entry.objects.latest('id').id)  # 25
```
### 1.2 Переопределение классовых атрибутов

Класс APIView наследуется от View класса представления Django(на картинке 
представлена часть исходного кода)

![img_4.png](img_4.png)

Внутри обладает классовыми атрибутами, которые ранее описывались в `settings.md`,
соответственно для каждого представления можно переопределить ряд настроек или
по умолчанию они будут загружаться из словаря `REST_FRAMEWORK` (задаваемом в `settings.py`):

* `renderer_classes` = api_settings.DEFAULT_RENDERER_CLASSES. 
Определяет классы рендеринга (отображения) контента


* `parser_classes` = api_settings.DEFAULT_PARSER_CLASSES. 
Определяет классы парсера, используемые для разбора входящего запроса.


* `authentication_classes` = api_settings.DEFAULT_AUTHENTICATION_CLASSES. 
Определяет классы аутентификации, используемые для проверки подлинности пользователя.


* `throttle_classes` = api_settings.DEFAULT_THROTTLE_CLASSES.
Определяет классы ограничения скорости (throttle), которые контролируют частоту 
запросов от клиентов


* `permission_classes` = api_settings.DEFAULT_PERMISSION_CLASSES.
Определяет классы разрешений, используемые для определения доступа к ресурсам API.


* `content_negotiation_class` = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS.
Определяет класс для выбора контента на основе заголовков запроса.


* `metadata_class` = api_settings.DEFAULT_METADATA_CLASS. 
Определяет класс метаданных, используемый для генерации метаданных API.


* `versioning_class` = api_settings.DEFAULT_VERSIONING_CLASS.
Определяет класс версионирования, используемый для управления версиями API.

Рассмотрим ниже часть данных атрибутов на урезанной версии `class MyView(APIView)`

Чаще других используют `permission_classes`, `authentication_classes`, `throttle_classes`

#### 1.2.1 Разрешения доступа (permission_classes) и базовая аутентификация (authentication_classes)
По умолчанию API может пользоваться любой пользователь, но если необходимо как-то ограничить круг влияния к конкретному
обработчику API, то можно в `permission_classes` прописать кто именно может получить доступ к этой части API. По умолчанию  
`['rest_framework.permissions.AllowAny']`, а так можно передать туда тоже самое, что можно задать в `settings.py`
словаря `REST_FRAMEWORK` по ключу `DEFAULT_PERMISSION_CLASSES`

##### 1.2.1.1 permissions.IsAuthenticated
Рассмотрим условие, что к нашему API может получить доступ только авторизированный пользователь. Тогда в `permission_classes`
пропишем `[rest_framework.permissions.IsAuthenticated]`. Сериализатор `EntrySerializer` возьмём из ранее рассмотреных задач

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = Entry.objects.all()  # Получаем все объекты модели
        serializer = EntrySerializer(queryset,
                                     many=True)  # Множество объектов для сериализации

        return Response(serializer.data)

# Данные для работы
data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

# Создаем объект get запроса (получение всей информации)
request = factory.get('/my-view/')
# По умолчанию создаётся анонимный(не авторизированный) пользователь
response = view(request)
# После прохода запроса через промежуточное ПО в Django - request приобрёл новые атрибуты включая user
# позволяющий идентифицировать пользователя
print(request.user.is_authenticated)  # False
# В данном случае создаётся сообщение о неавторизированном доступе
print(response.data)  # {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}

# У APIView есть атрубут authentication_classes по умолчанию в котором прописано как будет проходить
# авторизация пользователя по умолчанию это SessionAuthentication - авторизация по сессии(cookies);
# BasicAuthentication - авторизация по логину, паролю или любому другой связке, которую поддерживает ваше приложение

# Чтобы авторизировать пользователя, то передадим в factory.get параметры доступа в META['HTTP_AUTHORIZATION']
login = 'admin'
password = '123'
credentials = f'{login}:{password}'
# Создаем объект запроса с заголовком Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f"Basic {credentials}"
# Пароль в заголовке HTTP отправляется в открытом виде
print(request.META['HTTP_AUTHORIZATION'])  # Basic admin:123

# Вызываем представление и получаем ответ
response = view(request)

"""
Проверяем результат, получаем ошибку, что логин и пароль не найдены.
Это связано с промежуточным ПО, которое хочет обезопасить данные
и не хочет их принимать в открытом виде
"""
print(response.status_code)  # 403
print(response.data)  # {'detail': ErrorDetail(string='Invalid username/password.', code='authentication_failed')}
"""
Middleware аутентификации Django ожидает, что параметры для базовой аутентификации будут закодированы в формате Base64. 
Это стандартный способ передачи логина и пароля в заголовке Authorization при использовании Basic Authentication.
Таким образом, при использовании Basic Authentication, логин и пароль следует закодировать в формат Base64 и 
передать их в заголовке Authorization.
"""

import base64
# Кодируем логин и пароль в виде строковой комбинации
credentials = base64.b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')

# Создаем объект запроса с заголовком Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f'Basic {credentials}'
# Пароль в заголовке HTTP отправляется в закодированном виде
print(request.META['HTTP_AUTHORIZATION'])  # Basic YWRtaW46MTIz

# Вызываем представление и получаем ответ
response = view(request)

# Проверяем результат
print(response.status_code)  # 200
print(response.data)  # Выводит все записи
"""
Логин и пароль в открытом виде передавать не рекомендуется, так как это не безопасно. 
Basic Authentication предполагает передачу учетных данных в закодированной форме для повышения безопасности.
"""
```

Если вы используете протокол HTTPS для обмена данными между клиентом и сервером, то ваши данные уже защищены с 
использованием шифрования, их не видно посредникам (man-in-the-middle) и они безопасно передаются по сети. В этом случае 
базовая аутентификация, как правило, не требуется для обеспечения безопасности передачи логина и пароля.

В протоколе HTTPS данные между клиентом и сервером шифруются на уровне транспортного слоя, что обеспечивает 
конфиденциальность данных. Поэтому, если вы используете HTTPS, данные, включая логины и пароли, будут зашифрованы и 
надежно передаваться по сети.

В этом контексте использование кодирования Base64, как при базовой аутентификации, не добавляет дополнительной безопасности 
в обмене данными, так как данные уже защищены шифрованием HTTPS. Вместо этого, кодирование Base64 представляет собой 
стандартную практику для передачи логина и пароля в формате, понимаемом сервером, но оно не обеспечивает дополнительную 
безопасность в сети.

Важно подчеркнуть, что при использовании базовой аутентификации, логин и пароль все равно будут передаваться внутри запроса, 
и поэтому важно обеспечить надежное хранение и обработку паролей на сервере. 

На практике стоит рассмотреть более безопасные методы аутентификации, 
такие как токены или JWT, которые не требуют передачи паролей в открытом виде. Что и будет рассмотрено позже.

##### 1.2.1.2 permissions.IsAuthenticatedOrReadOnly

Если необходимо разрешить обработку запросов от авторизированных пользователей, а от неавторизированных принимать только
безопасные запросы (на чтение), то можно воспользоваться `IsAuthenticatedOrReadOnly`.

`IsAuthenticatedOrReadOnly` разрешает все запросы на чтение (GET, HEAD, OPTIONS) и разрешает запросы на запись только 
аутентифицированным пользователям.

На примере ниже будем использовать обработчик для get и post запросов:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        queryset = Entry.objects.all()  # Получаем все объекты модели
        serializer = EntrySerializer(queryset,
                                     many=True)  # Множество объектов для сериализации

        return Response(serializer.data)

    # Создание новой записи
    def post(self, request):
        serializer = EntrySerializer(data=request.data)  # Используем сериализатор для обработки данных
        if serializer.is_valid():
            # Если данные валидны, сохраняем их или выполняем необходимые действия
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import base64
login = 'admin'
password = '123'

# Данные для работы
data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

"""
Проверяем, что для авторизированного пользователя работает get и post запросы
"""
# Кодируем логин и пароль в виде строковой комбинации
credentials = base64.b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')

# Создаем объект запроса с заголовком Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f'Basic {credentials}'
print(request.META['HTTP_AUTHORIZATION'])  # Basic YWRtaW46MTIz
# Вызываем представление и получаем ответ
response = view(request)
# Проверка, что пользователь авторизирован
print(request.user.is_authenticated)  # True
# Проверяем результат
print(response.status_code)  # 200
print(response.data)  # Выводит все записи

# Создаем объект post запроса (добавление данных)
request = factory.post('/my-view/', data=data)
request.META['HTTP_AUTHORIZATION'] = f'Basic {credentials}'

print(Entry.objects.latest('id').id)  # 25
response = view(request)
print(response.status_code)  # 201
print(response.data)  # {'blog': 1, 'headline': 'Hello World',
# 'body_text': 'This is my first blog post.',
# 'pub_date': '2023-07-19T12:00:00Z',
# 'mod_date': '2023-08-18', 'authors': [1, 2, 3],
# 'number_of_comments': 0, 'number_of_pingbacks': 0, 'rating': 0.0}
print(Entry.objects.latest('id').id)  # 26

"""
Проверяем, что для неавторизированного пользователя работает только get, post не работает
"""
request = factory.get('/my-view/')
# Вызываем представление и получаем ответ
response = view(request)
# Проверка, что пользователь неавторизирован
print(request.user.is_authenticated)  # False
# Проверяем результат
print(response.status_code)  # 200
print(response.data)  # Выводит все записи

# Создаем объект post запроса (добавление данных)
request = factory.post('/my-view/', data=data)
response = view(request)
print(response.status_code)  # 403
print(response.data)  # {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}
```

##### 1.2.1.3 Создание своего разрешения
Так же есть возможность проверять, что пользователь администратор и давать доступ к определенной части API
путем задания `IsAdminUser` у `permission_classes`, а также получение прав доступа из моделей БД (`DjangoModelPermissions`,
`DjangoModelPermissionsOrAnonReadOnly`, `DjangoObjectPermissions`), однако такое удобнее при 

Но, допустим, вы хотите дать отдельное разрешение администраторам, у которых есть атрибут `is_staff` или выделить
любую другую группу пользователей, то вы можете создать свое собственное пользовательское разрешение в DRF. 

Для этого создаём разрешение, допустим как на базе `IsAuthenticatedOrReadOnly` - для чтения разрешено всем,
для изменения только авторизированным пользователям и с флагом `is_staff`

```python
from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешение для GET, HEAD и OPTIONS всегда разрешено
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверьте, является ли пользователь аутентифицированным и имеет ли он атрибут is_staff
        return request.user.is_authenticated and request.user.is_staff
```
Ну а далее всё по известной схеме

Вот полный пример, только к списку разрешений добавлен ещё и админ(`IsAdminUser`):

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP
from rest_framework.permissions import IsAdminUser, BasePermission, SAFE_METHODS

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Разрешение для GET, HEAD и OPTIONS всегда разрешено
        if request.method in SAFE_METHODS:
            return True

        # Проверьте, является ли пользователь аутентифицированным и имеет ли он атрибут is_staff
        return request.user.is_authenticated and request.user.is_staff


class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    permission_classes = [IsStaffOrReadOnly, IsAdminUser]
    def get(self, request):
        queryset = Entry.objects.all()  # Получаем все объекты модели
        serializer = EntrySerializer(queryset,
                                     many=True)  # Множество объектов для сериализации

        return Response(serializer.data)

    # Создание новой записи
    def post(self, request):
        serializer = EntrySerializer(data=request.data)  # Используем сериализатор для обработки данных
        if serializer.is_valid():
            # Если данные валидны, сохраняем их или выполняем необходимые действия
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import base64

# Данные для работы
data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

"""
Проверяем обработку post запроса для админа
"""
login = 'admin'
password = '123'
# Кодируем логин и пароль в виде строковой комбинации
credentials = base64.b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')

# Создаем объект запроса с заголовком Authorization
request = factory.post('/my-view/', data=data)
request.META['HTTP_AUTHORIZATION'] = f'Basic {credentials}'
# Вызываем представление и получаем ответ
response = view(request)
# Проверка, что пользователь админ c атрибутом is_staff
print(request.user.is_superuser)  # True
print(request.user.is_staff)  # True
# Проверяем результат
print(response.status_code)  # 201
print(response.data)  # Выводит запись которую добавил

"""
Проверяем обработку post запроса для администратора(is_staff)
"""
login = 'staff'
password = '!QAZXSW@'
# Кодируем логин и пароль в виде строковой комбинации
credentials = base64.b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')

# Создаем объект запроса с заголовком Authorization
request = factory.post('/my-view/', data=data)
request.META['HTTP_AUTHORIZATION'] = f'Basic {credentials}'
# Вызываем представление и получаем ответ
response = view(request)
# Проверка, что пользователь админ c атрибутом is_staff
print(request.user.is_superuser)  # False
print(request.user.is_staff)  # True
# Проверяем результат
print(response.status_code)  # 201
print(response.data)  # Выводит запись которую добавил

"""
Проверяем обработку post запроса для неавторизированного (анонимного) пользователя
"""
request = factory.post('/my-view/', data=data)
# Вызываем представление и получаем ответ
response = view(request)
# Проверка, что пользователь неавторизирован
print(request.user.is_authenticated)  # False
# Проверяем результат
print(response.status_code)  # 403
print(response.data)  # {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}
```

#### 1.2.2 Другие виды встроенной аутентификации (authentication_classes)

##### 1.2.1.1 Аутентификация по сессии

##### 1.2.1.2 Аутентификация по токенам
Помимо базовой аутентификации и аутентификации по сессии, среди доступных методое в DRF есть аутентификация 
по токенам. Для этого в `authentication_classes` к списку добавим или заменим на `authentication.TokenAuthentication`

`TokenAuthentication` - это один из методов аутентификации в DRF, который позволяет аутентифицировать пользователей с 
использованием токенов. Токены предоставляются аутентифицированным пользователям и должны быть включены в заголовок запроса 
для аутентификации.

Для полноценной работы с токенами необходимо будет произвести ряд действий (так как будет создаваться таблица для 
хранения токенов в БД)

Добавьте `'rest_framework.authtoken'` в `INSTALLED_APPS` в файле `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    # ...
]
```

Запустите миграцию и создание таблиц в БД
```python
python manage.py makemigrations
python manage.py migrate
```

В примере будем работать с только с токенами и разрешением на авторизированных пользователей

Передача токена идёт в том же заголовке `HTTP_AUTHORIZATION` что и при `BasicAuthentication`

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        queryset = Entry.objects.all()  # Получаем все объекты модели
        serializer = EntrySerializer(queryset,
                                     many=True)  # Множество объектов для сериализации

        return Response(serializer.data)

import base64

# Создаем объект RequestFactory
factory = APIRequestFactory()

# Создаем экземпляр представления
view = MyView.as_view()

"""
Проверяем обработку get запроса для авторизированного пользователя, но при BasicAuthentication
"""
login = 'admin'
password = '123'
# Кодируем логин и пароль в виде строковой комбинации
credentials = base64.b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')

# Создаем объект запроса с заголовком Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f'Basic {credentials}'
# Вызываем представление и получаем ответ
response = view(request)
# Проверяем результат
print(response.status_code)  # 401
# Возникнет сообщение "Учетные данные для аутентификации не были предоставлены"
print(response.data)  # {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}

"""
Проверяем обработку get запроса для авторизированного пользователя по токену
"""
# Обычно происходит следующее: пользователь регистрируется, ему выдаётся токен доступа, который он использует для
# доступа к API. При работе с сессиями происходит аналогично, выдаётся токен, записывается в сессию или куки, и уже
# по этому токену происходит аутентификация.

# Для начала токен нужно получить, это чем-то похоже на кодирование при base64, только используем тотже токенизатор,
# что DRF будет использовать при аутентификации.

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Token от rest_framework работает с объектами модели
user = User.objects.get(username=login)
# Получение токена по объекту модели
token, created = Token.objects.get_or_create(user=user)  # token: '2fe34544ba2bb4d401b9df1efccdb145e168a5b7'

# Создаем объект запроса с заголовком Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f'Token {token.key}'
print(request.META['HTTP_AUTHORIZATION'])  # Token 2fe34544ba2bb4d401b9df1efccdb145e168a5b7
# Вызываем представление и получаем ответ
response = view(request)
# Проверяем результат
print(response.status_code)  # 200
print(response.data)  # Выводит все записи

# Если токен не совпадет с тем, что есть в БД, то аутентификация будет неверной

request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f'Token {token.key}aaa'
print(request.META['HTTP_AUTHORIZATION'])  # Token 2fe34544ba2bb4d401b9df1efccdb145e168a5b7aaa
# Вызываем представление и получаем ответ
response = view(request)
# Проверяем результат
print(response.status_code)  # 401
print(response.data)  # {'detail': ErrorDetail(string='Invalid token.', code='authentication_failed')}
```

##### 1.2.1.3 Аутентификация с использованием внешних систем (RemoteUserAuthentication)
`RemoteUserAuthentication` - это класс аутентификации в DRF, который позволяет аутентифицировать пользователей на основе
переменной окружения REMOTE_USER, которая часто используется при интеграции с внешними системами, такими как серверы 
авторизации, аутентификации через одиночную сессию (Single Sign-On, SSO) и т. д.

Этот класс аутентификации полезен, когда ваше приложение настроено для аутентификации через другой сервер или сервис, и 
ваше приложение получает имя пользователя из переменной окружения REMOTE_USER, предоставляемой веб-сервером или другой 
аутентификационной системой. Вместо того чтобы требовать от пользователей вводить логин и пароль, DRF может использовать 
REMOTE_USER для аутентификации пользователей автоматически. Это удобно в тех случаях, когда вы хотите интегрировать Django 
и DRF с существующей системой аутентификации, которая управляет пользователями и их аутентификацией. 
Вместо того чтобы хранить логины и пароли в вашей базе данных, вы полагаетесь на аутентификацию, предоставляемую вашим сервером.

Когда `RemoteUserAuthentication` используется в DRF, он следует этим шагам:

1. Веб-сервер (или аутентификационная система) аутентифицирует пользователя и устанавливает REMOTE_USER.

2. DRF получает REMOTE_USER из переменной окружения и аутентифицирует пользователя с этим именем.

3. Если пользователь существует, он получает доступ к ресурсам, в противном случае ему отказан доступ.

Для использования `RemoteUserAuthentication`, вы должны настроить свой веб-сервер (например, Apache или Nginx) для 
аутентификации пользователей и передачи REMOTE_USER в ваше приложение Django. Также убедитесь, что ваши настройки 
Django `MIDDLEWARE` включают `'django.contrib.auth.middleware.RemoteUserMiddleware'`(по умолчанию не прописано).

Важно отметить, что работа с аутентификацией через REMOTE_USER требует аккуратности в настройке и обеспечении 
безопасности вашего сервера и приложения.

Для того, чтобы работала аутентификация, то необходимо прописать бэкенд аутентификации, так как это нестандартный бэкенд.
Всё прописывается в `settings.py` в переменной `AUTHENTICATION_BACKENDS` (по умолчанию её скорее всего не будет)
в неё допишем `'django.contrib.auth.backends.RemoteUserBackend'`, но чтобы прошлая базовая аутентификация работала, то пропишем

```python
AUTHENTICATION_BACKENDS= [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]
```

`django.contrib.auth.backends.RemoteUserBackend` - это аутентификационный бэкенд в Django, который используется для 
аутентификации пользователей на основе значения REMOTE_USER из переменной окружения или HTTP заголовка.

Ранее писалось, что необходимо в `MIDDLEWARE` включить `'django.contrib.auth.middleware.RemoteUserMiddleware'`. Его стоит
включить, в случае если сервер будет создавать переменную окружения.

`django.contrib.auth.middleware.RemoteUserMiddleware` - это middleware в Django, который играет важную роль в обработке 
переменной окружения `REMOTE_USER`, передаваемой в вашем приложении из внешней системы аутентификации или веб-сервера.

Если необходимо добавить `RemoteUserMiddleware`, то вот пример
```python
MIDDLEWARE = [
    ...,
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    ...,
]
```

Если Django берет значение `REMOTE_USER` из заголовка `request.META['REMOTE_USER']`, а не из переменных окружения, 
это может быть обусловлено конфигурацией вашего веб-сервера или прокси-сервера.

Приведем небольшой пример, с тестированием на локальной машине, вместо отдельного сервера. В заголовке `REMOTE_USER` передаём
username пользователя, так как особенностью `RemoteUserBackend` является то, что он не выполняет проверку пароля. 
Вместо этого он полагается на то, что пользователь уже был аутентифицирован на более высоком уровне 
(например, на уровне веб-сервера или системы одиночной сессии) и что значение `REMOTE_USER` является достоверным.

```python
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import RemoteUserAuthentication

# Создаем представление, использующее RemoteUserAuthentication
class MyView(APIView):
    authentication_classes = [RemoteUserAuthentication]

    def get(self, request):
        return Response({'username': request.user.username})

# Создаем фабрику запросов
factory = APIRequestFactory()
# Устанавливаем переменную окружения REMOTE_USER в объекте request.META
request = factory.get('/my-view/')
request.META['REMOTE_USER'] = 'my_user'  # Здесь устанавливаем имя пользователя
# Создаем представление и передаем в него запрос
view = MyView.as_view()
response = view(request)

# Выводим ответ даже если такого пользователя нет, так как это обусловлено подходом RemoteUserAuthentication. Однако если
# такого пользователя нет, то механиз может его создать. Так что нужно следить за этим.
print(response.data)  # {'username': 'my_user'}
```

##### 1.2.1.4 Создание своей аутентификации

#### 1.2.3 Аутентификация с применением сторонних пакетов (современные подходы)

##### 1.2.3.1 Работа с JSON Web Tokens(JWT)

`JSON Web Token(JWT)` - это компактный и самодостаточный способ представления информации между двумя сторонами в форме 
объекта в JSON-формате. JWT используется для передачи данных между клиентом и сервером в виде токена. Он может 
использоваться для аутентификации и обмена данными в безопасном формате.

###### Теоритическая часть
JWT состоит из трех частей, разделенных точками:

1. Заголовок (Header): Заголовок содержит информацию о типе токена (JWT) и алгоритме подписи, используемом для создания 
и проверки подписи. Пример заголовка:

```python
{
  "alg": "HS256",
  "typ": "JWT"
}
```
2. Полезная нагрузка (Payload): Полезная нагрузка содержит данные (claims), которые хранятся в токене. В JWT есть три типа claims:

   * `Registered claims`: Эти claims являются стандартными и включают, например, iss (issuer), exp (expiration time), 
sub (subject), и другие.
   * `Public claims`: Эти claims определяются пользователем и/или приложением и могут использоваться для обмена 
дополнительной информацией.
   * `Private claims`: Эти claims также определяются пользователем, но они предназначены для обмена между сторонами, 
которые заранее договорились о их значении.

Пример полезной нагрузки:
```python
{
  "sub": "1234567890",
  "name": "John Doe",
  "exp": 1516239022
}
```
3. Подпись (Signature): Подпись создается путем кодирования заголовка, полезной нагрузки и секретного ключа алгоритмом, 
указанным в заголовке. Это делает JWT самодостаточным, так как сторона, получившая токен, может проверить его подлинность, 
раскодировав токен и проверив подпись.

Процесс работы JWT:

1. Пользователь входит в систему и аутентифицируется на сервере, который генерирует JWT.
2. Сервер включает в токен информацию о пользователе и другие данные, которые ему необходимы.
3. JWT отправляется обратно клиенту, который может хранить его (например, в куках или localStorage) и включать в заголовки 
запросов к серверу.
4. При каждом запросе на сервер клиент включает токен в заголовок запроса.
5. Сервер проверяет подпись токена, раскодирует полезную нагрузку и использует информацию для аутентификации пользователя 
и принятия решения о предоставлении доступа к запрошенным ресурсам.

JWT позволяет создавать безсостоятельные, расширяемые и безопасные токены, которые могут использоваться в различных контекстах, 
таких как аутентификация в API, одиночная сессия (Single Sign-On), обмен данными между сервисами и многое другое.

###### djangorestframework-simplejwt

Работу с токенами будем делать с помощью сторонней библиотеки `djangorestframework-simplejwt` (уже есть в requirements.txt)
Ссылка на данный пакет есть в [официальной документации restframework](https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication) 

[Документация djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

JWT тоже токены, но отличаются от подхода описанного в `TokenAuthentication`

`djangorestframework-simplejwt` и `rest_framework.authtoken` - это два разных способа аутентификации и авторизации в DRF
с использованием токенов. Они имеют несколько существенных различий:

1. Механизм аутентификации:

   * `rest_framework.authtoken` использует механизм аутентификации на основе токенов, где каждый пользователь имеет свой 
уникальный токен, который используется для аутентификации в API. Эти токены создаются и управляются на стороне сервера.

   * `djangorestframework-simplejwt` использует JWT для аутентификации. JWT - это стандартный формат токенов, который 
содержит информацию о пользователе и может быть подписан цифровой подписью. В отличие от `rest_framework.authtoken`, 
пользовательские данные хранятся внутри самого токена, и сервер не обязан хранить и управлять отдельными токенами.

 2. Хранение данных пользователя:

    * В случае `rest_framework.authtoken`, данные пользователя (например, его идентификатор) хранятся на стороне сервера, 
 и токены служат как ссылки на эти учетные записи пользователя.

    * В `djangorestframework-simplejwt`, информация о пользователе хранится внутри самого токена, и серверу не требуется 
 для проверки подлинности пользователя. Это делает JWT более масштабируемым в средах, где у вас может быть множество 
 серверов, так как он не требует обращения к серверу для проверки токена.

 3. Сложность и настройка:

    * `rest_framework.authtoken` более прост в настройке и использовании. Он предоставляет готовые представления и 
 аутентификационные классы для использования в DRF.

    * `djangorestframework-simplejwt` требует немного больше настройки, но предоставляет более гибкую и расширяемую систему 
 аутентификации с поддержкой JWT, включая возможность настройки срока действия и обновления токенов.

 4. Срок действия токена:
     Оба метода могут поддерживать срок действия токена, но в `djangorestframework-simplejwt` это реализовано более гибко 
и позволяет устанавливать срок действия как для доступа, так и для обновления токена.

 5. Производительность и безопасность:
     JWT более безопасен в том смысле, что информация в токене зашифрована и подписана, что обеспечивает целостность данных 
и защиту от подделки. Однако это также может сделать JWT более сложным для управления, если требуется много дополнительной информации о пользователе.

Выбор между `rest_framework.authtoken` и `djangorestframework-simplejwt` зависит от ваших требований и предпочтений. 
Если вам нужна быстрая и простая аутентификация с токенами, `rest_framework.authtoken` может быть хорошим выбором. 
Если вам нужна более гибкая и безопасная аутентификация с JWT, то `djangorestframework-simplejwt` может быть более подходящим вариантом.

###### Практическая часть
В примере будем использовать JWT только для нашего обработчика, но помним, что если хотим применить JWT для всех обработчиков,
то просто укажем его в REST_FRAMEWORK в DEFAULT_AUTHENTICATION_CLASSES, как пример:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # Другие классы аутентификации, если есть
    ),
}
```

Регистрация в `INSTALLED_APPS` в `settings.py`

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',
    # ...
]
```

Далее необходимо получить токен и с ним сформировать запрос на получение нужной информации.
Поможет получить токен обработчик `TokenObtainPairView` у `rest_framework_simplejwt.views`

Код будет следующим(используем известный ранее сериализатор и представление):

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework import status  # Импортируем статусы HTTP
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date


class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        queryset = Entry.objects.all()  # Получаем все объекты модели
        serializer = EntrySerializer(queryset,
                                     many=True)  # Множество объектов для сериализации

        return Response(serializer.data)


# Создаем объект RequestFactory
factory = APIRequestFactory()

user_data = {
    "username": "admin",
    "password": "123"
}

from rest_framework_simplejwt.views import TokenObtainPairView
# Обработчик JWT для получения токена
token_view = TokenObtainPairView.as_view()
# Передаём запрос на получение токена для пользователя
request = factory.post('/token/', user_data, format='json')
response = token_view(request)
token_data = response.data
# Токен доступа
access_token = token_data.get("access")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyOTczNTkzLCJpYXQiOjE2OTI5NzMyOTMsImp0aSI6IjViNWRhZDA0Yjg0ODQxOTRiODdiOGFhM2EyN2E0MTI5IiwidXNlcl9pZCI6MX0.8Ea7HDi5IyZqiQxwXjo6u50MZQW5rnoKO0xRPc-ifNc'

# Создаем экземпляр представления
view = MyView.as_view()

# Создаем запрос и установливаем заголовок Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"

# Отправляем запрос с заголовком Authorization
response = view(request)
# Проверяем результат
print(response.status_code)  # 200
print(response.data)  # Выводит все записи
```

###### Проверка на запущенном сервере
Также дополнительно к `APIRequestFactory` можно воспользоваться `APIClient`.

`APIRequestFactory` предназначен для создания фабрики объектов `Request`, которые могут быть использованы для имитации 
HTTP-запросов к вашему API во время модульного тестирования. Этот инструмент создает объекты Request, но не выполняет 
фактические HTTP-запросы к вашему серверу. Он работает на более низком уровне и создает объекты Request, которые затем 
можно передать в представления API для тестирования и проверки ответов. `APIRequestFactory` удобен для тестирования 
отдельных представлений и их поведения **без необходимости запускать полноценный сервер**.

`APIClient` предоставляет более высокоуровневый интерфейс для тестирования API. Он выполняет фактические HTTP-запросы 
к вашему серверу и обрабатывает ответы. `APIClient` позволяет создавать запросы, **отправлять их на сервер** и получать ответы. 
Это полезно для интеграционного тестирования, когда вам нужно проверить взаимодействие между разными частями вашего API 
и его работу в целом. `APIClient` может автоматически обрабатывать аутентификацию (например, использование токенов или 
сессий) и управлять cookie и сеансами, что полезно для тестирования более сложных сценариев.

В итоге с `APIClient` можно проверить полноценное прохождение запроса, но для этого должны быть рабочие маршруты(
что не нужно для `APIRequestFactory`) и нужен запущенный сервер(что не нужно для `APIRequestFactory`).

Настроим URL-ы: Создайте URL-ы для представлений `TokenObtainPairView`, `TokenRefreshView` и, при необходимости, 
`TokenVerifyView`. Эти представления предоставляют возможность создавать, обновлять и проверять токены JWT.

Допустим для примера приведу код для корневого urls.py в папке project добавим маршруты `'token/'`, `'token/refresh/'`, 
`'token/verify/'`

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Проверка токена
]
```

Чтобы всё работало необходимо в `ALLOWED_HOSTS` в `settings.py` дописать `'testserver'`
```python
ALLOWED_HOSTS = ['localhosts', '127.0.0.1', 'testserver']
```

Далее запускаем сервер и код описанный ниже:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status  # Импортируем статусы HTTP
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date


class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
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

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        instance.save()  # Сохранение изменений в БД
        return instance


class MyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        queryset = Entry.objects.all()  # Получаем все объекты модели
        serializer = EntrySerializer(queryset,
                                     many=True)  # Множество объектов для сериализации

        return Response(serializer.data)


# Создаем объект RequestFactory
factory = APIRequestFactory()
# Создаем объект APIClient
client = APIClient()

user_data = {
    "username": "admin",
    "password": "123"
}
# Передаем запрос на получение токена для пользователя
response = client.post('/token/', user_data, format='json')
token_data = response.json()
# Токен доступа
access_token = token_data.get("access")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyOTczNTkzLCJpYXQiOjE2OTI5NzMyOTMsImp0aSI6IjViNWRhZDA0Yjg0ODQxOTRiODdiOGFhM2EyN2E0MTI5IiwidXNlcl9pZCI6MX0.8Ea7HDi5IyZqiQxwXjo6u50MZQW5rnoKO0xRPc-ifNc'

# Создаем экземпляр представления
view = MyView.as_view()

# Создаем запрос и установливаем заголовок Authorization
request = factory.get('/my-view/')
request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"

# Отправляем запрос с заголовком Authorization
response = view(request)
# Проверяем результат
print(response.status_code)  # 200
print(response.data)  # Выводит все записи
```

###### Обновление токена
Если стоит задача обновления токена доступа, то достаточно отправить запрос на путь `'token/refresh/'` со словарем 
с ключом `"refresh"`, где прописан ключ который получали в запросе на получение ключа(только "refresh", а не "access")

Для примера:

```python
factory = APIRequestFactory()

user_data = {
    "username": "admin",
    "password": "123"
}

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Обработчик JWT для получения токена
token_view = TokenObtainPairView.as_view()
# Передаём запрос на получение токена для пользователя
request = factory.post('/token/', user_data, format='json')
response = token_view(request)
token_data = response.data
# Токен доступа
access_token = token_data.get("access")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyOTczNTkzLCJpYXQiOjE2OTI5NzMyOTMsImp0aSI6IjViNWRhZDA0Yjg0ODQxOTRiODdiOGFhM2EyN2E0MTI5IiwidXNlcl9pZCI6MX0.8Ea7HDi5IyZqiQxwXjo6u50MZQW5rnoKO0xRPc-ifNc'
# Токен обновления
refresh_token = token_data.get("refresh")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MzA2NTIxOSwiaWF0IjoxNjkyOTc4ODE5LCJqdGkiOiIyNWI2OTE4YWJhNjI0NmE2YjNiYTk1MWRkMzFiOTRhMiIsInVzZXJfaWQiOjF9.yPJv6tmL71cqtvJj433Gnn2LAf6H26-L-n3rKxK6xG8'
# Получения обновления для токена
request = factory.post('/token/refresh/', {"refresh": refresh_token}, format='json')
refresh_view = TokenRefreshView.as_view()
response = refresh_view(request)
token_data = response.data
# Новый токен доступа
access_token = token_data.get("access")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyOTc5MTY5LCJpYXQiOjE2OTI5Nzg4MTksImp0aSI6IjVkYzA3Y2YwMTlhYzQ0NGRhZTdhMjcyNWZkYTk3Y2JlIiwidXNlcl9pZCI6MX0.-Y2bhL5vNeIjv4KfEH_mjg2sh4cDawHzuN6uXtaSt6E'
```

###### Проверка токена

Если стоит задача проверки токена, то достаточно отправить запрос на путь `'token/verify/''` со словарем 
с ключом `"token"`, где прописан ключ который получали в запросе на получение ключа("access")

В ответе вы получите информацию о валидности или невалидности токена. Если токен действителен, вы получите статус 200 OK 
и JSON-ответ:

```json
{
    "detail": "Token is valid"
}
```
Если токен недействителен, вы получите статус 401 Unauthorized и JSON-ответ:
```json
{
    "detail": "Token is invalid or expired"
}
```

Для примера:

```python
# Создаем объект RequestFactory
factory = APIRequestFactory()

user_data = {
    "username": "admin",
    "password": "123"
}

from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
# Обработчик JWT для получения токена
token_view = TokenObtainPairView.as_view()
# Передаём запрос на получение токена для пользователя
request = factory.post('/token/', user_data, format='json')
response = token_view(request)
token_data = response.data
# Токен доступа
access_token = token_data.get("access")  # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyOTczNTkzLCJpYXQiOjE2OTI5NzMyOTMsImp0aSI6IjViNWRhZDA0Yjg0ODQxOTRiODdiOGFhM2EyN2E0MTI5IiwidXNlcl9pZCI6MX0.8Ea7HDi5IyZqiQxwXjo6u50MZQW5rnoKO0xRPc-ifNc'
# Проверка токена
request = factory.post('/token/verify/', {"token": access_token}, format='json')
refresh_view = TokenVerifyView.as_view()
response = refresh_view(request)
print(response.status_code)  # 200
```

###### Настройка simplejwt

В `settings.py` в переменной `SIMPLE_JWT` можно прописать ряд параметров для управления поведением обработкой JWT.

Все настройки из [документации](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)

```python
# Django project settings.py

from datetime import timedelta
...
# В значениях приведены параметры используемые по умолчанию
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
```

* `ACCESS_TOKEN_LIFETIME`: Определяет срок действия токена доступа (access token). Этот параметр указывает, сколько 
времени токен доступа будет действителен. Например, timedelta(minutes=60) означает, что токен будет действителен 
в течение 1 часа.

По умолчанию равен времени сессии в Django, равной 2 недели (1209600 секунд).

* `REFRESH_TOKEN_LIFETIME`: Определяет срок действия токенов обновления (refresh tokens). Токен обновления позволяет 
пользователю обновить свой токен доступа (access token) после истечения его срока действия без необходимости повторной 
аутентификации. Этот параметр задает, сколько времени токен обновления будет действителен. Например, если установлено 
значение timedelta(days=30), то токен обновления будет действителен в течение 30 дней, после чего пользователю потребуется
повторная аутентификация.

По умолчанию явно не указан срок.

* `ROTATE_REFRESH_TOKENS`: Если установлен в True, токен обновления будет обновлен при каждом его использовании для 
продления токена доступа. Это может повысить безопасность вашей системы.

* `BLACKLIST_AFTER_ROTATION`: Определяет, будет ли токен обновления, использованный для обновления токена доступа, 
добавлен в черный список (blacklist) после использования. Когда токен обновления используется для получения нового токена 
доступа, он может быть инвалидирован, чтобы предотвратить его дальнейшее использование. 
Если `BLACKLIST_AFTER_ROTATION` установлен в True, токен обновления будет добавлен в черный список после обновления, 
и его дальнейшее использование будет невозможно. Если `BLACKLIST_AFTER_ROTATION` установлен в False, токен обновления 
останется действительным, и его можно будет использовать многократно для обновления токена доступа.

* `UPDATE_LAST_LOGIN`: Если установлено значение True, поле Last_login в таблице auth_user обновляется при входе 
в систему (TokenObtainPairView).
**Предупреждение**. Обновление last_login резко увеличит количество транзакций базы данных. 
Люди, злоупотребляющие представлениями, могут замедлить работу сервера, и это может стать уязвимостью безопасности. 
Если вы действительно этого хотите, ограничите конечную точку как минимум с помощью DRF.

* `ALGORITHM`: Определяет алгоритм, используемый для подписи JWT-токенов. По умолчанию используется алгоритм 'HS256' 
(HMAC с SHA-256). Вы можете выбрать другой поддерживаемый алгоритм, если это необходимо. 
Алгоритм из библиотеки PyJWT, который будет использоваться для выполнения операций подписи/проверки токенов. 

Для использования симметричной подписи и проверки `HMAC` можно использовать следующие алгоритмы: `'HS256'`, `'HS384'`, 
`'HS512'`. Если выбран алгоритм `HMAC`, этот `SIGNING_KEY` параметр будет использоваться как в качестве ключа подписи, 
так и в качестве ключа проверки. В этом случае `VERIFYING_KEY` настройка будет игнорироваться. 

Для использования асимметричной подписи и проверки `RSA` можно использовать следующие алгоритмы: `'RS256'`, `'RS384'`, 
`'RS512'`. Если выбран алгоритм `RSA`, в `SIGNING_KEY` качестве параметра должна быть установлена строка, содержащая 
закрытый ключ `RSA`. Аналогичным образом, для `VERIFYING_KEY` параметра должна быть установлена строка, содержащая 
открытый ключ `RSA`.

* `SIGNING_KEY`: Ключ подписи, используемый для подписи содержимого сгенерированных токенов. Для подписи `HMAC` это должна 
быть случайная строка, содержащая как минимум столько бит данных, сколько требуется протоколом подписи. Для подписи `RSA` 
это должна быть строка, содержащая закрытый ключ `RSA` длиной 2048 бит или больше. Поскольку Simple JWT по умолчанию 
использует 256-битную подпись `HMAC`, по `SIGNING_KEY` умолчанию используется значение параметра `SECRET_KEY` вашего проекта 
django. Хотя это наиболее разумное значение по умолчанию, которое может предоставить Simple JWT, разработчикам рекомендуется 
изменить этот параметр на значение, независимое от секретного ключа проекта django. Это облегчит изменение ключа подписи, 
используемого для токенов, в случае его компрометации.

* `VERIFYING_KEY`: Ключ проверки, который используется для проверки содержимого сгенерированных токенов. Если в настройке 
указан алгоритм `HMAC ALGORITHM`, этот `VERIFYING_KEY` параметр будет игнорироваться и `SIGNING_KEY` будет использоваться 
его значение. Если в настройке указан алгоритм `RSA ALGORITHM`, `VERIFYING_KEY` для параметра должна быть задана строка, 
содержащая открытый ключ `RSA`.

* `AUDIENCE`: Позволяет задать требуемую аудиторию (aud) для JWT-токенов. 
Аудитория указывает, для кого предназначен токен. Это может быть полезно, если вы хотите убедиться, что ваш токен может 
быть использован только определенным клиентом или сервисом. Если параметр AUDIENCE задан и значение aud в JWT-токене 
не совпадает с заданным AUDIENCE, токен считается недействительным.

* `ISSUER`: Позволяет задать издателя (iss) JWT-токенов. Издатель обычно указывает на сервис или приложение, которое 
создало токен. Указание издателя может помочь вам проверить подлинность токена и убедиться, что он был создан ожидаемой 
стороной. Если параметр `ISSUER` задан и значение iss в JWT-токене не совпадает с заданным `ISSUER`, токен считается недействительным.

* `JWK_URL`: `JWK_URL` используется для динамического разрешения открытых ключей, необходимых для проверки подписи токенов. 
Например, при использовании Auth0 вы можете установить для этого параметра значение 
`'https://yourdomain.auth0.com/.well-known/jwks.json'`. Если установлено значение None, это поле исключается из серверной 
части токена и не используется во время проверки.

* `LEEWAY`(Скользящее окно времени): позволяет установить временной диапазон (в секундах), в пределах которого JWT-токен 
считается действительным, даже если время его создания (время начала действия) или истечения срока (время окончания действия) 
не точно соответствуют текущему времени. Это может быть полезно, чтобы учесть разницу во времени между серверами или 
возможные временные задержки при обработке запросов.

Например, если LEEWAY установлен в 60 секунд, то токен будет считаться действительным, если он истекает или начинает действовать в течение 60 секунд до или после текущего времени.

* `AUTH_HEADER_TYPES`: Список строк, которые могут быть использованы как типы заголовков авторизации. По умолчанию, 
AUTH_HEADER_TYPES установлен в ('Bearer',), что означает, что JWT-токены могут быть переданы в заголовке Authorization 
с префиксом "Bearer". Вы можете изменить этот список по своему усмотрению. `Authorization: Bearer <token>('Bearer', 'JWT')`

* `AUTH_HEADER_NAME`: Имя заголовка авторизации, которое будет использоваться для аутентификации. 
По умолчанию используется тот HTTP_AUTHORIZATION, который будет принимать Authorization заголовок в запросе. 
Например, если вы хотите использовать X_Access_Token в заголовке своих запросов, укажите это AUTH_HEADER_NAME в 
HTTP_X_ACCESS_TOKEN своих настройках.

* `USER_ID_FIELD`: определяет, какое поле модели пользователя (обычно User в Django) будет использоваться для определения 
идентификатора пользователя (user ID), который будет включен в JWT-токен. 

По умолчанию устанавливается значение 'id', что означает, что поле id модели User будет использоваться для идентификации 
пользователя в токене.

* `USER_ID_CLAIM`: определяет имя поля (claim) в JWT-токене, в котором будет храниться идентификатор пользователя. 

Значение по умолчанию - 'user_id'. 

* `USER_AUTHENTICATION_RULE`: определяет правило для аутентификации пользователя с использованием JWT-токена. 

По умолчанию используется 'rest_framework_simplejwt.authentication.default_authentication_rule', которое выполняет 
аутентификацию на основе наличия и валидности JWT-токена. Вы можете настроить свое собственное правило аутентификации, 
если ваши требования отличаются.

* `AUTH_TOKEN_CLASSES`: позволяет задать классы для создания и валидации JWT-токенов. 

По умолчанию используется список классов, включая 'rest_framework_simplejwt.tokens.AccessToken' для токена доступа 
и 'rest_framework_simplejwt.tokens.RefreshToken' для токена обновления. Вы можете использовать свои собственные классы, 
если у вас есть специфические требования.

* `TOKEN_TYPE_CLAIM`: определяет имя поля (claim) в JWT-токене, которое будет использоваться для указания типа токена. 
Это может быть полезно, если вы хотите различать токены доступа и токены обновления, сохраненные в одной базе данных.

* `JTI_CLAIM`: определяет имя поля (claim) в JWT-токене, в котором будет храниться уникальный идентификатор (JTI) токена. 
Этот идентификатор может быть использован для инвалидации (отзыва) токена в случае необходимости.

* `TOKEN_USER_CLASS`: определяет класс пользователя, который будет создан из данных JWT-токена. 

По умолчанию, используется 'rest_framework_simplejwt.models.TokenUser', который предоставляет структуру для пользователя 
на основе данных из токена.

* `SLIDING_TOKEN_REFRESH_EXP_CLAIM`: Имя утверждения, которое используется для хранения времени истечения срока 
обновления скользящего токена

* `SLIDING_TOKEN_LIFETIME`: Определяет срок действия токена доступа после его обновления с использованием токена 
обновления. Если этот параметр установлен, то токен доступа будет действителен только на протяжении указанного периода 
после каждого обновления. Если не установлен, то срок действия токена будет начинаться заново после каждого обновления.

* `SLIDING_TOKEN_REFRESH_LIFETIME`: Указывает период, через который токен обновления (refresh token) может быть использован 
для продления срока действия токена доступа. Например, timedelta(days=1) означает, что пользователь может использовать 
токен обновления каждый день для продления срока действия токена доступа.

* `CHECK_REVOKE_TOKEN`: Если для этого поля установлено значение True, система проверит, был ли токен отозван или нет, путем 
сравнения хэша md5 текущего пароля пользователя со значением, хранящимся в поле REVOKE_TOKEN_CLAIM в полезных данных токена JWT.

* `REVOKE_TOKEN_CLAIM`: Имя утверждения, которое используется для хранения хеш-пароля пользователя. Если значение этого поля 
CHECK_REVOKE_TOKEN равно True, это поле будет включено в полезную нагрузку JWT.


Эти параметры позволяют настроить поведение и безопасность JWT-токенов в вашем приложении согласно вашим требованиям. Вам следует тщательно оценить параметры в SIMPLE_JWT, чтобы обеспечить безопасность и срок действия токенов, соответствующие вашим потребностям.

Допустим если рассмотреть такой пример:

```python

```

###### Добавление токенов в "черный список"

[Документация](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html)
Если есть необходимость целенаправленного заблокирования обслуживания токенов(даже если они работоспособны), то Simple JWT 
включает в себя приложение, предоставляющее функции черного списка токенов. 
Чтобы использовать это приложение, включите его в список установленных приложений в settings.py

```python
INSTALLED_APPS = (
    ...
    'rest_framework_simplejwt.token_blacklist',
    ...
)
```

Так как данные о заблокированных токенах будут храниться в БД, то необходимо выполнить команду
`python manage.py migrate` 
для создания таблицы в БД

В панели админа появится таблицы(Outstanding tokens, Blacklisted tokens)
![img_6.png](img_6.png)

Приложение «Черный список» Simple JWT реализует списки выдающихся и занесенных в черный список токенов, используя две модели: 
`OutstandingToken` и `BlacklistedToken`. Доступ к таблицам можно получить через панель администратора. Чтобы добавить 
токен в черный список, найдите соответствующую `OutstandingToken` запись в администраторе и снова используйте администратор, 
чтобы создать запись `BlacklistedToken`, указывающую на эту `OutstandingToken` запись.

Добавление в черный список через код можно через метод `blacklist()` экземпляра класса `RefreshToken`

```python
from rest_framework_simplejwt.tokens import RefreshToken

token = RefreshToken(base64_encoded_token_string)
token.blacklist()
```
Также можно работать через представление `TokenBlacklistView`

```python
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
  ...
  path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
  ...
]
```

Ниже приведён пример использования и ручного тестирования:



###### Настройка пользовательских заявок на токены
[Документация](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html)
Если необходимо 

#### 1.2.4 Ограничение скорости запросов с throttle_classes

#### 1.2.5 Получение данных с использованием пагинации



## GenericAPIView

`GenericAPIView` позволяют упростить часть повторяющихся задач, чтобы в итоге кода было меньше и не было необходимости
так объёмно описывать обработчик как при `APIView`.

![img_5.png](img_5.png)


