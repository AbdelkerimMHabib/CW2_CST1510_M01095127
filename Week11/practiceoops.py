class Car:
    def __init__(self, make, year, model, fuel_type):
        self.__make = make
        self.__year = year
        self.__model = model
        self.__fuel_type = fuel_type

    # Accessor methods
    def get_make(self):
        return self.__make

    def get_year(self):
        return self.__year

    def get_model(self):
        return self.__model

    def get_fuel_type(self):
        return self.__fuel_type
    

car1 = Car("Audi", 2020, "A4", "Petrol")
car2 = Car("Volvo", 2021, "S60", "Diesel")
car3 = Car("BMW", 2022, "X3", "Electric")

print(car1.get_make())    
print(car2.get_year())   
print(car3.get_model())   


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def bark(self):
        return "Woof!"

# Create an instance of Dog
dog = Dog("Rex", 5, "Labrador")
print(dog.bark())  

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def get_info(self):
        return f"{self.name} is a {self.age} year old {self.breed}"
