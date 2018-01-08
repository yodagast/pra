import os,sys
if(len(sys.argv)<3):
    print("using: python amie.py file1 file2")
f1=sys.argv[1]
f2=sys.argv[2]
print(f1+"\t"+f2)
###文件路径自己设置
DataDir="/home/oem/Documents/PRAResult/rulelearningresults/"


def filter(f=None,filePath="/home/oem/Documents/PRAResult/rulelearningresults/"):
    '''读取单个文件 过滤重复规则
    :param f: 
    :param filePath: 
    :return: 
    '''
    fileName=open(os.path.join(filePath,f),"r")
    d1={}
    tmp={}
    for line in fileName.readlines():
        line = line.replace("\n", "")
        num = 0
        if (line.find("=>") < 1):
            continue
        if (line.find("?b") > 0):
            num = line.rfind("?b")
        key = line[:num + 3].strip()
        val = line[num + 3:].strip()
        if (key in d1.keys() or val in tmp.keys()):
            continue
        d1[key] = val
        tmp[val] = key
    return d1

def write_rule(d,f=None,filePath="/home/oem/Documents/PRAResult/rulelearningresults/"):
    '''
    :param d:
    :param f: 
    :param filePath: 
    :return: 
    '''
    f1=os.path.join(filePath,f)
    print(f1)
    file1 = open(f1, "w")
    print(len(d.keys()))
    for key in d.keys():
        file1.write(key + "\t" + d[key] + "\n")

def intersection(d1,d2,manu="inter"):
    '''
    
    :param d1: 
    :param d2: 
    :param manu: 对字典d1和d2进行集合操作。inter求交集，union求并集合，diff求差集
    :return: 
    '''
    k1 = d1.keys()
    k2 = d2.keys()
    keys = set(k1)
    if(manu=="union"):
        keys=keys.union(k2)
    elif(manu=="inter"):
        keys=keys.intersection(k2)
    elif(manu=="diff"):
        keys=keys.difference(k2)
    print(len(keys))
    f = os.path.join(DataDir, f1 + f2)
    file = open(f, "w")
    for key in keys:
        file.write(key + "\t" + d1.get(key, d2.get(key, "error"))+"\n")
    file.close()

def main():
    '''
    将f1和f2文件中的交集写入f1+f2中
    :return: 
    '''
    d1=filter(f1,DataDir)
    d2=filter(f2,DataDir)
    write_rule(d1,f1+".tmp",DataDir)
    write_rule(d2,f2+".tmp",DataDir)
    intersection(d1,d2)

main()



