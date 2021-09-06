import numpy as np

#A
M = np.arange(2,27)
print(M)

#B
M = M.reshape(5,5)
print(M)

#C
i=1
j=1
while(j <= 3):
    i = 1
    while(i <= 3):
        M[i][j] = 0
        i += 1
    j += 1
print(M)

#D
M = M @ M
print(M)

#E
sum = 0
v = M[0]
for i in v:
    sum += i*i
print(np.sqrt(sum))
