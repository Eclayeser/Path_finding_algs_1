#queue = {"A": [0, "-"], "B": [20, "A"]}

#print(queue)
#i,j = queue.pop("A")
#print(i)

test_word = "racecar"

pal = True
while len(test_word) > 1 or pal == False:
    if test_word[0] == test_word[-1]:
        test_word = test_word[1:len(test_word)-1]
        print(test_word)
        pal = True
    else:
        print("not palindrome")
        pal = False
        

if pal:
    print("palindrome")