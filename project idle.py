from tkinter import *
from tkinter import ttk
from tkinter.font import Font, BOLD
from tkinter import messagebox
from tkinter.ttk import Labelframe
from PIL import ImageTk, Image
import pymysql as pym
from googletrans import Translator,constants
from gtts import gTTS
import os
from rake_nltk import Rake
from bs4 import BeautifulSoup 
from requests_html import HTMLSession

r = Rake()
translator = Translator()
mycon = pym.connect(host = "localhost",user = "root",password = "gautham@2005",database = "details")

login = Tk()
login.title("GMV NEWS")
login.configure(bg="#ffe5b4")

username_var = StringVar()
password_var = StringVar()
translate_var = StringVar()

register_username_var  = StringVar()
register_password_var  = StringVar()

def register():
    global registerpage
    registerpage = Toplevel(bg="#ffe5b4")
    registerpage.title("Register Page")

    usernamelabel = Label(registerpage, text="Enter Username",bg="#8ad8e6")
    usernamelabel.grid(row=0, column=0)

    usernameentry = Entry(registerpage,textvariable=register_username_var)
    usernameentry.grid(row=0,column=1)

    passwordlabel = Label(registerpage, text="Enter Password",bg="#8ad8e6")
    passwordlabel.grid(row=1, column=0)

    passwordentry = Entry(registerpage,textvariable=register_password_var,show="*")
    passwordentry.grid(row=1,column=1)

    register_submit_button = Button(registerpage,text="Submit",command=registration,bg="#ffdb58")
    register_submit_button.grid(row=2,column=0,columnspan=2)

def registration():
    cursor = mycon.cursor()
    register_username = register_username_var.get()
    register_password = register_password_var.get()
    try:
        if len(register_username)>= 1 and len(register_password) >= 1:
            cursor.execute(f'insert into up values("{register_username}","{register_password}")')
            mycon.commit()
            messagebox.showinfo("GMV NEWS","Registration Successful")
            cursor.close()
            registerpage.destroy()
        else:
            messagebox.showerror("GMV NEWS","Enter valid username and password")
    except:
        messagebox.showerror("GMV NEWS","Enter valid username and password")
    register_username_var.set("")
    register_password_var.set("")

def speech(heading,content):
    messagebox.showinfo("GMV News","Conversion is in progress, please wait till the audio plays")
    speech_text = "Heading "+heading+"Content "+content
    ttsobj = gTTS(speech_text)
    ttsobj.save("tts.mp3")
    os.system("tts.mp3")

def translate_function(translatecontent):
    translate_lang = translate_var.get()
    langcode = ""
    for i,j in constants.LANGUAGES.items():
        if j == translate_lang.lower():
            langcode = i
    if not langcode:
        messagebox.showerror("GMV NEWS","Enter a valid language!")
        translate_var.set("")
    else:
        result = translator.translate(translatecontent, src="en",dest=langcode)

        translateframe = LabelFrame(translatepage, text="Translated Content")  
        translateframe.grid(row=2,column=0,columnspan=2) 

        translatedtext = Text(translateframe,height=30,width=100,spacing2=4,font="lucida 13 bold",wrap=WORD)  
        translatedtext.bind("<Key>", lambda e: "break")
        translatedtext.insert(INSERT, result.text)
        translatedtext.grid(row=0,column=0)
        
        scrollbar = ttk.Scrollbar(
            translateframe,
            orient='vertical',
            command=translatedtext.yview
        )
        scrollbar.grid(row=0, column=1, sticky=NS)
        translatedtext['yscrollcommand'] = scrollbar.set

        translate_submit["state"] = "disabled"
        translate_var.set("")

def translate(content):
    translatecontentvar = content
    global translatepage
    global translate_submit
    translatepage = Toplevel()

    translate_label = Label(translatepage,text="Enter language to translate text to")
    translate_label.grid(row=0,column=0)

    translate_entry = Entry(translatepage,textvariable=translate_var)
    translate_entry.grid(row=0,column=1)

    translate_submit = Button(translatepage,text = "Submit",command = lambda:translate_function(translatecontentvar))
    translate_submit.grid(row=1,column=0)

    translate_exit = Button(translatepage,text = "Exit to Main Window",command=translatepage.destroy)
    translate_exit.grid(row=1,column=1)

