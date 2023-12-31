import gtts, pydub, ffmpeg, os, threading, configparser
from pydub import AudioSegment
from pydub.playback import play
from tkinter import *
from tkinter import ttk
from datetime import datetime

print("Voice gTTS v1.5 by glebanovsky")
config = configparser.ConfigParser()
config.read("./lang/en.ini", encoding="utf-8")

def setting_menu(): #Окно настроек
    def dismiss(setting): #Закрытие
        setting.grab_release() 
        setting.destroy()
        
    def themeselected(event): #Темы
        selected = themecombobox.get()
        config.read("./theme/"+selected, encoding="utf-8")
        root.config(bg=config.get("WINDOW", "root"))
        setting.config(bg=config.get("WINDOW", "setting"))
        ttk.Style().configure(".", font = config.get("STYLE", "font"), foreground=config.get("STYLE", "fg"), background=config.get("STYLE", "bg"))
        ttk.Style().configure("sfcheckbutton", font = config.get("STYLE", "font"), foreground=config.get("STYLE", "fg"), background=config.get("STYLE", "bg"))
        ttk.Style().configure("Base.TCombobox", foreground=config.get("COMBOBOX", "fg"), background=config.get("COMBOBOX", "bg"))
        textfield.config(bg=config.get("TEXTFIELD", "bg"), fg=config.get("TEXTFIELD", "fg"))
        playbutton.configure(foreground=config.get("BUTTON", "fg"),background=config.get("BUTTON", "bg"))
        
    def langselected(event): #Язык
        selected = langcombobox.get()
        config.read("./lang/"+selected, encoding="utf-8")
        themelabel["text"] = config.get("LABEL", "themelabel")
        langlabel["text"] = config.get("LABEL", "langlabel")
        label1["text"] = config.get("LABEL", "label1")
        sizelabel["text"] = config.get("LABEL", "sizelabel")
        main_menu.entryconfigure(0, label=config.get("MENU", "setting"))
        main_menu.entryconfigure(1, label=config.get("MENU", "window"))
        playbutton.configure(text=config.get("BUTTON", "play"))
        sfcheckbutton.configure(text=config.get("CHECKBUTTON", "savefile"))

    def sizeselected(event):
        selected = sizecombobox.get()
        if selected == "320x240":
            root.geometry(selected)
            textfield.configure(height=6)
            textfield.config(font="Verdana 13")
            playbutton.place(x=225, y=125)

        elif selected == "800x600":
            root.geometry(selected)
            textfield.configure(height=13)
            textfield.config(font="Verdana 22")
            playbutton.place(x=705, y=460)

        else:
            root.geometry(selected)
            textfield.configure(height=15)
            textfield.config(font="Verdana 26")
            playbutton.place(x=930, y=635)
            
      
    themelist = []
    langlist = []
    sizelist = ["320x240", "800x600", "1024x768"]

    for filename in os.listdir("./lang"):
        langlist.append(filename)
        
    for filename in os.listdir("./theme"):
        themelist.append(filename)
    
    setting = Toplevel()
    setting.title("Setting")
    setting.geometry("400x250")
    setting.resizable(False, False)
    setting.protocol("WM_DELETE_WINDOW", lambda: dismiss(setting))
    
    #выбор темы
    themelabel = Label(setting, text=config.get("LABEL", "themelabel"))
    themelabel.pack(anchor=NW)

    themecombobox = ttk.Combobox(setting, values=themelist, state="readonly", style="Base.TCombobox")
    themecombobox.pack(anchor=NW)
    themecombobox.current(0)
    themecombobox.bind("<<ComboboxSelected>>", themeselected)

    #Выбор языка
    langlabel = Label(setting, text=config.get("LABEL", "langlabel"))
    langlabel.pack(anchor=NW)

    langcombobox = ttk.Combobox(setting, values=langlist, state="readonly", style="Base.TCombobox")
    langcombobox.pack(anchor=NW)
    langcombobox.current(0)
    langcombobox.bind("<<ComboboxSelected>>", langselected)

    #Выбор размера
    sizelabel = Label(setting, text=config.get("LABEL", "sizelabel"))
    sizelabel.pack(anchor=NW)

    sizecombobox = ttk.Combobox(setting, values=sizelist, state="readonly", style="Base.TCombobox")
    sizecombobox.pack(anchor=NW)
    sizecombobox.current(1)
    sizecombobox.bind("<<ComboboxSelected>>", sizeselected)
    
    setting.grab_set()
    
