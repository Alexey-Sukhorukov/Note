# string = 'TMS'

# to_find = ['M', 'T', 'S']

# for s in string:
#     if to_find[0] == s:
#        to_find.pop(0)
#     if not to_find:
#         break

# res = 0 if to_find else 1
# print(res)

'''
'''
# connections = [i for i in [1, 2, 3, 4, 6, 0] if i != 0]
# connections = [19, 2, 3]
# connections = [i for i in connections if i != 0]


# while len(connections) > 1:
#     connections.sort(reverse=True)
#     for idx in range(0, len(connections)-1, 2):
#         connections[idx] -= connections[idx + 1]
#         connections[idx + 1] = 0
#         print(connections)
    
#     connections = [conn for conn in connections if conn != 0]
#     print(f'{connections=}')

# if connections:
#     res = connections[0] // 2
# else:
#     res = 0
    
# print(res)
        
x = 998244353


        