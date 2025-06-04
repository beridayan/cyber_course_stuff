
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

names = []
for i in range (len(sort)):
    names.append(sort[i]["word"])
print (names[1:sys.argv[1]])