В settings.py в словаре REST_FRAMEWORK можно настроить общее поведение фреймворка. Про настройки из 
[руководства](https://www.django-rest-framework.org/api-guide/settings/)

Значения по умолчанию и ключи, можно получить из `api_settings`

```python
from rest_framework.settings import api_settings

print(api_settings.defaults)
```
Передаваемые ключи в словарь REST_FRAMEWORK (задаваемом в settings.py) и их значения:

1. ключ `DEFAULT_RENDERER_CLASSES`: Определяет классы рендеринга (отображения) контента. 
По умолчанию `['rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer']`

Более полно в [документации](https://www.django-rest-framework.org/api-guide/renderers/)

Значения `DEFAULT_RENDERER_CLASSES`:
   * `rest_framework.renderers.JSONRenderer` для JSON-отображения.
   * `rest_framework.renderers.BrowsableAPIRenderer` Класс рендеринга, который предоставляет интерфейс API для просмотра 
   и взаимодействия с API через веб-браузер
   * `rest_framework.renderers.TemplateHTMLRenderer` Отображает данные в HTML, используя стандартный рендеринг шаблонов Django. 
   Используется, когда API предоставляет поддержку отображения данных через HTML-страницы.
   * `rest_framework.renderers.StaticHTMLRenderer` Класс визуализатора HTML, который просто возвращает предварительно обработанный HTML.
   * `rest_framework.renderers.HTMLFormRenderer` Визуализирует данные сериализатора в HTML-форму.
   * `rest_framework.renderers.AdminRenderer` Класс рендеринга, который применяет стили и форматирование, соответствующие 
   стилю административной панели Django, к данным API.
   * `rest_framework.renderers.DocumentationRenderer` Класс рендеринга, который предоставляет документацию API в формате 
HTML. Он используется для генерации документации на основе метаданных API, которые определяются во вьюсетах Django Rest 
Framework. Документация может включать информацию о доступных эндпоинтах, методах, параметрах запроса, сериализаторах и 
других деталях API. Класс `DocumentationRenderer` используется, когда API поддерживает интерфейс документации и 
взаимодействие через веб-браузер.
   * `rest_framework.renderers.MultiPartRenderer` Класс рендеринга для обработки мультипартных данных (multipart/form-data) 
во время загрузки файлов или отправки данных через форму. Он используется для разбора мультипартных запросов и представления 
ответа в соответствующем формате. Например, если клиент отправляет файл на сервер через форму, MultiPartRenderer позволяет 
корректно обработать этот запрос и обработать загруженный файл.
   * `rest_framework.renderers.SchemaJSRenderer` Класс рендеринга для преобразования схемы API в формате JSON в скрипт 
JavaScript. Этот скрипт может быть использован на клиентской стороне для динамической генерации интерфейса, взаимодействия 
с API или создания документации API в интерактивном виде.

Можно создать свой класс унаследовавшись от `BaseRenderer`, соответственно указав его в значениях `DEFAULT_RENDERER_CLASSES`
```python
from rest_framework.renderers import BaseRenderer

class MyRenderer(BaseRenderer):
    ...
```


Вы можете выбрать один или несколько из этих классов рендеринга и указать их в `DEFAULT_RENDERER_CLASSES` в словаре 
`REST_FRAMEWORK`, чтобы они использовались в качестве классов рендеринга по умолчанию для вашего проекта.

2. ключ `DEFAULT_PARSER_CLASSES`: Определяет классы парсера, используемые для разбора входящего запроса. 
По умолчанию `['rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser', 'rest_framework.parsers.MultiPartParser']`

Значения `DEFAULT_PARSER_CLASSES`:
   * `rest_framework.parsers.JSONParser` Класс парсера для разбора входящих данных в формате JSON.
   * `rest_framework.parsers.FormParser` Класс парсера для разбора данных, отправленных в формате application/x-www-form-urlencoded
   * `rest_framework.parsers.MultiPartParser` Класс парсера для разбора данных формы, отправленных с использованием 
мультипартного содержимого (multipart/form-data). Обычно используется для загрузки файлов
   * `rest_framework.parsers.FileUploadParser` Класс парсера для загрузки файлов с использованием мультипартного содержимого. 
Обрабатывает загрузку файлов и сохраняет их во временное хранилище.

Можно создать свой класс унаследовавшись от `BaseParser`, соответственно указав его в значениях `DEFAULT_PARSER_CLASSES`
```python
from rest_framework.parsers import BaseParser

class MyParser(BaseParser):
    ...
```

3. ключ `DEFAULT_AUTHENTICATION_CLASSES`: Определяет классы аутентификации, используемые для проверки подлинности пользователя.
По умолчанию `['rest_framework.authentication.SessionAuthentication', 'rest_framework.authentication.BasicAuthentication']`

Значения `DEFAULT_AUTHENTICATION_CLASSES`:
   * `rest_framework.authentication.BasicAuthentication` Класс аутентификации на основе базовой аутентификации HTTP. 
Клиенты должны предоставить имя пользователя и пароль при доступе к защищенным ресурсам API.
   * `rest_framework.authentication.SessionAuthentication` Класс аутентификации, основанный на сессиях Django. 
Используется для аутентификации пользователей с помощью сессий и cookie.
   * `rest_framework.authentication.TokenAuthentication` Класс аутентификации с помощью JSON Web Token (JWT). 
Клиенты должны предоставить JWT для аутентификации при доступе к защищенным ресурсам API.
   * `rest_framework.authentication.RemoteUserAuthentication` Класс аутентификации, использующий внешнюю систему аутентификации. 
Например, аутентификацию через протокол HTTP заголовком REMOTE_USER

Можно создать свой класс унаследовавшись от `BaseAuthentication`, соответственно указав его в значениях `DEFAULT_AUTHENTICATION_CLASSES`
```python
from rest_framework.authentication import BaseAuthentication

class MyAuthentication(BaseAuthentication):
    ...
```

4. ключ `DEFAULT_PERMISSION_CLASSES`: Определяет классы разрешений, используемые для определения доступа к ресурсам API.
По умолчанию  `['rest_framework.permissions.AllowAny']`

Значения `DEFAULT_PERMISSION_CLASSES`:
   * `rest_framework.permissions.AllowAny` Разрешает доступ к ресурсам API для всех пользователей, 
включая неаутентифицированных пользователей.
   * `rest_framework.permissions.IsAuthenticated` Разрешает доступ только аутентифицированным пользователям. 
Неаутентифицированным пользователям доступ запрещен.
   * `rest_framework.permissions.IsAdminUser` Разрешает доступ только администраторам. Неадминистраторам доступ запрещен.
   * `rest_framework.permissions.IsAuthenticatedOrReadOnly` Разрешает доступ аутентифицированным пользователям для выполнения 
операций записи (POST, PUT, PATCH, DELETE) и доступ неаутентифицированным пользователям только для операций чтения (GET)
   * `rest_framework.permissions.DjangoModelPermissions` Разрешает доступ на основе прав доступа модели Django. 
Определяет доступ на основе разрешений, определенных в модели.
   * `rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly` Аналогично DjangoModelPermissions, за исключением того, что анонимные пользователи
разрешен доступ только для чтения.
   * `rest_framework.permissions.DjangoObjectPermissions` Разрешает доступ на основе прав доступа к конкретному объекту 
модели Django. Определяет доступ на основе разрешений, определенных в модели для каждого объекта.

Можно создать свой класс унаследовавшись от `BasePermission`, соответственно указав его в значениях `DEFAULT_PERMISSION_CLASSES`
```python
from rest_framework.permissions import BasePermission

class MyPermission(BasePermission):
    ...
```

5. ключ `DEFAULT_PAGINATION_CLASS`: Определяет класс пагинации, используемый для разбиения больших наборов данных на страницы.
По умолчанию: `None` (без пагинации по умолчанию)

Значения `DEFAULT_PAGINATION_CLASS`:
   * `rest_framework.pagination.PageNumberPagination` Класс пагинации на основе номера страницы. 
Позволяет клиентам запрашивать конкретные страницы путем указания номера страницы в параметрах запроса.
   ```
   http://api.example.org/accounts/?page=4
   http://api.example.org/accounts/?page=4&page_size=100
   ```
   * `rest_framework.pagination.LimitOffsetPagination` Класс пагинации на основе лимита и смещения. 
Позволяет клиентам запрашивать определенное количество элементов, начиная с определенного смещения.
   ```
   http://api.example.org/accounts/?limit=100
   http://api.example.org/accounts/?offset=400&limit=100
   ```
   * `rest_framework.pagination.CursorPagination` Класс пагинации на основе курсора. 
Позволяет клиентам перемещаться по страницам, используя указатель курсора, который определяет текущую позицию.  
Вместо использования номеров страниц или лимитов и смещений, курсорная пагинация использует курсоры, чтобы помнить текущую 
позицию в наборе данных и позволяет клиентам перемещаться вперед и назад по страницам. Курсоры обычно представляют собой 
уникальные значения полей сортировки, и с их помощью клиенты могут запрашивать следующую или предыдущую страницу данных.
   ```
   http://api.example.org/accounts/?cursor=eyJ0eXBlIjoiY3Vyc29yIiwiaWQiOiI1OTBjMmM3ODg0Y2I2ZTAwMTc1N2I5NTgifQ%3D%3D
   ```

Можно создать свой класс унаследовавшись от `BasePagination`, соответственно указав его в значениях `DEFAULT_PAGINATION_CLASS`
```python
from rest_framework.pagination import BasePagination

class MyPagination(BasePagination):
    ...
```

6. ключ `PAGE_SIZE`: Определяет количество объектов, которые будут возвращены в одной странице при использовании пагинации. 
Если ваше API возвращает большое количество объектов, пагинация позволяет разбить результаты на отдельные страницы. 
Этот параметр устанавливает количество объектов на одной странице. Например, если PAGE_SIZE равен 10, то API вернет не 
более 10 объектов на одной странице.
По умолчанию: `None`

```python
REST_FRAMEWORK = {
    'PAGE_SIZE': 20,  # Определение количества объектов на одной странице пагинации
    # Другие настройки...
}
```

7. ключ `DEFAULT_FILTER_BACKENDS`: Определяет классы фильтрации, используемые для фильтрации данных по определенным критериям
По умолчанию: []

Значения `DEFAULT_FILTER_BACKENDS`:
   * `rest_framework.filters.SearchFilter` Класс фильтрации поиска. Позволяет клиентам выполнять поиск по определенным 
полям модели.
   * `rest_framework.filters.OrderingFilter` Класс фильтрации сортировки. Позволяет клиентам выполнять сортировку данных 
по определенным полям модели.
   * `rest_framework.filters.DjangoFilterBackend` Класс фильтрации на основе фильтров Django. Позволяет клиентам выполнять 
фильтрацию на основе полей модели, определенных в фильтрах Django.

Можно создать свой класс унаследовавшись от `BaseFilterBackend`, соответственно указав его в значениях `DEFAULT_FILTER_BACKENDS`
```python
from rest_framework.filters import BaseFilterBackend

class MyFilter(BaseFilterBackend):
    ...
```

8. ключ `DEFAULT_VERSIONING_CLASS`: Определяет класс версионирования, используемый для управления версиями API. 
По умолчанию: `None`

Значения `DEFAULT_VERSIONING_CLASS`:
   * `rest_framework.versioning.AcceptHeaderVersioning` Класс версионирования, который определяет версию API на основе 
   значения заголовка Accept в запросе. Клиенты могут указывать версию API в заголовке Accept, например, `Accept: application/json; version=1.0`.
   * `rest_framework.versioning.NamespaceVersioning` Класс версионирования, который определяет версию API на основе 
пространства имен (namespace). В URL маршрутах API используется префикс с указанием версии, например, `/v1/endpoint/`.
   * `rest_framework.versioning.URLPathVersioning` Класс версионирования, который определяет версию API на основе пути URL. 
В URL маршрутах API используется часть пути с указанием версии, например, `/api/v1/endpoint/`.
   * `rest_framework.versioning.HostNameVersioning` Класс версионирования для указания версии в хосте.
   ```
   GET /something/ HTTP/1.1
   Host: v1.example.com
   Accept: application/json
   ```
   * `rest_framework.versioning.QueryParameterVersioning` Класс версионирования, который определяет версию API на основе 
параметра запроса. Клиенты могут указывать версию API в параметре запроса, например, `/endpoint/?version=1.0`.
   ```
   GET /something/?version=0.1 HTTP/1.1
   Host: example.com
   Accept: application/json
   ```

Можно создать свой класс унаследовавшись от `BaseVersioning`, соответственно указав его в значениях `DEFAULT_VERSIONING_CLASS`
```python
from rest_framework.versioning import BaseVersioning

class MyVersioning(BaseVersioning):
    ...
```

9. ключ `DEFAULT_VERSION`: Определяет версию API по умолчанию, используемую при обращении к API без указания конкретной версии.
По умолчанию: `None`. Параметр DEFAULT_VERSION указывает версию, которая будет использоваться, если клиент не предоставил 
явное указание версии в запросе.

Пример:  `'DEFAULT_VERSION': '1.0'`

10. ключ `DEFAULT_THROTTLE_CLASSES`: Определяет классы ограничения скорости (throttle), которые контролируют частоту 
запросов от клиентов.
По умолчанию: []

Значения `DEFAULT_THROTTLE_CLASSES`:
   * `rest_framework.throttling.AnonRateThrottle` Класс ограничения скорости для анонимных пользователей. 
Ограничивает частоту запросов анонимных пользователей.
   * `rest_framework.throttling.UserRateThrottle` Класс ограничения скорости для зарегистрированных пользователей. 
Ограничивает частоту запросов зарегистрированных пользователей.
   * `rest_framework.throttling.ScopedRateThrottle` Класс ограничения скорости на основе области видимости (scope). 
Позволяет определять пользовательские области видимости и ограничивать запросы в каждой области отдельно.
   * `rest_framework.throttling.SimpleRateThrottle` Простой класс ограничения скорости, который ограничивает все запросы 
без различения по пользователям или областям видимости.

Можно создать свой класс унаследовавшись от `BaseThrottle`, соответственно указав его в значениях `DEFAULT_THROTTLE_CLASSES`
```python
from rest_framework.throttling import BaseThrottle

class MyThrottle(BaseThrottle):
    ...
```

11. ключ `DEFAULT_THROTTLE_RATES`: Определяет скорости ограничения для каждого класса ограничения скорости. 
По умолчанию: `{'user': None, 'anon': None}`

Пример:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',  # Скорость для анонимных пользователей: 100 запросов в день
        'user': '1000/day', # Скорость для зарегистрированных пользователей: 1000 запросов в день
    },
    # Другие настройки...
}
```
Также можно выстроить другие временные ограничения такие как `second`, `minute`, `hour`


12. ключ `DEFAULT_CONTENT_NEGOTIATION_CLASS`: Определяет класс для выбора контента на основе заголовков запроса. 
По умолчанию: `rest_framework.negotiation.DefaultContentNegotiation`

Значения `DEFAULT_CONTENT_NEGOTIATION_CLASS`:
* `rest_framework.negotiation.DefaultContentNegotiation` Класс контент-неготиации по умолчанию. Он обрабатывает запросы 
и выбирает наиболее подходящий формат представления данных на основе заголовков запроса.

Можно создать свой класс унаследовавшись от `BaseContentNegotiation`, соответственно указав его в значениях `DEFAULT_CONTENT_NEGOTIATION_CLASS`
```python
from rest_framework.negotiation import BaseContentNegotiation

