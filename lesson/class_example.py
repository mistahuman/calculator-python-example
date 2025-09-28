from abc import ABC, abstractmethod
from dataclasses import dataclass

# 1. Class vs Static vs Instance Methods
class MyClass:
    counter = 0
    
    def __init__(self, value):
        self.value = value
        MyClass.counter += 1
    
    def instance_method(self):
        return f"Valore: {self.value}"
    
    @classmethod
    def class_method(cls):
        return f"Istanze create: {cls.counter}"
    
    @staticmethod
    def static_method(x, y):
        return x + y


# 2. Proprietà con @property
class Persona:
    def __init__(self, nome, eta):
        self.nome = nome
        self._eta = eta
    
    @property
    def eta(self):
        return self._eta
    
    @eta.setter
    def eta(self, value):
        if value < 0:
            raise ValueError("Età non può essere negativa")
        self._eta = value


# 3. Metodi speciali
class Vettore:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __repr__(self):
        return f"Vettore({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vettore(self.x + other.x, self.y + other.y)
    
    def __len__(self):
        return abs(self.x) + abs(self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# 4. Ereditarietà e super()
class Animale:
    def __init__(self, nome):
        self.nome = nome
    
    def parla(self):
        return "..."


class Cane(Animale):
    def __init__(self, nome, razza):
        super().__init__(nome)
        self.razza = razza
    
    def parla(self):
        return "Bau!"


# 5. Classi astratte
class Forma(ABC):
    @abstractmethod
    def area(self):
        pass


class Cerchio(Forma):
    def __init__(self, raggio):
        self.r = raggio
    
    def area(self):
        return 3.14 * self.r ** 2


# 6. Singleton
class Singleton:
    _istanza = None
    
    def __new__(cls, *args, **kwargs):
        if cls._istanza is None:
            cls._istanza = super().__new__(cls)
        return cls._istanza


# 7. Metaclassi
class Meta(type):
    def __new__(cls, name, bases, attrs):
        print(f"Creo la classe {name}: {cls}")
        return super().__new__(cls, name, bases, attrs)


class MiaClasse(metaclass=Meta):
    pass


# 8. Dataclass
@dataclass
class Punto:
    x: int
    y: int


# MAIN
if __name__ == "__main__":
    # 1
    a = MyClass(10)
    b = MyClass(20)
    print(a.instance_method())
    print(MyClass.class_method())
    print(MyClass.static_method(3, 4))
    
    # 2
    p = Persona("Luca", 30)
    print(p.eta)
    p.eta = 35
    print(p.eta)
    
    # 3
    v1 = Vettore(1, 2)
    v2 = Vettore(3, 4)
    print(v1 + v2)
    print(len(v1))
    print(v1 == Vettore(1, 2))
    
    # 4
    cane = Cane("Fido", "Labrador")
    print(cane.nome, cane.razza, cane.parla())
    
    # 5
    c = Cerchio(5)
    print("Area cerchio:", c.area())
    
    # 6
    s1 = Singleton()
    s2 = Singleton()
    print("Singleton uguali?", s1 is s2)
    
    # 7
    m = MiaClasse()
    print("Oggetto metaclasse:", m)
    
    # 8
    punto = Punto(2, 3)
    print(punto)
