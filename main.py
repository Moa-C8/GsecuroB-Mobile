from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex


from plyer import filechooser
from plyer import notification

from kivymd.uix.button import MDFloatingActionButton
from kivymd.app import MDApp
from kivymd.uix.templates import RotateWidget
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager

import sqlite3
from other import *
import string
import hashlib
import random
import cryptography
import os
import shutil
import mimetypes

mimetypes.add_type('text/plain', '.txt')
mimetypes.add_type('application/octet-stream', '.dbc')

Upath = ''
if ( platform == 'android' ):
    Upath = '/storage/emulated/0/'
    

elif(platform == 'linux'):
    Upath = '/home/moa'
    
else:
    Upath = '/'


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class RootButton(MDFloatingActionButton, RotateWidget):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class AskPassword(FloatLayout):
    submit = ObjectProperty(None)
    path = StringProperty()
    filename = StringProperty()

class AskName(FloatLayout):
    submit = ObjectProperty(None)
    path = StringProperty()
    filename = StringProperty()

class GenPassword(FloatLayout):
    submit = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def genPassword(self,lent):
        lent = int(lent)
        if (lent < 14):
            return
        password = random_password(lent,alphabet_plus )
        self.ids.passwordgen.text = ''
        self.ids.passwordgen.text = password
    
    def clipboard(self,password):
        Clipboard.copy(password)
        if (platform != 'android'):
            toast(text='password copied',duration=1)

    

class MenuScreen(Screen):
    btn_visible = False
    duration = 0.1

    #Animation button
    def do_anim_show_btn_PassMan(self, *args):
        anim = Animation(
            y=dp(50) + dp(60),
            t="out_circ",
            d = self.duration,
            )
        
        anim &= Animation(
            x=(self.center_x - self.ids.btnPm.width /2) + dp(80),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnPm)
    
    def do_anim_hide_btn_PassMan(self, *args):
        anim = Animation(
            y=dp(50),
            t="out_circ",
            d = self.duration,
            )
        
        anim &= Animation(
            x=self.center_x - self.ids.btnPm.width /2,
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnPm)

    def do_anim_show_btn_SeedPhrase(self, *args):
        anim = Animation(
            y=dp(50) + dp(60),
            t="out_circ",
            d = self.duration,
            )
        
        anim &= Animation(
            x=(self.center_x - self.ids.btnSeedPhrase.width /2) - dp(80),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnSeedPhrase)
    
    def do_anim_hide_btn_SeedPhrase(self, *args):
        anim = Animation(
            y=dp(50),
            t="out_circ",
            d = self.duration,
            )
        
        anim &= Animation(
            x=self.center_x - self.ids.btnSeedPhrase.width /2,
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnSeedPhrase)

    def do_anim_show_btn_Blockchain(self, *args):
        anim = Animation(
            y=dp(50) + dp(120),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnBlockChain)
           
    def do_anim_hide_btn_Blockchain(self, *args):
        anim = Animation(
            y=dp(50),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnBlockChain)

        
    def anim_btn(self) -> None:
        Animation(rotate_value_angle=90 if not self.btn_visible else 0, d=0.1
                  ).start(self.ids.btn_root_menu)
        self.btn_visible = not self.btn_visible

        if self.btn_visible:
            Clock.schedule_once(self.do_anim_show_btn_SeedPhrase)
            Clock.schedule_once(self.do_anim_show_btn_Blockchain, 0.05)
            Clock.schedule_once(self.do_anim_show_btn_PassMan, 0.1)
              
        else:
            Clock.schedule_once(self.do_anim_hide_btn_SeedPhrase)
            Clock.schedule_once(self.do_anim_hide_btn_Blockchain, 0.05)
            Clock.schedule_once(self.do_anim_hide_btn_PassMan, 0.1)
            
            
    def WaitPopup(self):
        toast("Wait ...")

    #redefinission de taille ou chargement de la page
    def on_size(self, *args):
        if self.btn_visible:
            self.anim_btn()


