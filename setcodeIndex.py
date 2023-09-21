import PySimpleGUI as sg

def readSetCodes():
    try:
        f = open('setcode_ocg.txt')
        datalist = f.readlines()
    except Exception as e:
        #print(e)
        return {"setcode_ocg.txt読取失敗":0}
    else:
        list={}
        for data in datalist:
            data=data.split(" ")
            setcode=data[0]
            num=data[1]
            list[setcode]=num
        f.close()
        if len(list)==0:
            return {"setcode_ocg.txt読取失敗":0}
        else:
            return list

def createSetcodeTxt(path):
    try:
        conf = open(path,encoding="UTF-8")
        datalist = conf.readlines()
    except Exception as e:
        #print(e)
        sg.popup("confファイルが開けませんでした。")
    else:
        s=open('setcode_ocg.txt', 'w')
        for data in datalist:
            #print(data)
            if data.startswith("!setname"):
                data=data.split()
                dec=int(data[1],16)
                setcode=data[2].rstrip()
                if len(data)>3:
                    for i in range(3,len(data)):
                        setcode+=" "+data[i].rstrip()
                s.write(str(setcode)+" "+str(dec)+"\n")
        conf.close()
        s.close()

def readOricaSetCodes():
    try:
        f = open('setcode_orica.txt')
        datalist = f.readlines()
    except Exception as e:
        #print(e)
        return {"setcode_orica.txt読取失敗":0}
    else:
        list={}
        for data in datalist:
            data=data.split(" ")
            setcode=data[0]
            num=data[1]
            list[setcode]=num
        f.close()
        if len(list)==0:
            return {"setcode_orica.txt読取失敗":0}
        else:
            return list

def createOricaSetcodeTxt(path):
    try:
        conf = open(path,encoding="UTF-8")
        datalist = conf.readlines()
    except Exception as e:
        #print(e)
        sg.popup("confファイルが開けませんでした。")
    else:
        s=open('setcode_orica.txt', 'w')
        for data in datalist:
            #print(data)
            if data.startswith("!setname"):
                data=data.split()
                dec=int(data[1],16)
                setcode=data[2].rstrip()
                if len(data)>3:
                    for i in range(3,len(data)):
                        setcode+=" "+data[i].rstrip()
                s.write(str(setcode)+" "+str(dec)+"\n")
        conf.close()
        s.close()