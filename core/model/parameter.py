"""
    `core/model/parameter.py`
"""

from typing import Callable

from core.model.argument import Argument
from core.util.logging import error


class Parameter:
    def __init__(
            self,
            name: str,
            value_type: type=None,
            default_value: any=None,
            validation: Callable[[any], bool]=lambda x: True,
            error_message: str=str(),
            description: str=str()
        ):
        self.name: str = name.strip()
        self.value_type: type = value_type
        self.default_value: value_type = default_value
        self.validation: Callable[[any], bool] = validation
        self.error_message: str = error_message.strip()
        self.description: str = description.strip()

    def __str__(self) -> str:
        message = '{}'.format(self.name)

        if self.value_type is not None:
            message += ' {}'.format(self.value_type)

        if isinstance(self.description, str) and len(self.description) > 0:
            message += ' : {}'.format(self.description)

        if self.default_value is not None:
            message += ' (Default: {})'.format(self.default_value)

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

            if not self.validation(self.value_type(argument.value)):
                if isinstance(self.error_message, str) and len(self.error_message) > 0:
                    error(self.error_message, display=display_error)
                else:
                    error('Value validation of argument {} error.'.format(argument.name), display=display_error)
                return False

        return True