class MyNegotiation(BaseContentNegotiation):
    ...
```

13. ключ `DEFAULT_METADATA_CLASS`: Определяет класс метаданных, используемый для генерации метаданных API. 
По умолчанию: `rest_framework.metadata.SimpleMetadata`

Значения `DEFAULT_METADATA_CLASS`:
   * `rest_framework.metadata.SimpleMetadata` Класс метаданных по умолчанию, который предоставляет простую информацию об 
эндпоинтах, методах и типах запросов.

Можно создать свой класс унаследовавшись от `BaseMetadata`, соответственно указав его в значениях `DEFAULT_METADATA_CLASS`
```python
from rest_framework.metadata import BaseMetadata

class MyMetadata(BaseMetadata):
    ...
```

14. ключ `DEFAULT_SCHEMA_CLASS`: Определяет класс схемы (schema), используемый для автоматической генерации схемы API.

По умолчанию: `rest_framework.schemas.openapi.AutoSchema`

Значения `DEFAULT_SCHEMA_CLASS`:
   * `rest_framework.schemas.AutoSchema` Класс схемы, который автоматически генерирует схему API на основе метаданных API, 
определенных во вьюсетах Django Rest Framework. Он является классом схемы по умолчанию и предоставляет максимальное количество 
информации о вашем API. Он может использоваться для автоматической генерации документации API и интеграции с инструментами, 
поддерживающими различные форматы схем, такие как CoreAPI и OpenAPI (Swagger).
   * `rest_framework.schemas.ManualSchema` Класс схемы, который позволяет вам явно определять схему API для вашего вьюсета. 
В отличие от AutoSchema, где схема генерируется автоматически на основе метаданных, ManualSchema требует явного определения 
структуры схемы. Вы можете использовать ManualSchema, если хотите предоставить более точную и контролируемую документацию 
или представление вашего API.
   * `rest_framework.schemas.SchemaGenerator` Класс который используется для генерации схемы API на основе представлений 
(вьюсетов) вашего проекта. Он является базовым классом, который используется внутри AutoSchema для автоматической генерации 
схемы API. Вы можете использовать SchemaGenerator непосредственно, если хотите получить доступ к схеме API в коде и 
управлять процессом генерации схемы вручную.


15. ключ `TEST_REQUEST_DEFAULT_FORMAT`: используется для определения формата по умолчанию, который будет использоваться 
при создании тестовых запросов во время тестирования API.

По умолчанию: `'multipart'`

Параметр `TEST_REQUEST_DEFAULT_FORMAT` может принимать значения из списка поддерживаемых форматов DRF, таких как `'json'`, 
`'api'`, `'jsonapi'`, `'xml'`, `'multipart'`.


16. ключ `TEST_REQUEST_RENDERER_CLASSES`:

По умолчанию: `['rest_framework.renderers.MultiPartRenderer', 'rest_framework.renderers.JSONRenderer']`

Значения `TEST_REQUEST_RENDERER_CLASSES` аналогичны `DEFAULT_RENDERER_CLASSES`


17. ключ `ALLOWED_VERSIONS`: Определяет список разрешенных версий API, которые могут быть указаны в запросах.

По умолчанию: `None`

Пример:
```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'ALLOWED_VERSIONS': ['1.0', '2.0'],  # Определение доступных версий API
    # Другие настройки...
}
```

18. ключ `UNAUTHENTICATED_USER`: Определяет представление пользователя, используемое для невошедших в систему пользователей. 

По умолчанию: `django.contrib.auth.models.AnonymousUser`


19. ключ `UNAUTHENTICATED_TOKEN`: Класс, который следует использовать для инициализации request.auth для неаутентифицированных запросов.

По умолчанию: `None`


20. ключ `EXCEPTION_HANDLER`: Определяет пользовательскую функцию обработки исключений, которая будет вызываться при 
возникновении исключений во время обработки запросов API.

По умолчанию: `rest_framework.views.exception_handler`

Можно сделать свой обработчик
```python
# my_app/settings.py
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Ваш кастомный код обработки исключения
    response = exception_handler(exc, context)
    if response is not None:
        response.data['custom_error'] = 'Something went wrong.'
    return response

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_app.settings.custom_exception_handler',
    # Другие настройки...
}
```

21. ключ `NUM_PROXIES`: Целое число от 0 или больше, которое можно использовать для указания количества прокси-серверов приложений, 
за которыми работает API. Это позволяет регулировать более точно идентифицировать IP-адреса клиентов. Если установлено 
значение None, то классы дросселя будут использовать менее строгое сопоставление IP-адресов.

По умолчанию: `None`

22. ключ `SEARCH_PARAM`: Определяет имя параметра запроса, который будет использоваться для выполнения поисковых запросов к вашему API. 
Когда клиент отправляет запрос с параметром, указанным в SEARCH_PARAM, DRF выполняет поиск и возвращает результаты, 
соответствующие поисковому запросу. Параметр SEARCH_PARAM позволяет задать имя параметра запроса для поиска.

По умолчанию: `'search'`

Пример:
```python
REST_FRAMEWORK = {
    'SEARCH_PARAM': 'q',  # Определение параметра запроса для поискового запроса
    # Другие настройки...
}

