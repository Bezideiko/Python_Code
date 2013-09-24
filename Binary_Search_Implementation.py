lowerBound = balance/12.0
upperBound = balance *((1 + annualInterestRate/12.0)**12)
month = 0
epsilon = 0.01
originalBalance = balance
while abs(balance) > epsilon:
    monthlyPayment = (lowerBound + upperBound)/2.0
    month = 0
    balance = originalBalance
    while month <= 11:
        balance = (balance - ((lowerBound + upperBound)/2.0))* (1 + annualInterestRate/12)
        month = month + 1
    if balance > 0:
        lowerBound = monthlyPayment
    else:
        upperBound = monthlyPayment
print ('Lowest Payment: ' + str (round(monthlyPayment, 2)))