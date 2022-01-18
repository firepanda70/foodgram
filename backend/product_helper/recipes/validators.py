from django.core.validators import MinValueValidator, RegexValidator

UNVALID_HEX_MESSAGE = ('Неверный формат hex-кода, попробуйте еще раз '
                       '(например, #49B64E)')
ZERO_AMOUNT_MESSAGE = ('Значение не может быть рано 0')


class HEXCodeValidator(RegexValidator):
    message = UNVALID_HEX_MESSAGE
    regex = '#[A-Fa-f0-9]{6}$'


class CookingTimeValidator(MinValueValidator):
    def __init__(self, limit_value=0, message=ZERO_AMOUNT_MESSAGE):
        super().__init__(limit_value, message)