# Запрос к API будет выглядеть так
GET /api/posts/?q=django
```

23. ключ `ORDERING_PARAM`: Определяет имя параметра запроса, который будет использоваться для выполнения запросов с сортировкой данных. 
Когда клиент отправляет запрос с параметром, указанным в ORDERING_PARAM, DRF выполняет сортировку данных и возвращает 
результаты в указанном порядке.

По умолчанию: `'ordering'`

Пример:
```python
REST_FRAMEWORK = {
    'ORDERING_PARAM': 'sort',  # Определение параметра запроса для сортировки данных
    # Другие настройки...
}

# Запрос к API будет выглядеть так
GET /api/posts/?sort=-created_at
```

24. ключ `VERSION_PARAM`: Определяет имя параметра запроса, который будет использоваться для определения версии API. 
В DRF версионирование API может быть реализовано разными способами, и параметр VERSION_PARAM позволяет указать имя параметра 
запроса, в котором клиент может указать желаемую версию API.

По умолчанию: `'version'`

Пример:
```python
REST_FRAMEWORK = {
    'VERSION_PARAM': 'api_version',  # Определение параметра запроса для указания версии API
    # Другие настройки...
}

# Запрос к API будет выглядеть так
GET /api/v2/posts/?api_version=2
```

25. ключ `VIEW_NAME_FUNCTION`: Строка, представляющая функцию, которую следует использовать при создании имен представлений.

По умолчанию: `rest_framework.views.get_view_name`

26. ключ `VIEW_DESCRIPTION_FUNCTION`: Строка, представляющая функцию, которую следует использовать при создании описаний представлений.

По умолчанию: `rest_framework.views.get_view_description`

27. ключ `NON_FIELD_ERRORS_KEY`: Определяет имя ключа, используемого для сериализации и десериализации сообщений об ошибках, 
не связанных с конкретными полями. Этот ключ используется для хранения сообщений об ошибках, которые относятся ко всей 
форме или запросу, а не к конкретным полям формы или объекта. 

По умолчанию: `'non_field_errors'`. Вы можете изменить его на другое значение, если хотите 
использовать другое имя ключа для сообщений об ошибках.

28. ключ `URL_FORMAT_OVERRIDE`: Позволяет клиентам переопределять форматы ответов API путем добавления суффикса к URL. 
Если у вас есть формат ответа, который необходимо указать явно в URL, этот параметр может быть полезен. Если значение 
этого параметра равно None, переопределение формата URL-адреса будет отключено.

По умолчанию: `'format'`

Пример:
```python
REST_FRAMEWORK = {
    'URL_FORMAT_OVERRIDE': 'format',  # Использовать параметр 'format' в URL для указания формата ответа
    # Другие настройки...
}

