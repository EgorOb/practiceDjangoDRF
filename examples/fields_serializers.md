## Типы полей которые можно задать в сериализаторе.

В основном используется в случае использовании базового `Serializer` из `rest_framework.serializers`

### Параметры которые можно передавать в поля
Базовый блок который будет определяться как `**params`

* `read_only=False` - Указывает, что поле доступно только для чтения (сериализации) и не будет приниматься при десериализации данных.
Такое поле используется для представления данных, которые могут быть только прочитаны клиентом, но не могут быть изменены через API.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
```

* `write_only=False` - Определяет, что поле должно быть доступно только для записи (десериализации) и не будет включено в вывод (сериализацию).
Такое поле обычно используется для чувствительных данных, которые должны быть переданы на сервер для обработки, 
но не должны быть возвращены клиенту в ответе.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
```
* `required=None` - Указывает, является ли поле обязательным при десериализации данных.
Если `required` установлен в `True`, то поле должно быть предоставлено во входных данных. Если `False`, поле может быть опущено или иметь значение `None`.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
```
* `default=empty` -  Устанавливает значение по умолчанию для поля при десериализации, если поле не было предоставлено во входных данных.
Это значение будет использовано, если при десериализации не предоставлено значение для поля.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    is_active = serializers.BooleanField(default=True)
```
* `initial=empty` - Позволяет установить значение по умолчанию для поля при создании нового объекта.
Это значение будет использовано, если при десериализации не предоставлено значение для поля.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(initial='John')
```

* `source=None` - Определяет имя атрибута модели, из которого следует получить значение для поля.
Это полезно, когда название поля в сериализаторе не совпадает с именем атрибута модели.

```python
from rest_framework import serializers

class MyModel(models.Model):
    full_name = models.CharField(max_length=100)

class MySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
```

* `label=None` - Позволяет установить человекочитаемое описание поля, которое может быть использовано при выводе данных.
Оно обычно используется для создания дружественных пользователю меток полей.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(label='Full Name')
```

* `help_text=None` - Предоставляет описание поля, которое будет использовано для предоставления помощи пользователю.
Это полезно для добавления подсказок или объяснений к полям.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(help_text='Enter your full name')
```

* `style=None` - позволяет определить стилизацию поля, такую как форматирование даты или числа.
Это используется для отображения данных в определенном стиле, например, когда нужно форматировать дату в определенном формате.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    birth_date = serializers.DateField(style={'input_type': 'date'})
```

* `error_messages=None` - Позволяет определить пользовательские сообщения об ошибках для конкретного поля.
Это полезно для переопределения стандартных сообщений об ошибках.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'invalid': 'Invalid email format'})
```

* `validators=None` - Позволяет определить список валидаторов, которые будут применяться к полю при десериализации данных.
Валидаторы могут проверять данные на соответствие определенным критериям.

```python
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator

class MySerializer(serializers.Serializer):
    age = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
```

* `allow_null=False` -  Определяет, разрешено ли полю принимать значение None (нулевое значение) при десериализации.
Если `allow_null` установлен в `True`, то поле может быть пустым или иметь значение `None`. Если `False`, поле должно быть обязательно заполнено.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
```

#### Также в определенные поля или сериализатор можно передавать дополнительные параметры:

* `allow_empty` - указывает, разрешены ли пустые значения (например, пустые строки) для поля при десериализации.
Если `allow_empty` установлен в `True`, то пустые значения будут разрешены. Если `False`, то пустые значения будут 
считаться недопустимыми, и возникнет ошибка валидации, если такое значение будет передано при десериализации.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(allow_empty=False)
```

* `instance` - предоставляет экземпляр модели, который используется при обновлении данных через сериализатор.
Если передан instance при вызове сериализатора для десериализации, данные будут обновлены в этом экземпляре модели, 
а не создан новый.
```python
from rest_framework import serializers
from .models import MyModel

instance = MyModel.objects.get(pk=1)
serializer = MySerializer(instance=instance, data={'name': 'New Name'}, partial=True)
```

* `data` - предоставляет входные данные для десериализации через сериализатор.
Это обычно словарь или QueryDict, содержащий данные для обновления или создания экземпляра модели.

```python
from rest_framework import serializers

