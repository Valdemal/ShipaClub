#Валидаторы
from django.core.validators import ValidationError


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Введенное число должно находиться в диапазоне от %(min)s до %(max)s.',
        code='out_of_range',
        params={'min':self.min_value, 'max':self.max_value})


