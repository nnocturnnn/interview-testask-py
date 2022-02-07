


old_list = [6, 7, 9, 4, 2, 1 ] 

def is_even_plus_two(one_list:list) -> list:
  new_list = [i + 2 for i in one_list if i % 2 == 0]
  return new_list 


class Car:
  def __init__(self, name, number):
    self.name = name
    self.number = number


class BMV(Car):
  def __init__(self, name, number, ar):
    super().__init__(name, number)
    self.ar = ar

  def __str__(self):
      return f"Car: {self.name}\nNum: {self.number}\nAr: {self.ar}"