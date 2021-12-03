class ConfigError(Exception):
    def __init__(self, value): 
        self.value = value

    def __str__(self):
        return self.value

class BrowserInitError(Exception):
    def __init__(self, value): 
        self.value = value

    def __str__(self):
        return self.value

class XstavkaError(Exception):
    def __init__(self, value): 
        self.value = value

    def __str__(self):
        return self.value

class CssSelectorError(Exception):
    def __init__(self, value): 
        self.value = value

    def __str__(self):
        return self.value