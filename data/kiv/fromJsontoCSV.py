import json

file = json.load(open("output_merged.json"))

dic = {}

for i in file:
    for j in file[i]:
        dic[j] = i

f = open('data.csv', 'w')
f.write("doi,autor,pocet_citaci,pocet_autoru,pocet_instituci\n")

for i in dic:
    f.write("{0},{1},,\n".format(i, dic[i]))

f.close()
