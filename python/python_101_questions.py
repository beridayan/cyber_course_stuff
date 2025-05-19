def findmax_1(nums):
    max = nums[0]
    for i in range(len(nums)):
        if(nums[i] > max):
            max = nums[i]
    return max

def task_2(nums):
    nums2 = []
    for i in range(len(nums)):
        if nums[i] %2 == 0:
            nums2.append(nums[i])
    return nums2

def up_3(nums):
    start = nums[0]
    for i in range(1,len(nums)):
        if(start >= nums[i]):
            return False
        start = nums[i]
    return True

def reverse_4(str):
    return str[::-1]

def task_5(str):
    count = 0 
    list = ['a','e','i','o','u']
    for char in list:
        if char in str:
            count +=1 
    return count 

def find_longest_words(list):
    lit = []
    max = 0
    for word in list:
        if len(word) == max:
            lit.append(word)
        elif len(word) > max:
            max = len(word)
            lit = []
            lit.append(word)
    return lit

def is_palindrom(str):
    return str == str[::-1]
def find_palindromes(list):
    lit = []
    for word in list:
        if(is_palindrom(word)):
            lit.append(word)
    return lit
##hi
##after push