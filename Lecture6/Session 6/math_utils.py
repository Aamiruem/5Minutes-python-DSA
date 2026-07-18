def factorial(n):
  try:
    if n < 0:
        raise ValueError('Negative numbers have no factorial')
    return 1 if n == 0 else n * factorial(n - 1)

  except ValueError as err:
    print('Invalid input:', err)
    
print(factorial(5))  # Output: 120

def is_prime(n):
    if n <= 1:
        return False     
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

print(is_prime(11))  # Output: True