# Запрос к API будет выглядеть так
GET /api/posts/?format=json 
или 
GET /api/posts/?format=xml
```

29. ключ `FORMAT_SUFFIX_KWARG`: Имя параметра в конфигурации URL, которое может использоваться для предоставления суффикса формата. 
Этот параметр применяется при использовании format_suffix_patterns для включения шаблонов URL-адресов с суффиксами.

По умолчанию: `'format'`

Пример:
```python
http://example.com/organizations.csv/

равнозначно 
http://example.com/organizations/?format=csv
```

30. ключ `URL_FIELD_NAME`: Строка, представляющая ключ, который следует использовать для полей URL-адресов, 
сгенерированных HyperlinkedModelSerializer.

По умолчанию: `'url'`


31. ключ `DATE_FORMAT`: Строка формата, которая должна использоваться по умолчанию для отображения выходных данных полей 
сериализатора DateTimeField. Если нет, то поля сериализатора DateTimeField будут возвращать объекты даты и времени Python, 
а кодировка даты и времени будет определяться модулем визуализации.

Может быть любым из `None`, `'iso-8601'` или строкой формата `strftime` Python.

По умолчанию: `'iso-8601'`

32. ключ `DATE_INPUT_FORMATS`: Список строк формата, которые должны использоваться по умолчанию для анализа входных данных 
в поля сериализатора DateTimeField.

Может быть списком, включающим строку `'iso-8601'` или строки формата Python `strftime`.

По умолчанию: `['iso-8601']`

33. ключ `DATETIME_FORMAT`: Строка формата, которая должна использоваться по умолчанию для отображения вывода полей 
сериализатора DateField. Если нет, то поля сериализатора DateField будут возвращать объекты даты Python, 
а кодировка даты будет определяться модулем визуализации.

Может быть любым из `None`, `'iso-8601'` или строкой формата `strftime` Python.

По умолчанию: `'iso-8601'`

34. ключ `DATETIME_INPUT_FORMATS`: Список строк формата, которые должны использоваться по умолчанию для разбора входных 
данных в поля сериализатора DateField.

Может быть списком, включающим строку `'iso-8601'` или строки формата Python `strftime`.

По умолчанию: `['iso-8601']`

35. ключ `TIME_FORMAT`: Строка формата, которая должна использоваться по умолчанию для отображения вывода полей 
сериализатора TimeField. Если нет, то поля сериализатора TimeField будут возвращать объекты времени Python, 
а кодировка времени будет определяться модулем визуализации.

Может быть любым из `None`, `'iso-8601'` или строкой формата `strftime` Python.

По умолчанию: `'iso-8601'`

36. ключ `TIME_INPUT_FORMATS`: Список строк формата, которые должны использоваться по умолчанию для синтаксического 
анализа входных данных в поля сериализатора TimeField.

Может быть списком, включающим строку `'iso-8601'` или строки формата Python `strftime`.

По умолчанию: `['iso-8601']`

37. ключ `UNICODE_JSON`: Если установлено значение `True`, в ответах JSON будут разрешены символы Юникода.

По умолчанию: `True`

38. ключ `COMPACT_JSON`: Если установлено значение `True`, ответы JSON будут возвращать компактные представления без 
пробелов после символов ':' и ','.

По умолчанию: `True`
Пример:
```python
# 'COMPACT_JSON': True
{"is_admin":false,"email":"jane@example"}
# 'COMPACT_JSON': False
{"is_admin": false, "email": "jane@example"}
```

39. ключ `STRICT_JSON`: Если установлено значение `True`, рендеринг и синтаксический анализ JSON будут учитывать только 
синтаксически допустимый JSON, вызывая исключение для расширенных значений с плавающей запятой (nan, inf, -inf), 
принятых модулем json Python. Это рекомендуемая настройка, так как эти значения обычно не поддерживаются. например, 
ни JSON.Parse в Javascript, ни тип данных JSON в PostgreSQL не принимают эти значения.

Если установлено значение `False`, рендеринг и синтаксический анализ JSON будут разрешающими. Однако эти значения по-прежнему 
недействительны и должны быть специально обработаны в вашем коде.

По умолчанию: `True`

40. ключ `COERCE_DECIMAL_TO_STRING`: При возврате десятичных объектов в представлениях API, которые не поддерживают 
собственный десятичный тип, обычно лучше всего возвращать значение в виде строки. Это позволяет избежать потери точности, 
которая происходит с двоичными реализациями с плавающей запятой.

Если установлено значение True, класс сериализатора DecimalField будет возвращать строки вместо объектов Decimal. Если 
установлено значение False, сериализаторы будут возвращать объекты Decimal, которые кодировщик JSON по умолчанию будет 
возвращать как числа с плавающей запятой.

По умолчанию: `True`

41. ключ `UPLOADED_FILES_USE_URL`: Отвечает за определение того, будут ли загруженные файлы доступны через URL или нет.

При работе с файловыми загрузками в DRF, вы можете определить, как обрабатывать ссылки на загруженные файлы. 
Один из способов - это предоставить ссылку на загруженные файлы в ответах API, чтобы клиенты могли получить доступ к этим файлам по URL.

Если параметр `UPLOADED_FILES_USE_URL` установлен в значение `True`, DRF будет предоставлять URL для загруженных файлов 
в ответах API. Если параметр установлен в значение `False`, DRF будет предоставлять объекты с информацией о файлах, но не 
будет создавать URL для доступа к ним.

По умолчанию: `True`


42. ключ `HTML_SELECT_CUTOFF`: Глобальная настройка для значения html_cutoff. Должно быть целым числом. 
Если установлено, это будет максимальное количество вариантов(отношений), которые будут отображаться в раскрывающемся списке выбора HTML. 
Установите None, чтобы отключить любые ограничения.

По умолчанию: `1000`


43. ключ `HTML_SELECT_CUTOFF_TEXT`: Строка, представляющая глобальную настройку для html_cutoff_text.
Если установлено, будет отображаться текстовый индикатор, если максимальное количество элементов было обрезано 
в раскрывающемся списке выбора HTML. По умолчанию «Более {count} элементов…»

По умолчанию: `'More than {count} items...'`


44. ключ `SCHEMA_COERCE_PATH_PK`: Если установлено, это сопоставляет идентификатор «pk» в конфигурации URL-адреса с 
фактическим именем поля при создании параметра пути схемы. Обычно это будет «id». Это дает более подходящее представление, 
поскольку «первичный ключ» является деталью реализации, тогда как «идентификатор» является более общей концепцией.

По умолчанию: `True`


45. ключ `SCHEMA_COERCE_METHOD_NAMES`: Если установлено, это используется для сопоставления внутренних имен методов набора 
представлений с именами внешних действий, используемых при создании схемы. Это позволяет нам генерировать имена, более 
подходящие для внешнего представления, чем те, которые используются внутри кодовой базы.

По умолчанию: `{'retrieve': 'read', 'destroy': 'delete'}`
