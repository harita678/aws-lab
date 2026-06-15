class Dog:
    def __init__(self,name,age):
        self.name=name
        self.age = age
    
    def bark(self):
        print(f"{self.name} is barking")

    def birthday(self):
        self.age+=1
        print(f"{self.name} is now {self.age} years old")
    def describe(self):
        print(f"{self.name} is {self.age} years old")
    def two_dogs(self,second_dog):
        print(f" first dog: {self.name} and second dog:{second_dog.name}")
    def compare_age(self,second_dog):
        if self.age > second_dog.age:
            print(f"{self.name} is older than {second_dog.name}")
        elif self.age < second_dog.age:
            print(f"{self.name} is younger than {second_dog.name}")
        else:
            print(f"{self.name} and {second_dog.name} are the same age")

dog1=Dog() 
dog1.bark()
dog1.birthday()
dog1.describe()
dog2=Dog("Max",5)
dog1.two_dogs(dog2)
dog2.two_dogs(dog1)
dog1.compare_age(dog2)
print(dog1.bark)
a=print
print(a)
