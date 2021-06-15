# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:09:25 2020

@author: MVR
"""
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter import ttk
import pickle
from tkinter import filedialog
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from gtts import gTTS
from gtts.tokenizer import pre_processors
from gtts.tokenizer import Tokenizer
from gtts.tokenizer import tokenizer_cases
import gtts.tokenizer.symbols
import os
import shutil
from pathlib import Path
import re




#****************************************************** GLOBAL VARIABLES ********************************************************************

global user_list
user_list=[]
global user_count
user_count=0
global newuserlist
newuserlist=[]
global signup_user_list
signup_user_list=[]
global current_user
current_user=0
global fn
fn=""
global selected
selected=""
global media_count
media_count =0
global clicked
clicked=""
global gtts_dict
gtts_dict={"Arabic" : "ar", "Bengali" : "bn","Chinese" : "zh-cn", "Czech" : "cs", 
           "Dutch" : "nl", "English" : "en","Filipino" : "tl", "Finnish" : "fi", 
           "French" : "fr","German" : "de", "Greek" : "el", "Gujarati" : "gu", 
           "Hindi" : "hi","Indonesian" : "id", "Italian" : "it", "Japanese" : "ja",
           "Kannada" : "kn", "Latin" : "la", "Marathi" : "mr","Malayalam" : "ml",
           "Nepali" : "ne", "Polish" : "pl", "Portugese" : "pt", "Romanian" : "ro",
           "Russian" : "ru","Sinhala" : "si", "Spanish" : "es", "Swedish" : "sv",
           "Tamil" : "ta", "Telugu" : "te", "Thai" : "th", "Turkish" : "tr",
           "Urdu" : "ur", "Vietnamese" : "vi"}
global tess_dict
tess_dict={"Arabic" : "ara", "Bengali" : "ben","Chinese" : "chi_sim", "Czech" : "ces", 
           "Dutch" : "nld", "English" : "eng","Filipino" : "fil", "Finnish" : "fin", 
           "French" : "fra","German" : "deu", "Greek" : "ell", "Gujarati" : "guj", 
           "Hindi" : "hin","Indonesian" : "ind", "Italian" : "ita", "Japanese" : "jpn",
           "Kannada" : "kan", "Latin" : "lat", "Marathi" : "mar","Malayalam" : "mal",
           "Nepali" : "nep", "Polish" : "pol", "Portugese" : "por", "Romanian" : "ron",
           "Russian" : "rus","Sinhala" : "sin", "Spanish" : "spa", "Swedish" : "swe",
           "Tamil" : "tam", "Telugu" : "tel", "Thai" : "tha", "Turkish" : "tur",
           "Urdu" : "urd", "Vietnamese" : "vie"}

#***************************************************************************************************************************************

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class User:
    
    def __init__(self):
        self.fullname=""
        self.username=""
        self.id=0
        self.password=""
        self.confpass=""
        self.folder_name=""

user_list=[User() for i in range(15)]
#newuserlist=[User() for i in range(15)]



#*************************************************** LIBRARY **********************************************************

def library():
    
    global file_chosen
    
    chosen_audio_path=newuserlist[current_user].folder_name+"\\"+file_chosen.get()
    os.startfile(chosen_audio_path+"\\"+"testpdf.mp3")
    

#***************************************************** CONVERSION ***********************************************************

def convert(fname):
    
    
    global selected
    global media_count
    global current_user
    global newuserlist
    global clicked
    print("Clicked: ", clicked)
    
    if(clicked.get()=="Normal"):
        speed=False
    else:
        speed=True
        
    print("Speed: ", speed)
    
    print("Length: ", len(newuserlist))
    print("Current user: ", current_user)
    user_folder=newuserlist[current_user].folder_name
    print("Current user folder: ", user_folder)
    
    for fol in os.listdir(user_folder):
        if os.path.isdir(fol):
            media_count = media_count+1
            
    print(media_count)
    
    #new_folder_path=user_folder+"\\fol"+str(media_count+1)
    #print(new_folder_path)
    
    new_folder_path=user_folder+"\\"+Path(fname).stem
    print(new_folder_path)
    
    try:
        os.mkdir(new_folder_path)
    except OSError:
        print ("Creation of the directory %s failed" % new_folder_path)
    else:
        print ("Successfully created the directory %s " % new_folder_path)
        
    if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
        
        img = Image.open(fname)  
  
        # save a image using extension        
        name = new_folder_path + "\img" + '.jpg'
        print(name)
        #image.save(name, 'JPEG')
        img = img.save(name, 'JPEG')
    else:
        #print(fname)
            
        images = convert_from_path(fname)
        
        i = 1
        path_of_images=[]
        for image in images:
            name = new_folder_path + "\img" + str(i) + '.jpg'
            print(name)
            image.save(name, 'JPEG')
            i = i + 1
        	#image.save('output' + str(i) + '.jpg', 'JPEG')
        
    file_text=""
        
    global selected
    
    language=selected.get()
    
    tess_lang= tess_dict[language]
    print(tess_lang)
    gtts_lang= gtts_dict[language]
    print(gtts_lang)
    
    j=1
    for img in os.listdir(new_folder_path):
        input_path = os.path.join(new_folder_path, img)
        mytext = pytesseract.image_to_string(input_path, lang=tess_lang)
        file_text= file_text + mytext
        print(file_text)
    
    output=gTTS(text=file_text, slow=speed, tld="com", lang=gtts_lang, pre_processor_funcs = [pre_processors.tone_marks,pre_processors.end_of_line,pre_processors.abbreviations,pre_processors.word_sub], 
                tokenizer_func=Tokenizer([tokenizer_cases.tone_marks,tokenizer_cases.period_comma,tokenizer_cases.colon,tokenizer_cases.other_punctuation]).run)
    output.save("testpdf.mp3")
    shutil.move("testpdf.mp3", new_folder_path+"\\"+"testpdf.mp3")
    #output.save("%s.mp3" % os.path.join(new_folder_path+"\\"+testpdf))
    #os.system("start new_folder_path +'\\'+'testpdf.mp3' ")
    os.startfile(new_folder_path+"\\"+"testpdf.mp3")
    

#******************************************************** MAIN MENU ********************************************************************
'''def selectfile():
    
    filename= filedialog.askopenfilename( menu, title="Select a file", initialdir="\C:")
    print(filename)'''

def mainmenu():
    
    global fn
    main_menu=Toplevel()
    main_menu.configure(bg="#fddb3a")
    main_menu.geometry("1920x1080")
    main_menu.title("Main Menu")
    
    menu_img=ImageTk.PhotoImage(Image.open("logo.png").resize((130, 110), Image.ANTIALIAS))
    menu_label=Label(main_menu,image=menu_img,bg="#fddb3a")
    menu_label.img=menu_img
    #logo_label.image=logo_img
    menu_label.grid(row="0", column="0",columnspan="2",padx=(500,0),pady=(15,10))
    
    def selectfile():
    
        global fn
        filename= filedialog.askopenfilename(parent = main_menu, title="Select a file", initialdir="\C:")
        fn=filename
        print(filename)
        
        file_size = os.path.getsize(fn)
        print(file_size)
        
        if(file_size > 20000000):
            response=messagebox.showerror( "Error!" , "File size exceeds 20 MB. Upload a new file.", parent=main_menu)
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')) != True:
            response=messagebox.showerror( "Error!" , "Upload any pdf or image only.", parent=main_menu)
        else:
            fname_label.config(text="")
            #fname_label= Label(main_menu, text = fn, font="Helvetica 10",bg="#fddb3a")
            #fname_label.grid(row="2", column="2", columnspan="2", padx=(5,20), pady=(20,50))
            fname_label.config(text=fn)
        
        
    heading1=Label(main_menu, text="Convert a new file!",font='Helvetica 35 bold',bg="#fddb3a")
    heading1.grid(row="1",column="0",padx=(500,50),columnspan="2")
    
    upload_label= Label(main_menu, text="Upload PDF/Image : ",font='Helvetica 15 bold',bg="#fddb3a")
    upload_label.grid(row="2",column="0",padx=(500,50),pady=(20,50))
    upload_btn= Button(main_menu, text="Upload", bg="#0d395f",fg="#FFFFFF", padx="50", pady="5",font="Montserrat 13", command=selectfile)
    upload_btn.grid(row="2", column = "1",pady=(20,50) )
    fname_label= Label(main_menu, text = "Upload a PDF/Image with size less than 20MB.", font="Helvetica 10",bg="#fddb3a")
    fname_label.grid(row="2", column="2", columnspan="2", padx=(5,20), pady=(20,50))
    
    global clicked
    clicked=StringVar()
    clicked.set("Normal")
    speed_label=Label(main_menu, text="Speed: ",font='Helvetica 15 bold',bg="#fddb3a")
    speed_label.grid(row="3",column="0",padx=(500,50),pady=(0,50))
    speed_option=ttk.Combobox(main_menu, width="27", textvariable=clicked)
    speed_option["values"]=("Normal", "Slow")
    speed_option.grid(row="3", column="1",pady=(0,50))
    
    lang_label= Label(main_menu, text = "Language :", font='Helvetica 15 bold',bg="#fddb3a")
    lang_label.grid(row="4", column="0", padx=(500,50))
    
    global selected
    selected=StringVar()
    selected.set("English")
    global fn
    print(fn)
    
    
    dropdown= ttk.Combobox(main_menu, width="27", textvariable=selected)
    
    dropdown["values"]= ("Arabic", "Bengali","Chinese", "Czech", "Dutch", "English","Filipino", "Finnish", "French","German", "Greek", "Gujarati", "Hindi","Indonesian", "Italian", "Japanese", "Kannada", "Latin", "Marathi",
                          "Malayalam","Nepali", "Polish", "Portugese", "Romanian", "Russian", "Oriya", "Sinhala", "Spanish", "Swedish", "Tamil", "Telugu", "Thai", "Turkish", "Urdu", "Vietnamese")
    #dropdown.config(bg="#ec0101")
    dropdown.grid(row="4", column="1")
    
    convert_btn=Button(main_menu, text="Convert", bg="#0d395f",fg="#FFFFFF", padx="50", pady="5",font="Montserrat 13", command= lambda: convert(fn))
    convert_btn.grid(row="5", column="0", columnspan="2", pady=(30,10),sticky="n", padx=(600,100))
    
    heading2=Label(main_menu, text="Choose from Library!",font='Helvetica 35 bold',bg="#fddb3a")
    heading2.grid(row="6",column="0",padx=(500,50),pady=(30,50),columnspan="2")
    
    library_label=Label(main_menu, text = "Select file :", font='Helvetica 15 bold',bg="#fddb3a")
    library_label.grid(row="7", column="0", padx=(500,50))
    
    print("Current user issssssss ", newuserlist[current_user].folder_name)
    folder_list=[f.name for f in os.scandir(newuserlist[current_user].folder_name) if f.is_dir()]
    
    if not len(folder_list):
        user_lib=Label(main_menu, text="You are a first time user!", font='Helvetica 15 bold',bg="#fddb3a")
        user_lib.grid(row="7", column="1")
    
    global file_chosen
    file_chosen=StringVar()
    file_chosen.set(folder_list[0])
    folder_list=tuple(folder_list)
    file_option=ttk.Combobox(main_menu, width="27", textvariable=file_chosen)
    file_option["values"]=folder_list
    file_option.grid(row="7", column="1")
    
    
    library_btn=Button(main_menu, text="Play", bg="#0d395f",fg="#FFFFFF", padx="50", pady="5",font="Montserrat 13", command=library)
    library_btn.grid(row="8", column="0", columnspan="2",sticky="n", padx=(600,100),pady=(20,0))
    
    
                          

    


# *********************************************** LOGIN WINDOW ********************************************************************

def open_login():


    def confirm():
        
        global newuserlist
        newuserlist=[]
        g2=open("UserFile.txt","rb")

        while 1:
            try:
                #o = pickle.load(g2)
                #o= Unpickler(g2).load()
                newuserlist.append(pickle.load(g2))
            except EOFError:
                break
            #newuserlist.append(o)
        g2.close()
        
        #print(type(newuserlist[0]), type(newuserlist[0].username))

        #print(user_count)
        for j in range(0, len(newuserlist)):
            print(len(newuserlist))
            print(newuserlist[j].password)
            if(newuserlist[j].username == e1.get()):
                print(j, "aaaaaaaaaaaaaaaaa")
                if(newuserlist[j].password == e2.get()):
                    print(j)
                    print(newuserlist[j].username)
                    print(newuserlist[j].password)
                    print(newuserlist[j].id)
                    print("Folder: ", newuserlist[j].folder_name)
                    global current_user
                    current_user=j
                    login_cnf=Label(login, text="You have successfully logged in!")
                    login_cnf.grid(row="5", column="0",columnspan="2")
                    mainmenu()
                    break
                    
                else:
                    response=messagebox.showerror( "Error!" , "Incorrect Username or Password! Please try again.", parent=login) 
                    '''unconf_login=Label(login, text="Incorrect details! Please try again.")
                    unconf_login.grid(row="4",column="0", columnspan="2")
                    e1.delete(0,END)
                    e2.delete(0,END)
                    open_login()'''
                    break
            else:
                continue


    login=Toplevel()
    login.configure(bg="#fddb3a")
    login.geometry("1920x1080")
    login.title("Login Page")
    
    login_img=ImageTk.PhotoImage(Image.open("logo.png").resize((150, 130), Image.ANTIALIAS))
    login_label=Label(login,image=login_img,bg="#fddb3a")
    login_label.img=login_img
    #logo_label.image=logo_img
    login_label.grid(row="0", column="0",columnspan="2",padx=(10,0),pady=(80,20))
    
    label_title=Label(login, text="Login!",bg="#fddb3a",font='Helvetica 40 bold')
    label_title.grid(row="1", column="0",padx="650",columnspan="2")
    
    e1=Entry(login, width="40", borderwidth="5")
    label1=Label(login, text="Username:",bg="#fddb3a",font="Oxygen 18" )
    label1.grid(row="2", column="0", padx=(320,5), pady=(50,10))
    e1.grid(row="2", column="1", pady=(50,10), padx=(0,200),ipady="3")
    
    e2=Entry(login, width="40", borderwidth="5", show="*")
    label2=Label(login, text="Password:",bg="#fddb3a",font="Oxygen 18" )
    label2.grid(row="3", column="0", padx=(320,5))
    e2.grid(row="3", column="1", padx=(0,200),ipady="3")
    
    login_btn=Button(login, text="Login", bg="#0d395f", fg="#FFFFFF",padx="50", pady="5",font="Montserrat 13", command=confirm)
    login_btn.grid(row="4",column="0",columnspan="2", pady=(40,10))




#**********************SIGNUP WINDOW******************************************************************************************************

def open_signup():


    def confirmation():
        
        signup_user_list=[]
        g2=open("UserFile.txt","rb")

        while 1:
            try:
                #o = pickle.load(g2)
                #o= Unpickler(g2).load()
                signup_user_list.append(pickle.load(g2))
            except EOFError:
                break
            #newuserlist.append(o)
        g2.close()
        
        
        global user_count
        user_count= len(signup_user_list)
        user_count=user_count+1
        
        if any(x.username == e3.get() for x in signup_user_list):
            messagebox.showerror( "Error!" , "This username is already taken. Choose another one.", parent=signup)
        else:
            if e4.get()==e5.get():
                if len(e4.get()) < 8:
                    messagebox.showerror( "Error!" , "Your password cannot be empty and must be atleast 8 characters long, and should have a number and capital letter in it.", parent=signup)
                elif re.search('[0-9]',e4.get()) is None:
                    messagebox.showerror( "Error!" , "Your password cannot be empty and must be atleast 8 characters long, and should have a number and capital letter in it.", parent=signup)
                elif re.search('[A-Z]',e4.get()) is None: 
                    messagebox.showerror( "Error!" , "Your password cannot be empty and must be atleast 8 characters long, and should have a number and capital letter in it.", parent=signup)
                else:
                    #global 
                    x=0
                    if any(obj.fullname == e6.get() for obj in user_list):
                        x=x+1
                        print("X======", x)
                        
                    if(x>0):
                        user_list[user_count].fullname=e6.get()+str(x)
                    else:
                        user_list[user_count].fullname=e6.get()
                        
                    user_list[user_count].username=e3.get()
                    print(user_list[user_count].username, "aaaaaaa")
                    user_list[user_count].password=e4.get()
                    user_list[user_count].id=user_count+100
                    #user_list[user_count].fullname=e6.get()
                    #user_count=user_count+1
                    #print(e3.get(), "aaaaaaa")
                    
                    #user_count=user_count+1
                    conf_signup=Label(signup, text="You have successfully signed up!")
                    conf_signup.grid(row="7",column="0", columnspan="2")
                    
                    directory_path=r"C:\Users\MVR\Desktop\FINAL SE ROJECT"
                    user_path = r"C:\Users\MVR\Desktop\FINAL SE ROJECT" + '\\'  + user_list[user_count].fullname
                    
                    user_list[user_count].folder_name = user_path
                    g1=open("UserFile.txt","ab")
                    pickle.dump(user_list[user_count],g1)
                    g1.close()
                    print("Creater folder name: ", user_list[user_count].folder_name)
                    
                    try:
                        os.mkdir(user_path)
                    except OSError:
                        print ("Creation of the directory %s failed" % user_path)
                    else:
                        print ("Successfully created the directory %s " % user_path)
                    
                    
                    user_count=user_count+1
                    #print(user_count)
            else:
                response=messagebox.showerror( "Error!" , "Your passwords do not match! Please enter again.", parent=signup)
                '''unconf_signup=Label(signup, text="Incorrect details! Please try again.")
                unconf_signup.grid(row="5",column="0", columnspan="2")
                e3.delete(0,END)
                e4.delete(0,END)
                e5.delete(0,END)
                open_signup()'''


    signup=Toplevel()
    signup.configure(bg="#fddb3a")
    signup.geometry("1920x1080")
    signup.title("Sign Up Page")
    
    sign_img=ImageTk.PhotoImage(Image.open("logo.png").resize((150, 130), Image.ANTIALIAS))
    sign_label=Label(signup,image=sign_img,bg="#fddb3a")
    sign_label.img=sign_img
    #logo_label.image=logo_img
    sign_label.grid(row="0", column="0",columnspan="2",padx=(10,0),pady=(80,20))


    label_title2=Label(signup, text="Sign Up!",bg="#fddb3a",font='Helvetica 40 bold')
    label_title2.grid(row="1", column="0",padx="600",columnspan="2")
    
    e6=Entry(signup, width="40", borderwidth="5")
    label6=Label(signup, text="Full Name:",bg="#fddb3a",font="Oxygen 18" )
    label6.grid(row="2", column="0", padx=(320,0), pady=(50,10))
    e6.grid(row="2", column="1", pady=(50,10), padx=(0,200), ipady="3")

    e3=Entry(signup, width="40", borderwidth="5")
    label3=Label(signup, text="Username:",bg="#fddb3a",font="Oxygen 18" )
    label3.grid(row="3", column="0", padx=(320,0), pady=(0,10))
    e3.grid(row="3", column="1", pady=(0,10), padx=(0,200), ipady="3")

    e4=Entry(signup, width="40", borderwidth="5", show="*")
    label4=Label(signup, text="Password:",bg="#fddb3a",font="Oxygen 18" )
    label4.grid(row="4", column="0", padx=(320,0), pady=(0,10))
    e4.grid(row="4", column="1", padx=(0,200), pady=(0,10),ipady="3")

    e5=Entry(signup, width="40", borderwidth="5", show="*")
    label5=Label(signup, text="Confirm Password:",bg="#fddb3a",font="Oxygen 18" )
    label5.grid(row="5", column="0", padx=(250,0))
    e5.grid(row="5", column="1", padx=(0,200),ipady="3")

    sign_up_btn=Button(signup, text="Sign Up", bg="#0d395f", fg="#FFFFFF", padx="50", pady="5",font="Montserrat 13", command=confirmation)
    sign_up_btn.grid(row="6",column="0",columnspan="2", pady=(40,10))
    
    
#************************************************************** ABOUT ****************************************************************
    
def open_about():
    

    about=Toplevel()
    about.configure(bg="#fddb3a")
    about.geometry("400x400")
    about.title("About")
    
    about_img=ImageTk.PhotoImage(Image.open("logo.png").resize((120, 100), Image.ANTIALIAS))
    about_img_label=Label(about,image=about_img,bg="#fddb3a")
    about_img_label.img=about_img
    #logo_label.image=logo_img
    about_img_label.grid(row="0", column="0",padx=(10,0),pady=(15,15))
    
    about_label=Label(about, text="About!",bg="#fddb3a",fg="#0d395f", font='Helvetica 30 bold')
    about_label.grid(row="1", column="0", padx="130", pady=(0,10))
    
    info_label=Label(about, text="Welcome to Audiofy!\n A text to audio convertor.\n Upload any PDF or Image\n to convert to audio,\n or you could just choose an audio\n from your Audiofy library, click on Play,\n and sit back and relax!",bg="#fddb3a", fg="#0d395f", font="Montserrat 13 italic")
    info_label.grid(row="2", column="0")
    

#*****************************************************  HOME PAGE *******************************************************************


root=Tk()
root.configure(bg="#FFFFFF")
root.geometry("1920x1080")
root.title("Home Page")


logo_img=ImageTk.PhotoImage(Image.open("logo.png"))
logo_label=Label(root,image=logo_img,bg="#FFFFFF")
#logo_label.image=logo_img
logo_label.pack(fill=X, pady=(100,0))
login_bt=Button(root, text="Login", bg="#fecd1a", width="50", height="2",font="Montserrat 13 italic", command=open_login)
signup_bt=Button(root, text="Sign Up", bg="#fecd1a", width="50", height="2", font="Montserrat 13 italic", command=open_signup)
about_bt= Button(root, text="About",bg="#fecd1a", width="50", height="2",font="Montserrat 13 italic", command=open_about)
about_bt.pack(pady=(30,10),padx="150")
login_bt.pack( pady="10", padx="150")
signup_bt.pack( pady="10", padx="150")

root.mainloop()