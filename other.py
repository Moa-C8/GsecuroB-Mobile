import string
import hashlib
import random
from cryptography.fernet import Fernet
import sqlite3
import os,sys,stat

def random_password(lenght, alpha):
        i = 0
        j = 0
        password = ""
        while i < lenght:
            j = random.randint(0, len(alphabet_plusMoinSpace)-1)
            password += alpha[j]
            i += 1
            
        return password

def getExtension(path):
    i = -1
    ext = ""
    while(path[i] != "."):
        ext += path[i]
        i -= 1
    ext += "."    
    ext = ext[::-1]
    return ext

def getName(path):
    i = -1
    name = ""
    while(path[i] != "/"):
        name += path[i]
        i -= 1
    name = name[::-1]
    return name

def hashPassword(password):
    liste_letter = []
    hash_ = hashlib.sha512(password.encode()).hexdigest()

    i = 0
    mot1 = ""
    mot2 = ""
    for each in hash_:
        liste_letter.append(each)
    while i < 64:
        mot1 += liste_letter[i]
        i += 1
    while i < 128:
        mot2 += liste_letter[i]
        i += 1
    mot1 = hashlib.sha256(mot1.encode('utf-8')).hexdigest()
    mot2 = hashlib.sha256(mot2.encode('utf-8')).hexdigest()
    key = mot2 + mot1
    key = hashlib.sha256(key.encode('utf-8')).hexdigest()
    key.encode('utf-8')
    i = 0
    Lmot = list(key)
    while i < 21:  
        del Lmot[i]
        i += 1
    key = ""
    for each in Lmot:
        key += each
    key += "=" 
    key = key.encode('utf-8')

    return key

def cryptDatabase(key,pathdbc,types,namedb="",mode = ''):
    try:
        f = Fernet(key)
    except:
        return 1
    else:
        if (types=="db"):
            dbFile = open(tempDB, 'rb')
        elif (types=='tx'):
                dbFile = open(tempFile, 'rb')
        else:
            return 1
        contentDbFile = dbFile.read()
        dbFile.close()
        if (namedb != ""):
            pathListed = pathdbc.split('/')
            #print (pathListed)
            if (pathListed[-1] != namedb):
                pathdbc = os.path.join(pathdbc,namedb)
            #print("2",pathdbc)
        if (mode == 'resetP'):
            if os.path.exists(pathdbc):
                os.remove(pathdbc)
        contentDbcFile = f.encrypt(contentDbFile)
        contentDbFile=''
        #os.chmod(pathdbc, stat.S_IRWXU)
        try:
            dbcFile = open(pathdbc, 'wb')
        except:
            return 2
        os.chmod(pathdbc, stat.S_IRWXU)
        dbcFile.write(contentDbcFile)
        dbcFile.close()
        if os.path.exists(tempDB):
            os.remove(tempDB)
        if os.path.exists(tempFile):
            os.remove(tempFile)
        return 0
        

def decryptDatabase(key,pathdbc,type):
    try:
        f = Fernet(key)
    except:
        return False
    dbcFile = open(pathdbc, 'rb')
    contentDbcFile = dbcFile.read()
    dbcFile.close()
    try:
        contentDbFile = f.decrypt(contentDbcFile)
    except:
        return False
    try:
        createTable()
    except:
        return False
    else:
        if (type == "db"):
            dbFile = open(tempDB, 'wb')
        elif (type == "tx"):
                dbFile = open(tempFile, 'wb')
        else:
            return False
        try:
            dbFile.write(contentDbFile)
        except:
            dbFile.close()
            return False
        else:
            dbFile.close()
            return True

def createTable():
        try:
            conn = sqlite3.connect(tempDB)           
        except:
            return 1
        else:
            curs = conn.cursor()
            #create Table
            curs.execute("""CREATE TABLE if not exists customers (
                siteOrApp text,
                email text,
                password text,
                id INTEGER PRIMARY KEY AUTOINCREMENT)
            """)

            #commit changes
            conn.commit()

            conn.close()

def createSeed():
    fil = open(tempFile,"wb")
    fil.close()

def changeSets(part,sets):
    file = open('src/settings.txt')
    cont = file.read()
    file.close()
    listSets = cont.split('\n')

    if part == 0:
        listSets[0] = sets
    elif part == 1:
        listSets[1] = sets

    file = open('src/settings.txt','w+')
    for each in listSets:
        each= f'{each}\n'
        file.write(each)
    file.close()

def readPrimaryColor():
    file = open('src/settings.txt')
    cont = file.read()
    file.close()
    listSets = cont.split('\n')
    return colors[int(listSets[0])]

def readTheme():
    file = open('src/settings.txt')
    cont = file.read()
    file.close()
    listSets = cont.split('\n')
    return listSets[1]

tempDB = 'qwerty.db'
tempFile = 'azerty.txt'

listExt = ['txt','csv','zip','aac','avi','doc','docx','gif','gz','h','htm','ico','iso','jpeg','mkv','mp3','mp4','odt','odp','ods',
'odg','pdf','png','pps','py','rar','tar','torrent','xls','xlsx','wav','xml','bat','bmp','exe','sh']

# Alphabets
alphabet = string.ascii_letters
nombre = string.digits
alphabet_plusMoinSpace =list(string.ascii_letters + string.punctuation + string.digits)
alphabet_plus = list(string.ascii_letters + string.punctuation + string.digits + " ")

colors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue',
           'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 
           'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
themes = ['Dark',"Light"]
ecranPricipal = ['0,3,9,15,5']
