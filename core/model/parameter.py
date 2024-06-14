"""
    `core/model/parameter.py`
"""

from core.model.argument import Argument
from core.util.logging import error


class Parameter:
    def __init__(self, name: str, value_type: type=None, description: str=str()):
        self.name: str = name
        self.value_type: type = value_type
        self.description: str = description

    def __str__(self) -> str:
        message = '{}'.format(self.name)

        if self.value_type is not None:
            message += ' {}'.format(self.value_type)

        if isinstance(self.description, str) and len(self.description) > 0:
            message += ' : {}'.format(self.description)

        return message

    def validate_argument(self, argument: Argument, display_error: bool=True) -> bool:
        """ Method: Validate argument """
        if self.name != argument.name:
            error('Argument name mismatches parameter name.', display=display_error)
            return False
        if self.value_type is None and argument.value is not None:
            error('Parameter {} does not require value.'.format(self.name), display=display_error)
            return False
        if self.value_type is not None and argument.value is None:
            error('Parameter {} requires value with type {} but none is found.'.format(self.name, self.value_type), display=display_error)
            return False
        if self.value_type is not None and argument.value is not None:
            try:
                self.value_type(argument.value)
            except:
                error('Value of argument {} must be type {}.'.format(argument.name, self.value_type), display=display_error)
                return False

        return True
