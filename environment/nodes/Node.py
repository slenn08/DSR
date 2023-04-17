import numpy as np
import torch
from abc import abstractmethod, ABC


class Node(ABC):
    """
    Abstract class for a node of an equation tree
    """

    def __init__(self, num_children):
        # num_children should be either 0,1,2
        self.num_children = num_children
        self.trig_ancestor = None
        # children are just a list of nodes (which may be empty if num_children == 0)
        self.children = []

    # Need some logic here
    def add_child(self, child):
        if self.remaining_children() > 0:
            self.children.append(child)

    def remaining_children(self):
        return self.num_children-len(self.children)

    def has_trig_ancestor(self):
        return self.trig_ancestor

    def add_trig_ancestor(self):
        self.trig_ancestor = True

    @abstractmethod
    def compute(self):
        """
        So this kinda lends itself to recursive construction of functions but not sure how that will affect speed.
        Maybe it wont actually matter too much? Will need to do some profiling.
        Either way we will just implement it in whatever way makes sense at first and optimise later.
        """
        pass

    @abstractmethod
    def stringify(self):
        """
        So this kinda lends itself to recursive construction of functions but not sure how that will affect speed.
        Maybe it wont actually matter too much? Will need to do some profiling.
        Either way we will just implement it in whatever way makes sense at first and optimise later.
        """
        pass

    @abstractmethod
    def duplicate(self):
        """
        Creates a new instance of it's class
        """
        pass



# Just got a couple of examples here. Not sure if this is the best way to do things so I am open to other
# suggestions on how to structure this.
class Add(Node):
    def __init__(self, num_children: int = 2):
        super().__init__(num_children)
        self.trig_ancestor = False

    def compute(self):
        return self.children[0].compute() + self.children[1].compute()

    def stringify(self):
        return self.children[0].stringify() + " + " + self.children[1].stringify()

    def duplicate(self):
        return Add()


class Sub(Node):
    def __init__(self, num_children: int = 2):
        super().__init__(num_children)
        self.trig_ancestor = False

    def compute(self):
        return self.children[0].compute() - self.children[1].compute()

    def stringify(self):
        return self.children[0].stringify() + " - " + self.children[1].stringify()

    def duplicate(self):
        return Sub()


class Mult(Node):
    def __init__(self, num_children: int = 2):
        super().__init__(num_children)
        self.trig_ancestor = False

    def compute(self):
        return self.children[0].compute() / self.children[1].compute()

    def stringify(self):
        return self.children[0].stringify() + " * " + self.children[1].stringify()

    def duplicate(self):
        return Mult()

class Div(Node):
    def __init__(self, num_children: int = 2):
        super().__init__(num_children)
        self.trig_ancestor = False

    def compute(self):
        return self.children[0].compute() / self.children[1].compute()

    def stringify(self):
        return self.children[0].stringify() + " / " + self.children[1].stringify()

    def duplicate(self):
        return Div()

class Sin(Node):
    def __init__(self, num_children: int = 1):
        super().__init__(num_children)
        self.trig_ancestor = True

    def compute(self):
        return torch.sin(self.children[0].compute())

    def stringify(self):
        return "sin(" + self.children[0].stringify() + ")"

    def duplicate(self):
        return Sin()


class Cos(Node):
    def __init__(self, num_children: int = 1):
        super().__init__(num_children)
        self.trig_ancestor = True

    def compute(self):
        return torch.cos(self.children[0].compute())

    def stringify(self):
        return "cos(" + self.children[0].stringify() + ")"

    def duplicate(self):
        return Cos()

class Log(Node):
    def __init__(self, num_children: int = 1):
        super().__init__(num_children)
        self.trig_ancestor = False

    def compute(self):
        return torch.log(self.children[0].compute())

    def stringify(self):
        return "log(" + self.children[0].stringify() + ")"

    def duplicate(self):
        return Log()

class Exp(Node):
    def __init__(self, num_children: int = 1):
        super().__init__(num_children)
        self.trig_ancestor = False

    def compute(self):
        return torch.exp(self.children[0].compute())

    def stringify(self):
        return "exp(" + self.children[0].stringify() + ")"

    def duplicate(self):
        return Exp()

class X(Node):
    def __init__(self, num_children: int = 0, value: torch.Tensor = torch.zeros(1)):
        super().__init__(num_children)
        self.value = value
        self.trig_ancestor = False

    def set_value(self, value: torch.Tensor):
        self.value = value

    def compute(self):
        return self.value

    def stringify(self):
        return "x"

    def duplicate(self):
        return X(self.value)

class Y(Node):
    def __init__(self, num_children: int = 0, value: torch.Tensor = torch.zeros(1)):
        super().__init__(num_children)
        self.value = value
        self.trig_ancestor = False

    def set_value(self, value: torch.Tensor):
        self.value = value

    def compute(self):
        return self.value

    def stringify(self):
        return "y"

    def duplicate(self):
        return Y(self.value)

class Const(Node):
    def __init__(self, num_children: int = 0, value: float = 0):
        super().__init__(num_children)
        self.value = value
        self.trig_ancestor = False

    def compute(self):
        return self.value

    def stringify(self):
        return str(self.value)

    def duplicate(self):
        return Const(self.value)

# def BasicTest():
#     y = Add(2)
#     a = X(value=torch.rand(2, 2, requires_grad=True, dtype=torch.float))
#     b = Y(value=torch.rand(2, 2, requires_grad=True, dtype=torch.float))
#     c = Sin()
#     c.add_child(b)
#     y.add_child(a)
#     y.add_child(c)
#     print(y.stringify())


# BasicTest()