class PMScreen(Screen):
    btn_visible = False
    duration = 0.1
    Factory.register('LoadDialog', cls=LoadDialog)
    Factory.register('SaveDialog', cls=SaveDialog)

    #Animation button
    def do_anim_show_btn_menu(self, *args):
        anim = Animation(
            x=dp(20) + dp(70),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnMenu)
    
    def do_anim_hide_btn_menu(self, *args):
        anim = Animation(
            x=dp(20),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnMenu)

    def do_anim_show_btn_createdb(self, *args):
        anim = Animation(
            x=dp(20) + dp(140),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnCreateData)
    
    def do_anim_hide_btn_createdb(self, *args):
        anim = Animation(
            x=dp(20),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnCreateData)

    def do_anim_show_btn_passwordGen(self, *args):
        anim = Animation(
            x=dp(20) + dp(210),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnPss)
    
    def do_anim_hide_btn_passwordGen(self, *args):
        anim = Animation(
            x=dp(20),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnPss)

    def do_anim_show_btn_save(self, *args):
        anim = Animation(
            x=dp(20) + dp(280),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnSaveData)
    
    def do_anim_hide_btn_save(self, *args):
        anim = Animation(
            x=dp(20),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnSaveData)

    def anim_btn(self) -> None:
        Animation(rotate_value_angle=90 if not self.btn_visible else 0, d=0.1
                  ).start(self.ids.btn_root_pm)
        self.btn_visible = not self.btn_visible

        if self.btn_visible:
            Clock.schedule_once(self.do_anim_show_btn_menu)
            Clock.schedule_once(self.do_anim_show_btn_createdb, 0.05)
            Clock.schedule_once(self.do_anim_show_btn_passwordGen, 0.1)
            Clock.schedule_once(self.do_anim_show_btn_save, 0.15)
        else:
            Clock.schedule_once(self.do_anim_hide_btn_menu)
            Clock.schedule_once(self.do_anim_hide_btn_createdb, 0.05)
            Clock.schedule_once(self.do_anim_hide_btn_passwordGen, 0.1)
            Clock.schedule_once(self.do_anim_hide_btn_save, 0.1)
       
    def dismiss_popup(self):
        self._popup.dismiss()

    def loadfile_manager_open(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_loadpath
            #ext=['.dbc']
        )
        self.file_manager.show(Upath) # Le répertoire racine
        
    def select_loadpath(self, path):
        if os.path.isdir(path):
            #print('Répertoire sélectionné :', path)
            contents = os.listdir(path)
        else:
            #print('Fichier sélectionné :', path)
            self.load(path)
        self.exit_manager()
    
    def exit_manager(self, *args):
        '''Cette méthode est appelée lorsque l'utilisateur ferme le gestionnaire de fichiers.'''
        self.file_manager.close()


    def load(self, path):
        #print(path)
        name = getName(path)
        ext = getExtension(name)

        self.data = [path,name]
        #self.dismiss_popup()
        self.ids.browseDatabaseBtn.text = 'Browsed'
    
    def openDbcToTable(self):
        if (self.ids.openTreeviewBtn.text != 'Open'):
            toast("Close this one before")
            return
        password = self.ids.mainPassword.text
        if(len(password)>99):
            toast("Lenght 99 chars max")
            return
        key = hashPassword(password)
        password = ''
        dcrypt = decryptDatabase(key,self.data[0],'db')
        if (not dcrypt):
            toast("Wrong file or password")
            return

        self.ids.openTreeviewBtn.text = 'Opened'
        self.ids.labelopenedManager.text = f'Manager open : {self.data[1]}'
        self.querryDataBase()

    def savefile_manager_open(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.askPasswordDbc
        )
        self.file_manager.show(Upath) # Le répertoire racine
   
    def askPasswordDbc(self,path):
        content = AskPassword(submit=self.save,path=path)
        self._popup = Popup(title="Password", content=content,
                            size_hint=(0.6, 0.33),pos_hint={'top':0.8})
        self._popup.open()
        self.exit_manager()

    def save(self,path,filename,password):
        if (len(password) < 14):
            toast("lenght 14 chars min")
            return
            
        if ('.dbc' not in filename):
            filename = f'{filename}.dbc'
            createTable()
        try:
            self.dismiss_popup()
        except:
            pass
        key = hashPassword(password)
        crypt = cryptDatabase(key=key,pathdbc=path,namedb=filename,mode=self.mode,types='db')
        #print("1",key,path,filename,self.mode)
        if (crypt == 1):
            toast("Wrong file/password")
            return
        elif (crypt == 2):
            toast("Wrong name file")
            return
        else:
            if (self.mode == 'resetN'):
                if os.path.exists(os.path.join(self.data[0],self.data[1])):
                    os.remove(os.path.join(self.data[0],self.data[1]))
            if (self.mode == 'resetN' or self.mode == 'resetP'):
                self.Exit()
            try:
                self.dismiss_popup()
            except: pass
            finally: toast("Created")
            

    def PassworGenPopup(self):
        content = GenPassword(submit=self.genPassword, cancel=self.dismiss_popup)
        popup = Popup(title=f'Password Generator', content=content,
              auto_dismiss=True, size_hint=(0.7, 0.3),pos_hint={'top':0.7})
        popup.open()

    def clearBoxes(self):
        self.ids.name_field.text = ''
        self.ids.id_field.text = ''
        self.ids.password_field.text = ''

    def saveAndExitData(self):
        self.clearBoxes()
        self.ids.browseDatabaseBtn.text = 'Browse'
        if os.path.exists(self.data[0]):
            os.remove(self.data[0])
        
        self.save(self.data[0], self.data[1],self.ids.mainPassword.text)
        self.ids.mainPassword.text = ''
        self.ids.openTreeviewBtn.text = 'Open'
        self.ids.labelopenedManager.text = "Manager open :"
        if os.path.exists(tempDB):
            os.remove(tempDB)
        self.updateDatble()
        self.data = []

    def Exit(self):
        self.clearBoxes()
        self.ids.browseDatabaseBtn.text = 'Browse'
        self.ids.mainPassword.text = ''
        self.ids.openTreeviewBtn.text = 'Open'
        self.ids.labelopenedManager.text = "Manager open :"
        if os.path.exists(tempDB):
            os.remove(tempDB)
        self.updateDatble()
        self.data = []

    mode = ''
    def changePasswordMain(self):
        if (self.ids.openTreeviewBtn.text == 'Open'):
            self.errorFilePopup(["Database", "need to browse \n and unlock manager"])
            return
        self.mode = 'resetP'
        self.askPasswordDbc(self.data[0],self.data[1])

    def askNameDbc(self,path,filename):
        self.dismiss_popup()
        if (filename == '' or filename == ' '):
            return
        content = AskName(submit=self.save,path=path,filename=filename)
        self._popup = Popup(title="Name", content=content,
                            size_hint=(0.6, 0.25),pos_hint={'top':0.8})
        self._popup.open()

    def changeNameDbc(self):
        if (self.ids.openTreeviewBtn.text == 'Open'):
            self.errorFilePopup(["Database", "need to browse \n and unlock manager"])
            return
        self.mode = 'resetN'
        self.askNameDbc(self.data[0],self.ids.mainPassword.text)

