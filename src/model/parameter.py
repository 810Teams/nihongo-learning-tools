"""
    `src/model/parameter.py`
"""


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
