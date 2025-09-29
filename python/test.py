# import timeit

# start = timeit.default_timer()

# #Your statements here

# stop = timeit.default_timer()

# print('Time: ', stop - start) 

# myArray = [170, 45, 75, 90, 802, 24, 2, 66]#aqui o valor de maior prioridade é 3 porque é o maior e o menor é 1
# print("Original array:", myArray)
# radixArray = [[], [], [], [], [], [], [], [], [], []]
# maxVal = max(myArray)
# exp = 1

# while maxVal // exp > 0:
#     while len(myArray) > 0:
#         val = myArray.pop()
#         radixIndex = (val // exp) % 10
#         radixArray[radixIndex].append(val)

#     for bucket in radixArray:
#         while len(bucket) > 0:
#             val = bucket.pop()
#             myArray.append(val)

#     exp *= 10

# print("Sorted array:", myArray)

# import random
# import string

# def gere_codigo_produto() -> str:
#     letters = "".join(random.choice(string.ascii_letters) for _ in range(2))
#     digits = "".join(random.choice(string.digits) for _ in range(4))
#     return f"{letters}-{digits}"

# def gere_codigo_ordem() -> str:
#     letters = "".join(random.choice(string.ascii_letters) for _ in range(3))
#     digits = "".join(random.choice(string.digits) for _ range(3))
#     return f"{digits}-{letters}"

p = 3
for i in range(3):
    print(i // p)
    print(i % p)
