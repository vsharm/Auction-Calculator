from __future__ import print_function
import re
import csv

transactions = {}
current_owner = ""
next_is_owner = True
current_amount = False
financial_transactions = open("financial_transactions.txt", "r")
for i in financial_transactions:
  if 'Current Amount' in i:
    transactions[current_owner] = (int(re.search("\d+", i).group()), transactions[current_owner][1])

  if next_is_owner: # owner line
    current_owner = i.rstrip().replace(":", "")
    start_money = next(financial_transactions)
    transactions[current_owner] = (0, [])
    next_is_owner = False
    current_amount = True
  elif len(i.rstrip()) == 0: # empty line
    next_is_owner = True

  if len(i.rstrip()) != 0:
    transactions[current_owner][1].append(i.rstrip())
  if current_amount:
    transactions[current_owner][1].append(start_money.rstrip())
    current_amount = False

with open('input.csv', 'rb') as csvfile:
    input_file = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in input_file:
        owner = row[0]
        player = row[1]
        price = int(row[-1])
        print(owner, player, price)
        (amount, history) = transactions[owner]
        amount = amount - price
        history[-1] = "Current Amount: $" + str(amount)
        history.insert(-1, "-$" + str(price) + " " + player)
        transactions[owner] = (amount, history)

print(transactions)

with open('financial_transactions.txt', 'w') as f:
  for i in transactions:
    (amount, history) = transactions[i]
    for trans in history:
      print(trans)
      print(trans, file=f)
    print("")
    print("", file=f)