def keyword(content):
    keywordpage = Toplevel()

    keywordframe = LabelFrame(keywordpage, text="Top Ten Keywords",padx=100)  
    keywordframe.grid(row=0,column=0)

    r.extract_keywords_from_text(content)
    count = 1
    text = ""
    for i in r.get_ranked_phrases_with_scores():
        if i[1] not in text:
            text += str(i[1])+"\n"
            count += 1
        if not count <= 10:
            break
    count = 1

    keywordtext = Message(keywordframe,text = text ,aspect=400,justify=CENTER,font = ("helvetica",11))
    keywordtext.grid(row=0,column=0) 

    keyword_exit = Button(keywordpage,text = "Exit to Main Window",command=keywordpage.destroy)
    keyword_exit.grid(row=1,column=0)
    
def file_maker(heading,content,name):
    file = open("news.txt","w")
    file.write(name+"\n\n")
    file.write("Heading:\n-------\n")
    file.write(heading)
    file.write("\n\nContent:\n-------\n")
    for i in content:
        try:
            file.write(i)
        except:
            pass
    messagebox.showinfo("GMV NEWS","File has been created in directory under the name \"news.txt\"")       
    file.close()

def w1():
    def show_article1():
        drop_button['state'] = DISABLED
        drop['state'] = DISABLED
        labelframe1 = LabelFrame(w1, text="Heading",padx=100,bg="#8ad8e6",font=("helvetica",10,"bold"))  
        labelframe1.grid(row=1,column=0,columnspan=5)  
    
        toplabel = Message(labelframe1, text= heading1,aspect=400,justify=CENTER,font=("helvetica",10,"bold"),fg = "blue",bg="#8ad8e6")  
        toplabel.grid(row=0,column=0) 

        labelframe2 = LabelFrame(w1, text = "Content",font=("helvetica",10,"bold"))  
        labelframe2.grid(row=2,column=0,columnspan=5) 
    
        text = Text(labelframe2,height=30,width=100,spacing2=4,font=("lucida",clicked.get(),"bold"),wrap=WORD,bg="#ffe5b4")  
        text.bind("<Key>", lambda e: "break")
        text.insert(INSERT, content1)  
        text.grid(row=0,column=0)

        b1 = Button(w1,text = "Convert to Speech",command = lambda:speech(heading1,content1),bg="#ffdb58") # heading variable, content variable
        b1.grid(row=3,column=0)

        b2 = Button(w1,text = "Translate",command = lambda:translate(content1),bg="#ffdb58")
        b2.grid(row=3,column=1)

        b3 = Button(w1,text = "Display Keywords",command = lambda:keyword(content1),bg="#ffdb58")
        b3.grid(row=3,column=2)
        
        b4 = Button(w1,text="Create File with News",command = lambda:file_maker(heading1,content1,"Indian Defense News"),bg="#ffdb58")
        b4.grid(row=3,column=3)
        
        b5 = Button(w1,text = "Return to Main Page",command=w1.destroy,bg="#ffdb58")
        b5.grid(row=3,column=4)
        
        scrollbar = ttk.Scrollbar(
            labelframe2,
            orient='vertical',
            command=text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=NS)
        text['yscrollcommand'] = scrollbar.set
        
    w1 = Toplevel(bg="#ffe5b4")

    l = []
    s = HTMLSession()
    s2 = HTMLSession()
    url = 'http://www.indiandefensenews.in/'
    def getdata(url):
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_heading(soup):
        page = soup.find('h1', {'class' : 'post-title'})
        return page.text
    soup = getdata(url)
    heading1 = get_heading(soup)

    def get_link(soup):
        page = soup.find('a', {'class' : 'color-transition'})
        return page['href']
    get_link(soup)
    url2 = get_link(soup)
    url2 = url2[37:]

    def getarticle(url):
        r = s.get(url2)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_content(soup):
        page = soup.find('div', {'class' : 'post-content'})
        c = page.find_all('div')
        for i in c:
            l.append(i.text)
        s = ' '.join(l)
        return s
    soup2 = getarticle(url2)

    content1 = get_content(soup2)
    
    clicked = StringVar()
    clicked.set("Select Font Size")
    
    messagebox.showinfo("GMV News","Select font size from the drop down list provided please")

    drop = OptionMenu(w1,clicked,6,7,8,9,10,11,12,13)
    drop.config(bg="#a91b0d",fg="white")
    drop.grid(row=0,column=0)
    
    drop_button = Button(w1, text="OK", command=show_article1,bg="#86dc3d")
    drop_button.grid(row=0,column=1)

