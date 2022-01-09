from django.core.validators import MinValueValidator, RegexValidator
from rest_framework.validators import UniqueTogetherValidator


UNVALID_HEX_MESSAGE = ('Неверный формат hex-кода, попробуйте еще раз '
                       '(например, #49B64E)')
ZERO_AMOUNT_MESSAGE = ('Значение не может быть рано 0')
UNIQUE_FAVORITE_MESSAGE = ('Рецепт уже в списке избранных')


class HEXCodeValidator(RegexValidator):
    message = UNVALID_HEX_MESSAGE
    regex = '#[A-Fa-f0-9]{6}$'

class NotZeroValidator(MinValueValidator):
    message = ZERO_AMOUNT_MESSAGE

    def __init__(self) -> None:
        self.limit_value = 0
