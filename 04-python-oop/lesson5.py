class Animal:
    def __init__(self,name):
        self.name=name
    def describe(self):
        print(f"My name is {self.name}!")

class Dog(Animal):
    def __init__(self,name, age):
        super().__init__(name)
        self.age=age
    def describe(self,patern):
        super().describe()
        print(f"...my patern is {patern} and I am a dog!")
    def bark(self):
        print("Woof!")
class Cat(Animal):
    def describe(self):
        print(f"My name is {self.name} and I am a cat!")

dog1=Dog("Buddy",6)
animal1=Animal("Max")
animal1.describe()

dog1.describe("Golden")
print(dog1.age)
dog1.bark()
cat1=Cat("Whiskers")
cat1.describe()