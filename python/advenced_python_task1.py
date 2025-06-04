
import sys
file = "C:\\Users\\berid\\Downloads\\test_txt_file.txt"
with open(file, "r") as file:
    content = file.read()

lst = content.strip().split(" ") 
dicti = [{"word" : lst[0] ,"times" : 1}]
for wrd in lst[1:]:
    enterd = False 
    for i in range(len(dicti)):
        if dicti[i]["word"] ==wrd:
            dicti[i]["times"] +=1
            enterd = True
    if enterd == False:
        dicti.append({"word" : wrd , "times" : 1})
        
sort = sorted(dicti,key=lambda wrd:wrd["times"] , reverse=True)

final = sort[:int(sys.argv[1])]
for i in range(len(final)):
    print(f"the word '{final[i]["word"]}' accured {final[i]["times"]} times")