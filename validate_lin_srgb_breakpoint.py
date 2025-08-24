#!/usr/bin/env python
# encoding: utf-8
from decimal import Decimal, getcontext

getcontext().prec = 80

A = Decimal(211) / Decimal(200)   # 1.055
B = Decimal(11)  / Decimal(200)   # 0.055
L = Decimal(323) / Decimal(25)    # 12.92
p = Decimal(5)   / Decimal(12)    # 1/2.4

# Newton's method to solve f(x)=A*x^p - B - L*x = 0
x = Decimal("0.00313")  # initial guess
# x = 0.00313
for _ in range(60):
	f = A*(x**p) - B - L*x
	df = A*p*(x**(p-1)) - L
	x = x - f/df

print(x)
