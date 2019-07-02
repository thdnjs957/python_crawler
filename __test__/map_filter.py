a = [1, 2, 3, 4]

# def f(x):
#     return x**2

# map(f, [1, 2, 3, 4])

it = map(lambda x: print(x, sep=' '), [1, 2, 3, 4])  # map은 iter 객체를 반환한다 그래서 돌면서 실행시켜줘야함
next(it)
next(it)
next(it)
next(it)

# map만 가지고는 안됨 return 값을 받아서 뭔가 하는애가 필요
# 그래서 list에 담는다
print('========================================')
lst = list(map(lambda x: x**2, [1, 2, 3, 4]))

print(lst)

print('========================================')

list(map(lambda x: print(x, end=' '), [1, 2, 3, 4]))

# filter
lst = list(filter(lambda x : x % 2 == 0, [1, 2, 3, 4]))
print(lst)