def w2():
    def show_article2():
        drop_button['state'] = DISABLED
        drop['state'] = DISABLED
        labelframe1 = LabelFrame(w2, text="Heading",padx=100,bg="#8ad8e6",font=("helvetica",10,"bold"))  
        labelframe1.grid(row=1,column=0,columnspan=5)
    
        toplabel = Message(labelframe1, text=heading2,aspect=400,justify=CENTER,font=("helvetica",10,"bold"),fg = "blue",bg="#8ad8e6")  
        toplabel.grid(row=0,column=0) 

        labelframe2 = LabelFrame(w2, text = "Content",font=("helvetica",10,"bold"))  
        labelframe2.grid(row=2,column=0,columnspan=5) 
    
        text = Text(labelframe2,height=30,width=100,spacing2=4,font=("lucida",clicked.get(),"bold"),wrap=WORD,bg="#ffe5b4")  
        text.bind("<Key>", lambda e: "break")
        text.insert(INSERT, content2)  
        text.grid(row=0,column=0)

        b1 = Button(w2,text = "Convert to Speech",command = lambda:speech(heading2, content2),bg="#ffdb58")
        b1.grid(row=3,column=0)

        b2 = Button(w2,text = "Translate",command = lambda:translate(content2),bg="#ffdb58")
        b2.grid(row=3,column=1)

        b3 = Button(w2,text = "Display Keywords",command = lambda:keyword(content2),bg="#ffdb58")
        b3.grid(row=3,column=2)
        
        b4 = Button(w2,text="Create File with News",command = lambda:file_maker(heading2,content2,"Defense News"),bg="#ffdb58")
        b4.grid(row=3,column=3)

        b5 = Button(w2,text = "Return to Main Page",command=w2.destroy,bg="#ffdb58")
        b5.grid(row=3,column=4)
        
        scrollbar = ttk.Scrollbar(
            labelframe2,
            orient='vertical',
            command=text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=NS)
        text['yscrollcommand'] = scrollbar.set
    w2 = Toplevel(bg="#ffe5b4")

    l = []
    std_url = 'https://www.defensenews.com/'
    link = ''
    s = HTMLSession()
    url = 'https://www.defensenews.com/global/'
    def getdata(url):
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_heading(soup):
        page = soup.find('a', {'class' : 'ArticleLink-sc-1f35nm6-0 jckchf o-articleCard__link'})
        return page.text
    soup = getdata(url)
    heading2 = get_heading(soup)


    def get_link(soup):
        page = soup.find('a', {'class' : 'ArticleLink-sc-1f35nm6-0 jckchf o-articleCard__link'})
        return page['href']
    get_link(soup)
    url2 = std_url+get_link(soup)


    def getarticle(url):
        r = s.get(url2)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_content(soup):
        page = soup.findAll('p', {'class' : 'Paragraph-sc-1tqpf5s-0 kEzXdV body-paragraph body-paragraph'})
        for i in page:
            l.append(i.text)
        s = ' '.join(l)
        return s
    soup2 = getarticle(url2)

    content2 = get_content(soup2)
    
    clicked = StringVar()
    clicked.set("Font Size")
    
    messagebox.showinfo("GMV News","Please select font size from the drop down list provided")

    drop = OptionMenu(w2,clicked,6,7,8,9,10,11,12,13)
    drop.config(bg="#a91b0d",fg="white")
    drop.grid(row=0,column=0)
    
    drop_button = Button(w2, text="Select Size", command=show_article2,bg="#86dc3d")
    drop_button.grid(row=0,column=1)

