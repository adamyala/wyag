class Maybe:
    def __init__(self, value):
        self._value = value

    def bind(self, func):
        if self._value is None:
            return Maybe(None)
        else:
            return Maybe(func(self._value))

    def orElse(self, default):
        if self._value is None:
            return Maybe(default)
        else:
            return self

    def unwrap(self):
        return self._value

    def __or__(self, other):
        return Maybe(self._value or other._value)

    def __str__(self):
        if self._value is None:
            return "Nothing"
        else:
            return "Just {}".format(self._value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Maybe):
            return self._value == other._value
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __bool__(self):
        return self._value is not None


def add_one(x):
    return x + 1


def double(x):
    return x * 2


result = Maybe(3).bind(add_one).bind(double)
print(result)  # Just 8

result = Maybe(None).bind(add_one).bind(double)
print(result)  # Nothing

result = Maybe(None).bind(add_one).bind(double).orElse(10)
print(result)  # Just 10

result = Maybe(None) | Maybe(1)
print(result)  # Just 1


class State:
    def __init__(self, state):
        self.state = state

    def __call__(self, value):
        return self.state[1], State((self.state[0] + 1, value))


# create a stateful computation that counts the number of times it is called
counter = State((0, 0))

# call the computation multiple times and print the current count
for i in range(5):
    result, counter = counter(i)
    print(f"Computation result: {result}, count: {counter.state[0]}")

# Computation result: 0, count: 1
# Computation result: 0, count: 2
# Computation result: 1, count: 3
# Computation result: 2, count: 4
# Computation result: 3, count: 5


from typing import Any, Callable, TypeVar

T = TypeVar("T")


def reader(f: Callable[[Any], T]) -> Callable[[Any], T]:
    def wrapped(*args):
        return f(*args)

    return wrapped


def greet(name: str) -> str:
    return f"Hello, {name}!"


greet_reader = reader(greet)

# call greet_reader with the name argument
result = greet_reader("Alpha")

print(result)  # output: "Hello, Alpha!"


from typing import Callable, Dict, TypeVar

T = TypeVar("T")


def reader(f: Callable[..., T]) -> Callable[..., T]:
    def wrapped(*args, **kwargs):
        config = kwargs.get("config")
        return f(config, *args)

    return wrapped


@reader
def greet(config: Dict[str, str]) -> str:
    return f"Hi, {config['name']}"


result = greet(config={"name": "Beta"})
print(result)


from typing import Tuple


def writer(value, log):
    return (value, log)


def add(x, y):
    result = x + y
    log = f"Adding {x} and {y} to get {result}.\n"
    return writer(result, log)


def multiply(x, y):
    result = x * y
    log = f"Multiplying {x} and {y} to get {result}.\n"
    return writer(result, log)


# Chain together add and multiply using the Writer monad
add_result, add_log = add(2, 3)
mul_result, mul_log = multiply(add_result, 4)
result = mul_result
log = add_log + mul_log
print(f"Result: {result}")
print(f"Log: {log}")

# result: 20
# log: Adding 2 and 3 to get 5.
# Multiplying 5 and 4 to get 20.


class IO:
    def __init__(self, effect):
        self.effect = effect

    def __call__(self):
        return self.effect()


def read_file(filename):
    def read_file_effect():
        with open(filename, "r") as f:
            return f.read()

    return IO(read_file_effect)


def print_contents(contents):
    def print_effect():
        print(contents)

    return IO(print_effect)


# chain the IO operations manually
contents = read_file("example.txt")()
print_contents(contents)()
