import math

def distance(point1, point2):
    return math.sqrt( (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 )

print(distance((0,0), (9,40)))


a = 542.09
b = 655.73
c = 140.66

def calc_angle(a,b,c):
    b1 = b**2
    c1 = c**2
    a1 = a**2

    lower = 2*b*c
    inner = (b1 + c1 - a1)/lower
    return math.degrees(math.acos(inner))

def magnitude(vec):
    return math.sqrt(sum([i**2 for i in vec]))

print("TEST", math.degrees(calc_angle(a,b,c)))

A_B = [2, 0, -2]
B_C = [-2, -1, 0]
B_C = B_C[::-1]

dot_prod = sum(p * q for p, q in zip(A_B, B_C))
print(dot_prod)
print(magnitude(A_B))
print(magnitude(B_C))






#calc_angle(a,b,c)