def w3():
    def show_article3():
        drop_button['state'] = DISABLED
        drop['state'] = DISABLED
        labelframe1 = LabelFrame(w3, text="Heading",padx=100,bg="#8ad8e6",font=("helvetica",10,"bold"))  
        labelframe1.grid(row=1,column=0,columnspan=5)  
    
        toplabel = Message(labelframe1, text=heading3,aspect=400,justify=CENTER,font=("helvetica",10,"bold"),fg = "blue",bg="#8ad8e6")  
        toplabel.grid(row=0,column=0) 

        labelframe2 = LabelFrame(w3, text = "Content",font=("helvetica",10,"bold"))  
        labelframe2.grid(row=2,column=0,columnspan=5) 
    
        text = Text(labelframe2,height=30,width=100,spacing2=4,font=("lucida",clicked.get(),"bold"),wrap=WORD,bg="#ffe5b4")  
        text.bind("<Key>", lambda e: "break")
        text.insert(INSERT, content3)  
        text.grid(row=0,column=0)

        b1 = Button(w3,text = "Convert to Speech",command = lambda:speech(heading3, content3),bg="#ffdb58")
        b1.grid(row=3,column=0)

        b2 = Button(w3,text = "Translate",command = lambda:translate(content3),bg="#ffdb58")
        b2.grid(row=3,column=1)

        b3 = Button(w3,text = "Display Keywords",command = lambda:keyword(content3),bg="#ffdb58")
        b3.grid(row=3,column=2)
        
        b4 = Button(w3,text="Create File with News",command = lambda:file_maker(heading3,content3,"Janes"),bg="#ffdb58")
        b4.grid(row=3,column=3)

        b5 = Button(w3,text = "Return to Main Page",command=w3.destroy,bg="#ffdb58")
        b5.grid(row=3,column=4)
        
        scrollbar = ttk.Scrollbar(
            labelframe2,
            orient='vertical',
            command=text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=NS)
        text['yscrollcommand'] = scrollbar.set
        
    w3 = Toplevel(bg="#ffe5b4")

    l = []
    link = ''
    s = HTMLSession()
    url = 'https://www.janes.com/defence-news/'
    def getdata(url):
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_heading(soup):
        page = soup.find('div', {'class' : 'list-content'})
        c = page.find('h2')
        return c.text
    soup = getdata(url)
    heading3 = get_heading(soup)

    def get_link(soup):
        page = soup.find('section', {'id' : 'Contentplaceholder1_C030_Col00'})
        c = page.find('a')
        return c['href']
    get_link(soup)
    url2 = get_link(soup)

    def getarticle(url):
        r = s.get(url2)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_content(soup):
        page = soup.find('div', {'class' : 'read-more-p'})
        c = page.find_all('p')
        for i in c:
            l.append(i.text)
        s = ' '.join(l)
        return s
    soup2 = getarticle(url2)

    content3 = get_content(soup2)
    
    clicked = StringVar()
    clicked.set("Select Font Size")
    
    messagebox.showinfo("GMV News","Select font size from the drop down list provided please")

    drop = OptionMenu(w3,clicked,6,7,8,9,10,11,12,13)
    drop.config(bg="#a91b0d",fg="white")
    drop.grid(row=0,column=0)
    
    drop_button = Button(w3, text="OK", command=show_article3,bg="#86dc3d")
    drop_button.grid(row=0,column=1)

