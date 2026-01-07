class Mode:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, owner):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value not in ("clip", "error"):
            raise ValueError("Mode type can only be 'clip' or 'error'")
        else:
            obj.__dict__[self.name] = value

class LimitArgs:

    mode = Mode("mode")
    
    def __init__(self, max_value: int, mode):
        if max_value <= 0:
            raise ValueError("Max value must be >= 0")
        else:
            self.max_value = max_value
        
        self.mode = mode

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            args = self._check_args(*args)
            kwargs = self._check_kwargs(**kwargs)

            return func(*args, **kwargs)

        return wrapper

    def _check_args(self, *args):
        args = list(args)

        for i, arg in enumerate(args):
            if self.mode == "error" and arg > self.max_value:
                raise ValueError(f"Function argument max value must be <= {self.max_value}") 
            elif self.mode == "clip" and arg > self.max_value:
                args[i] = self.max_value 
                
        return tuple(args)

    def _check_kwargs(self, **kwargs):
        for key, value in list(kwargs.items()):
            if value > self.max_value:
                if self.mode == "error":
                    raise ValueError(
                            f"Function argument '{key}' max value must be <= {self.max_value}"
                    )
                elif self.mode == "clip":
                    kwargs[key] == self.max_value

        return kwargs

@LimitArgs(10, "clip")
def multiply(a, b):
    return a * b

print(multiply(2, 3))
print(multiply(100, 3))
