from queue import LifoQueue
import numpy as np

class BoolVar:
   def __init__(self, value):
      self.value = value

   # '-' — отрицание
   def __neg__(self):
      return BoolVar(not self.value)

   # '+' — дизъюнкция
   def __add__(self, other):
      return BoolVar(self.value or other.value)

   # '*' — конъюнкция
   def __mul__(self, other):
      return BoolVar(self.value and other.value)

   # '>' — импликация
   def __gt__(self, other):
      return BoolVar((not self.value) or other.value)

   # '=' — эквивалентность
   def __eq__(self, other):
      return BoolVar(self.value == other.value)

   # строковое представление значения
   def __str__(self):
      return "True" if self.value else "False"
   
   #объектное представление
   def __format__(self, format_spec):
      return format(str(self), format_spec)

# метод заполнения нулями
def zeros(array):
    for j in range(len(array)-1):
        array[j] = 0
    return array

# метод заполенения единицами
def ones(array):
    for k in range(len(array)):
        array[k] = 1
    return array

# метод формирования СКНФ
def sknf(arr):
    alph, rez = [chr(j) for j in range(65, 65+len(arr))], ''
    for i in range(len(arr)):
        if arr[i] == 0:
            rez += alph[i] + ' v '
        if arr[i] == 1:
            rez += '¬' + alph[i] + ' v '
    return rez[:-2]

# метод формирования СДНФ
def sdnf(arr):
    alph, rez = [chr(j) for j in range(65, 65+len(arr))], ''
    for i in range(len(arr)):
        if arr[i] == 1:
            rez += alph[i] + ' & '
        if arr[i] == 0:
            rez += '¬' + alph[i] + ' & '
    return rez[:-2]

my_stack = LifoQueue()  # создаем стэк
v = input('Введите логическое выражение: ')
v = v.replace("=", "==")  # корректирование ввода
pb = sorted(set([c for c in v if c.isalpha()])) # пропозиционные буквы
m = 2**len(pb)
arr = np.zeros((len(pb), m))  # задаем матрицу n x m
step = 1  # задание шага разбива массивов

# заполенение таблицы истинности размера n x (2^n)
# c помощью разбиения массивы на подмассивы
for i in range(len(pb)):
    step = step * 2
    mass = np.array_split(arr[i], step)
    for j in range(len(mass)):
        my_stack.put(mass[j])
    mass_list = []
    while my_stack.qsize() != 0:
        a = zeros(my_stack.get())
        mass_list.append(a)
        b = ones(my_stack.get())
        mass_list.append(b)
    arr[i] = np.concatenate(mass_list)

vars_for_eval, rez, arr, res1, res2 = {}, [], arr.transpose(), '', ''
#формируем для каждой строки булевое значение логического высказывания
for x in range(m):
   for y, (k, key) in zip(arr[x], reversed(list(enumerate(reversed(pb))))):
      vars_for_eval[key] = BoolVar(y)
   result = eval(v, {}, vars_for_eval)
   rez.append(int(result.value))

#формируем скнф и сднф
for z in range(len(rez)):
   if rez[z] == 0: res1 += '(' + sknf(arr[z]) + ')' + ' & '
   else: res2 += '(' + sdnf(arr[z]) + ')' + ' v '

print(f'CКНФ: {res1[:-2]},\nСДНФ: {res2[:-2]}')