def w4():
    def show_article4():
        drop_button['state'] = DISABLED
        drop['state'] = DISABLED
        labelframe1 = LabelFrame(w4, text="Heading",padx=100,bg="#8ad8e6",font=("helvetica",10,"bold"))  
        labelframe1.grid(row=1,column=0,columnspan=4)  
    
        toplabel = Message(labelframe1, text=heading4,aspect=400,justify=CENTER,font=("helvetica",10,"bold"),fg = "blue",bg="#8ad8e6")  
        toplabel.grid(row=1,column=0) 

        labelframe2 = LabelFrame(w4, text = "Content",font=("helvetica",10,"bold"))  
        labelframe2.grid(row=2,column=0,columnspan=4) 
  
        text = Text(labelframe2,height=30,width=100,spacing2=4,font=("lucida",clicked.get(),"bold"),wrap=WORD,bg="#ffe5b4")  
        text.bind("<Key>", lambda e: "break")
        text.insert(INSERT, content4)  
        text.grid(row=0,column=0)

        b1 = Button(w4,text = "Convert to Speech",command = lambda:speech(heading4, content4),bg="#ffdb58")
        b1.grid(row=3,column=0)
        
        b2 = Button(w4,text = "Translate",command = lambda:translate(content4),bg="#ffdb58")
        b2.grid(row=3,column=1)

        b3 = Button(w4,text = "Display Keywords",command = lambda:keyword(content4),bg="#ffdb58")
        b3.grid(row=3,column=2)
        
        b4 = Button(w4,text="Create File with News",command = lambda:file_maker(heading4,content4,"Lockheed Martin"),bg="#ffdb58")
        b4.grid(row=3,column=3)

        b5 = Button(w4,text = "Return to Main Page",command=w4.destroy,bg="#ffdb58")
        b5.grid(row=3,column=4)
        
        scrollbar = ttk.Scrollbar(
            labelframe2,
            orient='vertical',
            command=text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=NS)
        text['yscrollcommand'] = scrollbar.set
        
    w4 = Toplevel(bg="#ffe5b4")

    from requests_html import HTMLSession
    import csv
    l = []
    link = ''
    s = HTMLSession()
    url = 'https://news.lockheedmartin.com/news-releases'
    def getdata(url):
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_heading(soup):
        page = soup.find('div', {'class' : 'wd_title'})
        c = page.find('a')
        return c.text
    soup = getdata(url)
    heading4 = get_heading(soup)
    def get_link(soup):
        page = soup.find('div', {'class' : 'wd_title'})
        c = page.find('a')
        return c['href']
    get_link(soup)
    url2 = get_link(soup)


    def getarticle(url):
        r = s.get(url2)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_content(soup):
        page = soup.find('div', {'class' : 'wd_body wd_news_body'})
        c = page.find_all('p')
        for i in c:
            l.append(i.text)
        s = ' '.join(l)
        return s
    soup2 = getarticle(url2)

    content4 = get_content(soup2)

    clicked = StringVar()
    clicked.set("Select Font Size")
    
    messagebox.showinfo("GMV News","Select font size from the drop down list provided please")

    drop = OptionMenu(w4,clicked,6,7,8,9,10,11,12,13)
    drop.config(bg="#a91b0d",fg="white")
    drop.grid(row=0,column=0)
    
    drop_button = Button(w4, text="OK", command=show_article4,bg="#86dc3d")
    drop_button.grid(row=0,column=1)


