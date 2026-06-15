class Animal:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def describe(self):
        print(f"my name is {self.name}!")
class Dog(Animal):
    def bark(self):
        print(f"{self.name} is barking and age is {self.age}")
class Cat(Animal):
    def meow(self):
        print(f"{self.name} is meowing and age is {self.age}")
class Bird(Animal):
    def fly(self):
        print(f"{self.name} is flying and age is {self.age}")
dog1=Dog("Buddy",3)
print(dog1.name)
dog1.bark()
bird1=Bird("hidck",1)
bird1.fly()
bird1.bark()
bird1.describe()