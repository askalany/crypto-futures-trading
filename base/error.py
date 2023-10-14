class Error(Exception):
    pass


class ParameterRequiredError(Error):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return f'{", ".join(self.params)} is mandatory, but received empty.'


class ParameterValueError(Error):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return f'the enum value {", ".join(self.params)} is invalid.'


class ParameterTypeError(Error):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return f"{self.params[0]} data type has to be {self.params[1]}"


class ParameterArgumentError(Error):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return self.error_message