def main():
    global image_label
    root = Toplevel(bg="#ffe5b4")

    gdimg = ImageTk.PhotoImage(Image.open("ms.png"))
    dfimg = ImageTk.PhotoImage(Image.open("df.png"))
    janesimg = ImageTk.PhotoImage(Image.open("janes.png"))
    lhimg = ImageTk.PhotoImage(Image.open("lockheed.png"))

    image_list = [gdimg,dfimg,janesimg,lhimg]

    title_label = Label(root,text="Select Website : ",font=("Ariel","15","bold"),fg="red",bg="#8ad8e6")
    title_label.grid(row=0,column=0,columnspan=3)

    image_label = Label(root,image=gdimg)
    image_label.grid(row=1,column=0,columnspan=3)

    def forward(image_number):
        global image_label
        global button_forward
        global button_back
        
        image_label.grid_forget()
        image_label = Label(root,image=image_list[image_number-1])
        button_forward = Button(root,text = ">> (Next)",command=lambda:forward(image_number+1),bg="#86dc3d")
        button_back = Button(root,text = "<< (Previous)",command=lambda:back(image_number-1),bg="#86dc3d")
        
        if image_number == 4:
            button_forward = Button(root,text=">> (Next)",state=DISABLED,bg="#86dc3d")
        
        if image_number == 1:
            website_button['command'] = w1
        if image_number == 2:
            website_button['command'] = w2
        if image_number == 3:
            website_button['command'] = w3
        if image_number == 4:
            website_button['command'] = w4
            
        image_label.grid(row=1,column=0,columnspan=3) 
        website_button.grid(row=2,column = 0,columnspan=3)          
        button_back.grid(row=3,column=0)
        button_forward.grid(row=3,column=2)
        
    def back(image_number):
        global image_label
        global button_forward
        global button_back
        
        image_label.grid_forget()
        image_label = Label(root,image=image_list[image_number-1])
        button_forward = Button(root,text = ">> (Next)",command=lambda:forward(image_number+1),bg="#86dc3d")
        button_back = Button(root,text = "<< (Previous)",command=lambda:back(image_number-1),bg="#86dc3d")
        
        if image_number == 1:
            button_back = Button(root,text="<< (Previous)",state=DISABLED,bg="#86dc3d")
            
        if image_number == 1:
            website_button['command'] = w1
        if image_number == 2:
            website_button['command'] = w2
        if image_number == 3:
            website_button['command'] = w3
        if image_number == 4:
            website_button['command'] = w4
            
        image_label.grid(row=1,column=0,columnspan=3) 
        website_button.grid(row=2,column = 0,columnspan=3)  
        button_back.grid(row=3,column=0)
        button_forward.grid(row=3,column=2)
    
    website_button = Button(root,text = "Open News",bg="#ffdb58",command=w1)
    website_button.grid(row=2,column = 0,columnspan=3)

    button_back = Button(root,text = "<< (Previous)",command=back,bg="#86dc3d",state = DISABLED)
    button_back.grid(row=3,column=0)

    button_forward = Button(root,text = ">> (Next)",bg="#86dc3d",command=lambda:forward(2))
    button_forward.grid(row=3,column=2)

    button_exit = Button(root,text = "Exit Application",bg="#ffdb58",command=login.destroy)
    button_exit.grid(row=3,column=1)


def submit():
    username = username_var.get()
    password = password_var.get()
    cursor = mycon.cursor()
    cursor.execute(f'select * from up where username = "{username}" and password = "{password}"')
    data = cursor.fetchone()
    if not data:
        messagebox.showerror("GMV NEWS","Enter Valid Username and Password")
        username_var.set("")
        password_var.set("")
    elif username == data[0] and password == data[1]:
        login.iconify()
        messagebox.showinfo("GMV NEWS","Login Successful")
        main()

    else:
        messagebox.showerror("GMV NEWS","Enter Valid Username and Password")
        username_var.set("")
        password_var.set("")
    cursor.close()


my_img = ImageTk.PhotoImage(Image.open("fighter jet 2.png"))
labelimg1 = Label(login,image=my_img)
labelimg1.grid(row=0,column=0,columnspan=2)

label1 = Label(login, text="LOGIN",font=("Ariel",13,"bold"),fg="red",bg="#8ad8e6")
label1.grid(row=1,column=0,columnspan=2)

usernamelabel = Label(login, text="Username",bg="#8ad8e6")
usernamelabel.grid(row=2, column=0)

usernameentry = Entry(login,textvariable=username_var)
usernameentry.grid(row=2,column=1)

passwordlabel = Label(login, text="Password",bg="#8ad8e6")
passwordlabel.grid(row=3, column=0)

passwordentry = Entry(login,textvariable=password_var,show="*")
passwordentry.grid(row=3,column=1)

registerbutton = Button(login,text="Register",bg="#ffdb58",command = register)
registerbutton.grid(row=4,column=0)

submitbutton = Button(login,text="Submit",bg="#ffdb58",command = submit)
submitbutton.grid(row=4,column=1)

login.mainloop()

mycon.close()
