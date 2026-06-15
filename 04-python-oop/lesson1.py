class Dog:
    pass

do1 = Dog()
do2 = Dog()

print(do1)
print(do2)
print(do1 == do2)
print(type(do1))

class Cat:
    def __init__(self,name,age):
        self.name=name
        self.age=age

cat1=Cat("Tom",3)
cat2=cat1
cat3=Cat()

print(cat2.name)
cat1.name="Kitty"
print(cat2==cat1)
print(cat3)

