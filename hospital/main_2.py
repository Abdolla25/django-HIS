

class human():
    def __init__(self, name, age, weight, hight):
        self.name = name
        self.age = age
        self.weight = weight
        self.hight = hight

    def get_BMI(self):
        BMI = self.weight / (self.hight**2)
        return BMI

    def __str__(self) -> str:
        return self.name