data = {'name': 'John', 'age': 30}
serializer = MySerializer(data=data)
```


* `partial` - указывает, что входные данные являются частичными обновлениями, и можно обновить только указанные поля.
Если partial установлен в `True`, необязательные поля могут быть пропущены, и они не будут считаться недопустимыми значениями.
```python
from rest_framework import serializers

data = {'name': 'John'}
serializer = MySerializer(data=data, partial=True)
```

* `context` - предоставляет дополнительные данные или контекст, которые могут быть использованы в процессе сериализации или десериализации.
Контекст может быть использован для передачи дополнительной информации из вида (view) или других частей приложения в сериализатор.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    def to_representation(self, instance):
        context_value = self.context.get('custom_value')
        # Дальнейшая обработка данных
```

* `max_length`, `min_length` -  позволяют задать максимальную и минимальную длину для строковых полей.
Это полезно, когда нужно ограничить допустимую длину текста.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
```


### Поля

Код для полей можно посмотреть по пути `venv\Lib\site-packages\rest_framework\fields.py`

* `BooleanField(**params)`: Поле для булевых значений (True/False).


* `CharField(allow_blank=False, trim_whitespace=True, max_length=None, min_length=None, **params)`: Строковое поле.


* `ChoiceField(choices, html_cutoff=None, 
html_cutoff_text='More than {count} items...', allow_blank=False, **params)`: Поле для выбора из предопределенных значений.


* `DateField(format=empty, input_formats=None, **params)`: Поле даты.


* `DateTimeField(format=empty, input_formats=None, default_timezone=None, **params)`: Поле даты и времени.


* `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, **params)`: Поле для чисел с фиксированной точностью.


* `DictField(child=rest_framework.fields._UnvalidatedField(), allow_empty=True, **params)`: Поле для словарей.


* `DurationField(max_value=None, min_value=None, **params)`: Поле для хранения длительности времени.


* `EmailField(**params)`: Поле электронной почты.


* `Field(**params)`: Базовый класс для всех полей, используется в основном для создания своих полей.


* `FileField(max_length=None, allow_empty_file=False, **params)`: Поле для загрузки файлов.


* `FilePathField(path, match=None, recursive=False, allow_files=True,
                 allow_folders=False, required=None, ChoiceField.__init__(**kwargs), **params)`: Поле для выбора файла из заданной директории.


* `FloatField(max_value=None, min_value=None, **params)`: Поле для чисел с плавающей точкой.


* `HiddenField(write_only=True, **params)`: Скрытое поле, не выводится в сериализации.


* `HStoreField(child=rest_framework.fields._UnvalidatedField(), allow_empty=True, **params)`: Поле для хранения данных в формате HStore.


* `IPAddressField(protocol='both', **params)`: Поле для IPv4 или IPv6 адресов.


* `ImageField(FileField.__init__(**kwargs))`: Поле для загрузки изображений.


* `IntegerField(max_value=None, min_value=None, **params)`: Целочисленное поле.


* `JSONField(binary=False, encoder=None, decoder=None, **params)`: Поле для хранения данных в формате JSON.


* `ListField(child=rest_framework.fields._UnvalidatedField(), allow_empty=True, max_length=None, min_length=None, **params)`: Поле для хранения списков.


* `ModelField(model_field, max_length=None, **params)`: Поле для связи с моделью.


* `MultipleChoiceField()`: Поле для выбора из множества предопределенных значений.


* `ReadOnlyField()`: Поле только для чтения, не используется при десериализации.


* `RegexField()`: Поле для данных, соответствующих заданному регулярному выражению.


* `SerializerMethodField()`: Поле, использующее метод сериализатора для получения данных.


* `SlugField()`: Поле для URL-фрагментов.


* `TimeField()`: Поле времени.


* `URLField()`: Поле URL-адреса.


* `UUIDField()`: Поле для хранения уникальных идентификаторов UUID.