# Tables et database
    # Tables
    def tables(self, records=[]):
        
        listone = []
        
        if (records != ""):
            for record in records:
                listtwo = []
                for object in record:
                    listtwo.append(object)
                del listtwo[0]
                listone.append(listtwo)
        
        self.table = MDDataTable(
            pos_hint = {'center_x': 0.5},
            y=("100dp"),
            size_hint=(0.9,0.5),
            check = True,
            #use_pagination = True,
            rows_num = 999,
            #pagination_menu_height = '60dp',

            background_color = [1,0,0],
            column_data = [
                ("Site/App", dp(35)),
                ("Id/Mail", dp(35)),
                ("Password", dp(45)),
                ("No.", dp(10))
            ],
            
            row_data = listone

        )
        self.table.bind(on_check_press=self.checked)
        self.table.bind(on_row_press=self.row_press)

        self.add_widget(self.table)
        return self

    def updateDatble(self, records=[]):
        self.remove_widget(self.table)
        self.tables(records)

    listRow = []
    def checked(self, table, row):

        if (row in self.listRow):
            self.listRow.remove(row)
        else:
            self.listRow.append(row)
      
    def row_press(self, table, row):
        row_num = int(row.index/len(table.column_data))
        #print(row.index,len(table.column_data),row.index/len(table.column_data),row)
        row_data = table.row_data[row_num]
        passData = row_data[2]
        self.ids.name_field.text = row_data[0]
        self.ids.id_field.text = row_data[1]
        self.ids.password_field.text = row_data[2]
        Clipboard.copy(passData)
        if(platform != 'android'):
            toast("password copied")
          
    # Records

    def addRecord(self):
        #update database
        if (self.ids.name_field.text == '' or self.ids.id_field.text== '' or self.ids.password_field.text == ''):
            toast("fill Name field")
            return

        try:
            conn = sqlite3.connect(tempDB)
        except:
            pass
        else:
            c = conn.cursor()

            #add new record

            request1 = "INSERT INTO customers (siteOrApp, email, password) values (?, ?, ?) "

            c.execute(request1,(self.ids.name_field.text, self.ids.id_field.text, self.ids.password_field.text))

            conn.commit()
            conn.close()

            self.clearBoxes()

            #clear the treeview table

            self.querryDataBase() 

    def querryDataBase(self):
        try:
            conn = sqlite3.connect(tempDB)
        except:
            return
        else:
            curs = conn.cursor()
            try:
                curs.execute('SELECT rowid, * FROM customers')
            except:
                toast("Probably Seed File")
                self.ids.browseDatabaseBtn.text = 'Browse'
                return
            else:
                records = curs.fetchall()

                self.tables(records)

                conn.commit()
                conn.close()

    def removeRecordSelected(self):
        listId = []
        for rows in self.listRow:
            listId.append(rows[3])
        try:
            conn = sqlite3.connect(tempDB)
        except:
            return
        else: 
            c = conn.cursor()

            c.executemany("DELETE FROM customers WHERE id = ?", [(a,) for a in listId])

            #Delete From Database
            c.execute("")

            conn.commit()
            conn.close()

            self.clearBoxes()
            self.querryDataBase()
            Clipboard.copy('')

    def updateRecordSelected(self):
            if len(self.listRow) == 1:
                row = self.listRow[0]
                record_id = row[3]
                try:
                    conn = sqlite3.connect(tempDB)
                except:
                    #print("no connection")
                    return
                else:
                    site_app = row[0]
                    id_mail = row[1]
                    password = row[2]
                    c = conn.cursor()
                    if (self.ids.name_field.text != ""):
                        site_app = self.ids.name_field.text

                    if (self.ids.id_field.text != ""):
                        id_mail = self.ids.id_field.text

                    if (self.ids.password_field.text != ""):
                        password = self.ids.password_field.text
                        


                    c.execute("""UPDATE customers SET 
                        siteOrApp = :siteOrApp, 
                        email = :email, 
                        password = :password

                        WHERE oid = :oid""", 
                        {'siteOrApp': site_app, 
                         'email': id_mail, 
                         'password':password, 
                         'oid':record_id})

                    conn.commit()
                    conn.close()

                    self.clearBoxes()
                    self.updateDatble()
                    self.querryDataBase()
                    
    def searchRecords(self):
        lookupRecord = self.ids.name_field.text
        lookupRecord+= '%'
        self.remove_widget(self.table)
        conn = sqlite3.connect(tempDB)
        curs = conn.cursor()
        curs.execute("SELECT rowid,* FROM customers WHERE siteOrApp like ?", (lookupRecord,))
        records = curs.fetchall()
        self.tables(records)
        conn.commit()
        conn.close()


    def genPassword(self,lent):
        lent = int(lent)
        if (lent < 14):
            return
        password = random_password(lent,alphabet_plus )
        self.ids.passwordgen.text = ''
        self.ids.passwordgen.text = password

    def clipboard(self,password):
        Clipboard.copy(password)

    def on_size(self, *args):
        if self.btn_visible:
            self.anim_btn()
        self.tables()
        if (os.path.exists(tempFile)):
            os.remove(tempFile)
        if (os.path.exists(tempDB)):
            os.remove(tempDB)

    def on_pause(self, *args):
        if (os.path.exists(tempDB)):
            os.remove(tempDB)
        if (os.path.exists(tempFile)):
            os.remove(tempFile)
    
    def errorFilePopup(self, args=[]):
        popup = Popup(title=f'Problem {args[0]}', content=Label(text=args[1],halign='center'),
              auto_dismiss=True, size_hint=(0.7, 0.3),pos_hint={'top':0.7})
        popup.open()

