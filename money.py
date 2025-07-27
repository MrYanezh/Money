# Создать текстовый файл с логом
with open('log.txt', 'w') as log:
    log.write("Начнём считать деньги\n")

# # Спросить какое количество человек платит
l = int(input('Какое количество человек платит?\n'))
with open('log.txt', 'a') as log:
    log.write('Какое количество человек платит?\n')
    log.write(str(l))
    log.write("\n")

# # Спросить имена жертв и записать их в список
list_name = []
for i in range (l):
    a = str(input("Введите имя жертвы \n"))
    list_name.append(a)
with open('log.txt', 'a') as log:
    log.write('Список жертв\n')
    log.write(str(list_name))
    log.write("\n")

# # Спросить сколько заплатил каждый и записать в лог
list_money = []
for i in range (l):
    print("Сколько заплатил ", list_name[i], "?", sep="")
    b = float(input())
    list_money.append(b)
with open('log.txt', 'a') as log:
    log.write('Жертвы заплатили:\n')
    log.write(str(list_money))
    log.write("\nИтого:\n")
    log.write(str(sum(list_money)))
    log.write("\n")

# # Спросить коэффициент каждого и записать в лог
list_coef = []
for i in range (l):
    print("Коэффициент ", list_name[i], "?", sep="")
    c = float(input())
    list_coef.append(c)
with open('log.txt', 'a') as log:
    log.write('Коэффициенты:\n')
    log.write(str(list_coef))
    log.write("\nСуммарный коэффициент:\n")
    log.write(str(sum(list_coef)))
    log.write("\n")

# Для отладки
# l = 4
# list_name = ['Горди', 'Женя', 'Шур', 'Серега']
# list_money = [32868.0, 5947.0, 36403.0, 1430.0]
# list_coef = [2.5, 3.5, 3.0, 1.0]

# Сколько стоит единица нашего коэффициента?
unit = sum(list_money)/sum(list_coef)
unit = round(unit, 2)
with open('log.txt', 'a') as log:
    log.write('Единица коэффициента стоит:\n')
    log.write(str(unit))

# Сколько должен был заплатить каждый?
list_portion = []
for i in range (l):
    d = list_coef[i]*unit
    d = round(d, 2)
    list_portion.append(d)
with open('log.txt', 'a') as log:
    log.write('\nКаждый должен был заплатить:\n')
    log.write(str(list_portion))

# Кто в минусе или плюсе?
list_difference = []
for i in range (l):
    e = list_portion[i]-list_money[i]
    e = round(e, 2)
    list_difference.append(e)
with open('log.txt', 'a') as log:
    log.write('\nРазница у каждого:\n')
    log.write(str(list_difference))
    log.write('\nПроверяем результаты (должен быть 0.0)\n')
    sum_dif = abs(round((sum(list_difference)), 2))
    log.write(str(sum_dif))

# Создаём списки бедных и богатых
positive_balances = [(list_name[i], balance) for i, balance in enumerate(list_difference) if balance > 0]
negative_balances = [(list_name[i], -balance) for i, balance in enumerate(list_difference) if balance < 0]
with open('log.txt', 'a') as log:
    log.write('\nДолжны заплатить:\n')
    log.write(str(positive_balances))
    log.write('\nДолжны получить:\n')
    log.write(str(negative_balances))

# Выбираем кто и кому должен перевести
transfers = []
while positive_balances and negative_balances: # пока существуют
        index_pos, pos_balance = positive_balances.pop() # удаляем последний, запоминая имя и сумму
        index_neg, neg_balance = negative_balances.pop() # удаляем последний, запоминая имя и сумму
        transfer_amount = min(pos_balance, neg_balance) # ищем минимум в удалённых должниках или плательщиках
        transfers.append((index_pos, index_neg, transfer_amount)) # запоминаем индекс плательщика, индекс получателя и сумму (это и есть наш ответ)
        # print(transfers)
        # print(transfer_amount)
        if pos_balance > neg_balance: 
            positive_balances.append((index_pos, pos_balance - neg_balance)) # Если плательщик должен больше чем получатель, то возвращаем его в лист, но с другой суммой (разница)
        elif pos_balance < neg_balance:
            negative_balances.append((index_neg, neg_balance - pos_balance)) # Если получатель больше чем долг, то возвращаем его (плательзика) в лист, но с другой суммой (разница)
with open('log.txt', 'a') as log:
    log.write('\nКто кому переводит:\n')
    log.write(str(transfers)) # вывод в режиме: индекс плательщика, индекс получателя, сумма