class app(Tk):
    def play():
        def playaudio():
            print("--------------------------------------------------------\nVoice acting has begun")
            try:
                textinput = textfield.get("1.0", "end")
                date = datetime.now().strftime("%d%m%Y%H%M%S")
                filename = "saves/voicegtts"+date+".mp3"
                lang = combobox.get()
                print("Language: "+lang)
                tts = gtts.gTTS(textinput, lang=lang)
                tts.save(filename)
                print("Editing sound with pydub")
                sound = AudioSegment.from_file(filename, format="mp3")
                float_value = pitchscale.get()
                new_value = round(float_value, 1)
                octaves = new_value
                print("Pitch: "+str(octaves))
                new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
                audio = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                os.remove(filename)
                print("Audio playback...")
                play(audio)
                print("... End \n--------------------------------------------------------")
            except AssertionError:
                print("Error: \nThe input field is empty \n--------------------------------------------------------")
            if savefile.get() == 1:
               audio.export(filename, format="mp3")
               print("The audio file was successfully saved to the saves folder")
               print("--------------------------------------------------------")
        thread = threading.Thread(target=playaudio)
        thread.start()
        

def pitch(value):
    float_value = float(value)
    new_value = round(float_value, 1)
    pitchlabel["text"] = new_value

root = Tk()
root.title("VoiceGTTS")
root.geometry("800x600")
root.resizable(False, False)
icon = PhotoImage(file = "icon.png")
root.iconphoto(True, icon)

root.option_add("*tearOff", FALSE)


#Стандартные стили
root.config(bg="#e3e3e3")
ttk.Style().configure(".", font ="Verdana 16", foreground="black", background="#e3e3e3")
textfield = Text(root, height=13, wrap="word", font="Verdana 22", bg="white", fg="black")
combobox_style = ttk.Style()
combobox_style.configure("Base.TCombobox", font = "Verdana 12", foreground="black", background="white")

#Меню
main_menu = Menu()

main_menu.add_cascade(label=config.get("MENU", "setting"), command=setting_menu)
main_menu.add_cascade(label=config.get("MENU", "window"))

#Список языков в combobox
config.read("gtts.ini")
_langlist = config.get("LANG", "langlist")
_langlist.split(" ")


#Текстовое поле
textfield = Text(root, height=13, wrap="word", font="Verdana 22")
textfield.pack(anchor=N)

#Кнопка Play
playbutton = Button(root, text=config.get("BUTTON", "play"), command=app.play, width=12, height=2)
playbutton.place(x=705, y=460)

#Сохранять?
savefile = IntVar()
sfcheckbutton = ttk.Checkbutton(text=config.get("CHECKBUTTON", "savefile"), variable=savefile)
sfcheckbutton.pack(side=RIGHT)
#sfcheckbutton.select()

#Выбор языка
combobox = ttk.Combobox(root, values=_langlist, state="readonly", style="Base.TCombobox")
combobox.pack(anchor=NW)
combobox.current(0)

label1 = ttk.Label(text=config.get("LABEL", "label1"))
label1.pack(anchor=NW)

#Питч звука
pitchscale = ttk.Scale(root, orient=HORIZONTAL, length=145, from_=-1, to =1, value =0, command=pitch)
pitchscale.pack(anchor=NW)

#Отображения значения питча
pitchlabel = ttk.Label(root, text="0.0")
pitchlabel.pack(anchor=W)


root.config(menu=main_menu)
root.mainloop()



