import string
import hashlib
import random
from cryptography.fernet import Fernet
import sqlite3
import os

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

def cryptDatabase(key,pathdbc,namedb,mode = ''):
    f = Fernet(key)
    dbFile = open(tempDB, 'rb')
    contentDbFile = dbFile.read()
    dbFile.close()
    if (mode == 'resetP'):
        if os.path.exists(os.path.join(pathdbc, namedb)):
            os.remove(os.path.join(pathdbc, namedb))
    contentDbcFile = f.encrypt(contentDbFile)
    contentDbFile=''
    dbcFile = open(os.path.join(pathdbc, namedb), 'wb')
    dbcFile.write(contentDbcFile)
    dbcFile.close()
    if os.path.exists(tempDB):
         os.remove(tempDB)

def decryptDatabase(key,pathdbc):
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
        print("lalal")
    else:
        dbFile = open(tempDB, 'wb')
        dbFile.write(contentDbFile)
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


tempDB = 'qwerty.db'

listExt = ['txt','csv','zip','aac','avi','doc','docx','gif','gz','h','htm','ico','iso','jpeg','mkv','mp3','mp4','odt','odp','ods',
'odg','pdf','png','pps','py','rar','tar','torrent','xls','xlsx','wav','xml','bat','bmp','exe','.sh']

# Alphabets
alphabet = string.ascii_letters
nombre = string.digits
alphabet_plusMoinSpace =list(string.ascii_letters + string.punctuation + string.digits)
alphabet_plus = list(string.ascii_letters + string.punctuation + string.digits + " ")