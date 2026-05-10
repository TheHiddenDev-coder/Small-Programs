class Car:
    def __init__(self, make: str, model: str, year: int, type: str):
        self.make = make
        self.model = model
        self.year = year
        self.type = type


myCar = Car("Land Rover", "Freelander2", 2010, "SUV")
myPrevCar = Car("Mercedes", "C200", 2010, "Limo-ish")
myPrevPrevCar = Car("Audi", "A6", 1234567890, "Sedan-ish")
