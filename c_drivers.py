import json


f= open("json/drivers_2018.json","r")
d_22 = json.load(f)

print(d_22["response"][1])
# for piloto in d_22["response"]:
#     print(piloto[1])




