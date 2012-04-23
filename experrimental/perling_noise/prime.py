def primes(n):
    """
primes(n) --> primes
Return list of primes from 2 up to but not including n.  Uses Sieve of Erasth.
"""
    if n < 2:
        return []
    nums = range(2,int(n))
    p = []
    while nums:
        new_prime = nums[0]
        p.append(new_prime)
        for i in nums[1:]:
            if i % new_prime == 0:
                nums.remove(i)
        nums.remove(nums[0])
    return p

def power_mod(a, b, n):
    """
power_mod(a,b,n) --> int
Return (a ** b) % n
"""
    if b < 0:
        return 0
    elif b == 0:
        return 1
    elif b % 2 == 0:
        return power_mod(a*a, b/2, n) % n
    else:
        return (a * power_mod(a,b-1,n)) % n
    
def rabin_miller(n, tries = 7):
    """
rabin_miller(n, tries) --> Bool
Return True if n passes Rabin-Miller strong pseudo-prime test on the
given number of tries, which indicates that n has < 4**(-tries) chance of being composite; return False otherwise.
http://mathworld.wolfram.com/Rabin-MillerStrongPseudoprimeTest.html
"""
    if n == 2:
        return True
    
    if n % 2 == 0 or n < 2:
        return False
    
    p = primes(tries**2)
    # necessary because of the test below
    if n in p:
        return True
    
    s = n - 1
    r = 0
    while s % 2 == 0:
        r = r+1
        s = s/2
    for i in range(tries):
        a = p[i]
        
        if power_mod(a,s,n) == 1:
            continue
        else:
            for j in range(0,r):
                if power_mod(a,(2**j)*s, n) == n - 1:
                    break
            else:
                return False
            continue
    return True

print primes(100000)