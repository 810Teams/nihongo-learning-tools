"""
    `src/model/parameter.py`
"""

from src.model.argument import Argument


class Parameter:
    def __init__(self, name: str, value_type: type=None, description: str=str()):
        self.name = name
        self.value_type = value_type
        self.description = description

    def __str__(self) -> str:
        message = '{}'.format(self.name)

        if self.value_type is not None:
            message += ' ({})'.format(self.value_type)

        if isinstance(self.description, str) and len(self.description) > 0:
            message += ' : {}'.format(self.description)

        return message

    def validate_argument(self, argument: Argument) -> bool:
        if self.name != argument.name:
            return False
        if self.value_type is None and argument.value is not None:
            return False
        if self.value_type is not None and argument.value is not None:
            try:
                self.value_type(argument.value)
            except:
                return False

        return True
