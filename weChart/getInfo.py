import pickle, json

# 读取
pickle_file = open("itchat.pkl", "rb")
newInfos = pickle.load(pickle_file)
pickle_file.close()

dicts = json.dumps(newInfos)

authDict = newInfos.get("loginInfo").get("User")

NickName = authDict.get("NickName")

Sex = authDict.get("Sex")
print(NickName, Sex)


