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
    path('api-auth/', include('rest_framework.urls'))
]
```

![img_1.png](img_1.png)

Также в settings.py в словаре REST_FRAMEWORK можно настроить общее поведение фреймворка

1. ключ `DEFAULT_RENDERER_CLASSES`: Определяет классы рендеринга (отображения) контента. 
По умолчанию `['rest_framework.renderers.JSONRenderer']`

Значения `DEFAULT_RENDERER_CLASSES`:
   * `rest_framework.renderers.JSONRenderer` для JSON-отображения.
   * `rest_framework.renderers.BrowsableAPIRenderer` Класс рендеринга, который предоставляет интерфейс API для просмотра 
   и взаимодействия с API через веб-браузер
   * `rest_framework.renderers.TemplateHTMLRenderer` Класс рендеринга для преобразования данных в HTML-шаблоны. 
   Используется, когда API предоставляет поддержку отображения данных через HTML-страницы.
   * `rest_framework.renderers.AdminRenderer` Класс рендеринга, который применяет стили и форматирование, соответствующие 
   стилю административной панели Django, к данным API.
   * `rest_framework.renderers.YAMLRenderer` Класс рендеринга для преобразования данных в формат YAML.

Вы можете выбрать один или несколько из этих классов рендеринга и указать их в `DEFAULT_RENDERER_CLASSES` в словаре 
`REST_FRAMEWORK`, чтобы они использовались в качестве классов рендеринга по умолчанию для вашего проекта.

2. ключ `DEFAULT_PARSER_CLASSES`: Определяет классы парсера, используемые для разбора входящего запроса. 
По умолчанию `['rest_framework.parsers.JSONParser']`

Значения `DEFAULT_PARSER_CLASSES`:
   * `rest_framework.parsers.JSONParser` Класс парсера для разбора входящих данных в формате JSON.
   * `rest_framework.parsers.FormParser` Класс парсера для разбора данных, отправленных в формате application/x-www-form-urlencoded
   * `rest_framework.parsers.MultiPartParser` Класс парсера для разбора данных формы, отправленных с использованием 
мультипартного содержимого (multipart/form-data). Обычно используется для загрузки файлов
   * `rest_framework.parsers.FileUploadParser` Класс парсера для загрузки файлов с использованием мультипартного содержимого. 
Обрабатывает загрузку файлов и сохраняет их во временное хранилище.
   * `rest_framework.parsers.YAMLParser` Класс парсера для разбора входящих данных в формате YAML.
   * `rest_framework.parsers.TextParser` Класс парсера для разбора текстовых данных.

3. ключ `DEFAULT_AUTHENTICATION_CLASSES`: Определяет классы аутентификации, используемые для проверки подлинности пользователя.
По умолчанию `['rest_framework.authentication.SessionAuthentication']`

Значения `DEFAULT_AUTHENTICATION_CLASSES`:
   * `rest_framework.authentication.BasicAuthentication` Класс аутентификации на основе базовой аутентификации HTTP. 
Клиенты должны предоставить имя пользователя и пароль при доступе к защищенным ресурсам API.
   * `rest_framework.authentication.SessionAuthentication` Класс аутентификации, основанный на сессиях Django. 
Используется для аутентификации пользователей с помощью сессий и cookie.
   * `rest_framework.authentication.TokenAuthentication` Класс аутентификации с помощью JSON Web Token (JWT). 
Клиенты должны предоставить JWT для аутентификации при доступе к защищенным ресурсам API.
   * `rest_framework.authentication.OAuth2Authentication` Класс аутентификации с помощью протокола OAuth 2.0. 
Используется для аутентификации и авторизации через сторонний OAuth-провайдер
   * `rest_framework.authentication.RemoteUserAuthentication` Класс аутентификации, использующий внешнюю систему аутентификации. 
Например, аутентификацию через протокол HTTP заголовком REMOTE_USER

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
   * `rest_framework.permissions.BasePermission` Абстрактный базовый класс для создания пользовательских классов разрешений. 
Вы можете создать собственные классы разрешений, унаследовавшись от `BasePermission` и определив свою логику доступа.

5. ключ `DEFAULT_PAGINATION_CLASS`: Определяет класс пагинации, используемый для разбиения больших наборов данных на страницы.
По умолчанию: `None` (без пагинации по умолчанию)

Значения `DEFAULT_PAGINATION_CLASS`:





6. ключ `DEFAULT_FILTER_BACKENDS`: Определяет классы фильтрации, используемые для фильтрации данных по определенным критериям
По умолчанию: []

Значения `DEFAULT_FILTER_BACKENDS`:



7. ключ `EXCEPTION_HANDLER`: Определяет пользовательскую функцию обработки исключений, которая будет вызываться при 
возникновении исключений во время обработки запросов API.
По умолчанию: []



8. ключ `DEFAULT_VERSIONING_CLASS`: Определяет класс версионирования, используемый для управления версиями API. 
По умолчанию: []



9. ключ `DEFAULT_THROTTLE_CLASSES`: Определяет классы ограничения скорости (throttle), которые контролируют частоту 
запросов от клиентов.
По умолчанию: []



10. ключ `DEFAULT_THROTTLE_RATES`: Определяет скорости ограничения для каждого класса ограничения скорости. 
По умолчанию: []


11. ключ `DEFAULT_CONTENT_NEGOTIATION_CLASS`: Определяет класс для выбора контента на основе заголовков запроса. 
По умолчанию: []


12. ключ `DEFAULT_METADATA_CLASS`: Определяет класс метаданных, используемый для генерации метаданных API. 
По умолчанию: []


13. ключ `DEFAULT_VERSION`: Определяет версию API по умолчанию, используемую при обращении к API без указания конкретной версии.
По умолчанию: []


14. ключ `ALLOWED_VERSIONS`: Определяет список разрешенных версий API, которые могут быть указаны в запросах.
По умолчанию: []


15. ключ `UNAUTHENTICATED_USER`: Определяет представление пользователя, используемое для невошедших в систему пользователей. 
По умолчанию: []


16. ключ `DEFAULT_METADATA_CLASS`: Определяет класс метаданных, используемый для генерации метаданных API. 
По умолчанию: []


17. ключ `DEFAULT_SCHEMA_CLASS`: Определяет класс схемы (schema), используемый для автоматической генерации схемы API.
По умолчанию: []

    