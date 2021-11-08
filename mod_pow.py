'''
This computes the result of (base ^ exponent) % modulus for large numbers with
both an iterative and recursive solution. Time complexity is O(logN) where N is
the exponent.
'''

def power_mod(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base ** 2) % modulus
        exponent = exponent // 2
    return result


def power_mod_recursive(base, exponent, modulus):
    if exponent == 0:
        return 1
    base = base % modulus
    result = power_mod_recursive((base ** 2) % modulus, exponent // 2, modulus)
    if exponent % 2 == 1:
        result = (result * base) % modulus
    return result 


if __name__ == '__main__':
    examples = [
        (1223, 4124, 1),
        (1223, 0, 13),
        (2, 3, 5),
        (1231214, 12592198, 12577),
        (2467092835, 1035991785, 149855123)
    ]

    for example in examples:
        print(f'{power_mod(*example)} == {power_mod_recursive(*example)}')
