class Variable:
    """A config variable
    """
    def __init__(self, name, default, description, type):
        # Variable name, used as key in yaml, or to get variable via command line and env varaibles 
        self.name = name

        # Description of the variable, used for --help
        self.description = description

        # Type of the variable, can be int, float, str, list
        self.type = type

        # The value of the variable
        self._value = None
        self.set_value(default)

    def get_value(self):
        return self._value

    def set_value(self, value):
        """Check if the value match the type of the variable and set it
        
        Args:
            value: The new value of the variable, will be checked before updating the var 
        
        Raises:
            TypeError: if the type of value doesn't matche the type of the variable
        """

        if self.type != str and type(value) == str:
            # Try to convert
            if self.type in [int, float]:
                value = float(value)

        if self.type == int:
            # In the special case value is a int encoded in float, should convert it before loading
            if int(value) == value:
                value = int(value)

        if type(value) == self.type:
            self._value = value
        else:
            raise TypeError("value should have type {} but have type {}".format(self.type, type(value)))