class SeedScreen(Screen):
    btn_visible = False
    duration = 0.1

    def do_anim_show_btn_menu(self, *args):
        anim = Animation(
            x=dp(300) - dp(70),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnMenu)

    def do_anim_hide_btn_menu(self, *args):
        anim = Animation(
            x=dp(300),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnMenu)

    def do_anim_show_btn_createdb(self, *args):
        anim = Animation(
            x=dp(300) - dp(140),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnCreateData)
    
    def do_anim_hide_btn_createdb(self, *args):
        anim = Animation(
            x=dp(300),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnCreateData)

    def do_anim_show_btn_passwordGen(self, *args):
        anim = Animation(
            x=dp(300) - dp(210),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnPss)
    
    def do_anim_hide_btn_passwordGen(self, *args):
        anim = Animation(
            x=dp(300),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnPss)

    def do_anim_show_btn_save(self, *args):
        anim = Animation(
            x=dp(300) - dp(280),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnSaveData)
    
    def do_anim_hide_btn_save(self, *args):
        anim = Animation(
            x=dp(300),
            t="out_circ",
            d = self.duration,
            )
        
        anim.start(self.ids.btnSaveData)


    def anim_btn(self) -> None:
        Animation(rotate_value_angle=90 if not self.btn_visible else 0, d=0.1
                  ).start(self.ids.btn_root_pm)
        self.btn_visible = not self.btn_visible

        if self.btn_visible:
            Clock.schedule_once(self.do_anim_show_btn_menu)
            Clock.schedule_once(self.do_anim_show_btn_createdb, 0.05)
            Clock.schedule_once(self.do_anim_show_btn_passwordGen, 0.1)
            Clock.schedule_once(self.do_anim_show_btn_save, 0.15)
        else:
            Clock.schedule_once(self.do_anim_hide_btn_menu)
            Clock.schedule_once(self.do_anim_hide_btn_createdb, 0.05)
            Clock.schedule_once(self.do_anim_hide_btn_passwordGen, 0.1)
            Clock.schedule_once(self.do_anim_hide_btn_save, 0.1)

    def exit_manager(self, *args):
        self.file_manager.close()

    def savefile_seedPhrase_open(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.askPasswordDbc
        )
        self.file_manager.show(Upath)
   
    def askPasswordDbc(self,path):
        content = AskPassword(submit=self.save,path=path)
        self._popup = Popup(title="Password", content=content,
                            size_hint=(0.6, 0.33),pos_hint={'top':0.8})
        self._popup.open()
        self.exit_manager()

    def save(self,path,filename,password):
        if (len(password) < 14):
            toast("lenght 14 chars min")
            return
            
        if ('.dbc' not in filename):
            filename = f'{filename}.dbc'
            createSeed()
        try:
            self.dismiss_popup()
        except:
            pass
        key = hashPassword(password)
        crypt = cryptDatabase(key=key,pathdbc=path,namedb=filename,types='tx')
        #print("1",key,path,filename)
        if (crypt == 1):
            toast("Wrong file/password")
            return
        elif (crypt == 2):
            toast("Wrong name file")
            return
        else:
            try:
                self.dismiss_popup()
            except:
                return
            toast("Created")

    def loadfile_SeedPhrase_open(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_loadpath
            #ext=['.dbc']
        )
        self.file_manager.show(Upath) # Le répertoire racine
        
    def select_loadpath(self, path):
        if os.path.isdir(path):
            #print('Répertoire sélectionné :', path)
            contents = os.listdir(path)
            for item in contents:
                print(item)
        else:
            #print('Fichier sélectionné :', path)
            self.load(path)
        self.exit_manager()

    def load(self, path):
        #print(path)
        name = getName(path)
        ext = getExtension(name)

        self.data = [path,name]
        #self.dismiss_popup()
        self.ids.browseSeedPhraseBtn.text = 'Browsed'

    def PassworGenPopup(self):
        content = GenPassword(submit=self.genPassword, cancel=self.dismiss_popup)
        popup = Popup(title=f'Password Generator', content=content,
              auto_dismiss=True, size_hint=(0.7, 0.3),pos_hint={'top':0.7})
        popup.open()
    
    def genPassword(self,lent):
        lent = int(lent)
        if (lent < 14):
            return
        password = random_password(lent,alphabet_plus )
        self.ids.passwordgen.text = ''
        self.ids.passwordgen.text = password

    def openSeedPhrase(self):
        if (self.ids.openSeedInBtn.text != 'Open'):
            toast("Close this one before")
            return
        password = self.ids.mainPassword.text
        if(len(password)>99):
            toast("Lenght 99 chars max")
            return
        key = hashPassword(password)
        password = ''
        dcrypt = decryptDatabase(key,self.data[0],'tx')
        if (not dcrypt):
            toast("Wrong file or password")
            return
        
        self.makeListFromFile()
        self.ids.openSeedInBtn.text = 'Opened'
        self.ids.labelopenedSManager.text = f'Seeds open : {self.data[1]}'

    def querrySeeds(self):
        file = open(tempFile,'rb')
        contFile = file.read()
        file.close()
        if b"SQLite" in contFile:
            contFile = ""
            self.ids.openSeedInBtn.text = 'Open'
            self.ids.labelopenedSManager.text = 'Seeds open :'
            self.ids.browseSeedPhraseBtn.text = 'Browse'
            toast("Probably Password Manager File")
            return
        contFile = self.listAllInputs()
        print(contFile)
        file = open(tempFile,'wb')
        for all in contFile:
            #print(all)
            file.write(all)
            file.write(b',')
        file.close()

    def clearAllInputs(self):
            self.ids.text_field1.text = ""
            self.ids.text_field2.text = ""
            self.ids.text_field3.text = ""
            self.ids.text_field4.text = ""
            self.ids.text_field5.text = ""
            self.ids.text_field6.text = ""
            self.ids.text_field7.text = ""
            self.ids.text_field8.text = ""
            self.ids.text_field9.text = ""
            self.ids.text_field10.text = ""
            self.ids.text_field11.text = ""
            self.ids.text_field12.text = ""
            self.ids.text_field13.text = ""
            self.ids.text_field14.text = ""
            self.ids.text_field15.text = ""
            self.ids.text_field16.text = ""
            self.ids.text_field17.text = ""
            self.ids.text_field18.text = ""
            self.ids.text_field19.text = ""
            self.ids.text_field20.text = ""
            self.ids.text_field21.text = ""
            self.ids.text_field22.text = ""
            self.ids.text_field23.text = ""
            self.ids.text_field24.text = ""

    def listAllInputs(self):
        listWords =[self.ids.text_field1.text ,
            self.ids.text_field2.text ,
            self.ids.text_field3.text ,
            self.ids.text_field4.text ,
            self.ids.text_field5.text ,
            self.ids.text_field6.text ,
            self.ids.text_field7.text ,
            self.ids.text_field8.text ,
            self.ids.text_field9.text ,
            self.ids.text_field10.text ,
            self.ids.text_field11.text ,
            self.ids.text_field12.text ,
            self.ids.text_field13.text ,
            self.ids.text_field14.text ,
            self.ids.text_field15.text ,
            self.ids.text_field16.text ,
            self.ids.text_field17.text ,
            self.ids.text_field18.text ,
            self.ids.text_field19.text ,
            self.ids.text_field20.text ,
            self.ids.text_field21.text ,
            self.ids.text_field22.text ,
            self.ids.text_field23.text ,
            self.ids.text_field24.text]
        print(listWords)
        for i in range(len(listWords)):
            listWords[i] = listWords[i].encode('utf-8')
        print(listWords)
        return listWords

    def saveAndExit(self):
        #print(self.data)
        self.querrySeeds()
        self.clearAllInputs()
        if os.path.exists(self.data[0]):
            os.remove(self.data[0])
        self.ids.openSeedInBtn.text = 'Open'
        self.ids.labelopenedSManager.text = 'Seeds open :'
        self.ids.browseSeedPhraseBtn.text = 'Browse'
        self.save(self.data[0],self.data[1],self.ids.mainPassword.text)
        if os.path.exists(self.data[0]):
            try:
                os.remove(tempFile)
            except:pass
        else:
            toast("Problem with save not saved")
            return
        self.data= []
        self.ids.mainPassword.text=""

    def makeListFromFile(self):
        file = open(tempFile,'rb')
        contFile = file.read()
        file.close()
        liste = contFile.decode()
        liste = liste.split(',')
        try:
            self.putWordInInput(liste)
        except:pass

    def putWordInInput(self,liste):
        self.ids.text_field1.text = liste[0]
        self.ids.text_field2.text = liste[1]
        self.ids.text_field3.text = liste[2]
        self.ids.text_field4.text = liste[3]
        self.ids.text_field5.text = liste[4]
        self.ids.text_field6.text = liste[5]
        self.ids.text_field7.text = liste[6]
        self.ids.text_field8.text = liste[7]
        self.ids.text_field9.text = liste[8]
        self.ids.text_field10.text = liste[9]
        self.ids.text_field11.text = liste[10]
        self.ids.text_field12.text = liste[11]
        self.ids.text_field13.text = liste[12]
        self.ids.text_field14.text = liste[13]
        self.ids.text_field15.text = liste[14]
        self.ids.text_field16.text = liste[15]
        self.ids.text_field17.text = liste[16]
        self.ids.text_field18.text = liste[17]
        self.ids.text_field19.text = liste[18]
        self.ids.text_field20.text = liste[19]
        self.ids.text_field21.text = liste[20]
        self.ids.text_field22.text = liste[21]
        self.ids.text_field23.text = liste[22]
        self.ids.text_field24.text = liste[23]

    def dismiss_popup(self):
        self._popup.dismiss()

    def on_pause(self, *args):
        if (os.path.exists(tempDB)):
            os.remove(tempDB)
        if (os.path.exists(tempFile)):
            os.remove(tempFile)
    
    def on_size(self, *args):
        if self.btn_visible:
            self.anim_btn()
        if (os.path.exists(tempDB)):
            os.remove(tempDB)
        if (os.path.exists(tempFile)):
            os.remove(tempFile)


