class Error(Exception):
    pass


class ParameterRequiredError(Error):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return "%s is mandatory, but received empty." % (", ".join(self.params))


class ParameterValueError(Error):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return "the enum value %s is invalid." % (", ".join(self.params))


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
