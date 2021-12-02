"""
    `src/model/parameter.py`
"""

class Parameter:
    def __init__(self, name, value_type=None, description=str()):
        self.name = name
        self.value_type = value_type
        self.description = description