class SettsScreen(Screen):
    def changePColor(self,name):
        for x in name:
            name = name.replace(" ","")
        #print(name)
        changeSets(0,name)
    
    def changeTheme(self,theme):
        changeSets(1,theme)
        


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(PMScreen(name='pm'))
sm.add_widget(SeedScreen(name='seed'))
sm.add_widget(SettsScreen(name='setts'))

class GsecuroB(MDApp):

    def build(self):
        self.theme_cls.theme_style = readTheme()
        self.theme_cls.primary_palette = readPrimaryColor()
        kv = Builder.load_file('src/GsecuroB.kv')
        
        return kv

    def file_manager_open(self):
        from kivymd.uix.filemanager import MDFileManager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        self.file_manager.show('/') # Le répertoire racine
         
    def select_path(self, path):
        '''Cette méthode est appelée lorsque l'utilisateur sélectionne un fichier ou un dossier.'''
        #print(path)
        self.exit_manager()
         
    def exit_manager(self, *args):
        '''Cette méthode est appelée lorsque l'utilisateur ferme le gestionnaire de fichiers.'''
        self.file_manager.close()

    def on_stop(self):
        if (os.path.exists(tempFile)):
            os.remove(tempFile)
        if (os.path.exists(tempDB)):
            os.remove(tempDB)
        return True
    def changePColor(self,name):
        for x in name:
            name = name.replace(" ","")
        #print(name)
        changeSets(0,name)
    

if __name__ == '__main__':
    GsecuroB().run()

