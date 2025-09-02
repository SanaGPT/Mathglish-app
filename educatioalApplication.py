#in the name of god
#Sana Sadat Hosseini
#Maryam Mirzakhani school
#7th grade
#aim : to write an app about mathematics and English
#mathematic part and section includes gcd,lcd,power,second root, equation, counters and prime numbers

#importing modules
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
import sympy as sp
from sympy import Eq,solve,symbols
import pyttsx3
from tkinter import ttk
from sympy import gcd
import json
import os
from tkinter import font

#creating a class to show results
class Response:
    def __init__(self, response, window):
        self.response = response
        self.window = window

    def result(self):
        label = tk.Label(self.window, text = f'نتیجه:{self.response}')
        label.pack(pady = 5)

#creating main window
main_window = tk.Tk()
main_window.geometry('250x250')
main_window.configure(bg = 'lightblue')
style = ttk.Style()
style.theme_use('vista')

#creating a variable including font
farsi_font = font.Font(family="Roya", size=14)

#defining english function
# Initialize text-to-speech
tts = pyttsx3.init()

# Dictionary file
DICT_FILE = "dictionary.json"

def load_dict():
    """Load dictionary from JSON file"""
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_dict(data):
    """Save dictionary to JSON file"""
    with open(DICT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def english():
    # Create main window
    eng_window = tk.Toplevel()
    eng_window.title("English Dictionary")
    eng_window.geometry("400x500")
    eng_window.configure(bg = 'blue')

    # Treeview for words
    tree = ttk.Treeview(eng_window)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    # Load existing words
    data = load_dict()
    for word in data:
        parent = tree.insert("", "end", text=word)
        tree.insert(parent, "end", text="🔊 پخش صدا")
        tree.insert(parent, "end", text="📖 معنی")
        tree.insert(parent, "end", text="✏️ مثال")
        tree.insert(parent, 'end', text='حذف کلمه')

    # Add new word function
    def add_word():
        word = word_entry.get().strip()
        if word and word not in data:
            data[word] = {"meaning": "", "example": ""}
            save_dict(data)
            parent = tree.insert("", "end", text=word)
            tree.insert(parent, "end", text="🔊 پخش صدا")
            tree.insert(parent, "end", text="📖 مثال")
            tree.insert(parent, "end", text="✏️ معنی")
            tree.insert(parent, "end", text="حذف کلمه")
            word_entry.delete(0, 'end')

    # Word entry frame
    entry_frame = tk.Frame(eng_window)
    entry_frame.pack(pady=5)
    
    word_entry = tk.Entry(entry_frame, width=25)
    word_entry.pack(side='left', padx=5)
    
    add_btn = tk.Button(entry_frame, text="افزودن کلمه",font = farsi_font, command=add_word, bg = 'darkblue', fg = 'white')
    add_btn.pack(side='left')

    # Handle tree item clicks
    def on_tree_click(event):
        item = tree.focus()
        parent = tree.parent(item)
        
        if parent:  # If it's a child item (not main word)
            word = tree.item(parent, "text")
            action = tree.item(item, "text")
            
            if "🔊 پخش صدا" in action:
                tts.say(word)
                tts.runAndWait()
                
            elif "📖 معنی" in action:
                show_detail_window(word, "meaning", data[word]["meaning"])
                
            elif "✏️ مثال" in action:
                show_detail_window(word, "example", data[word]["example"])

            elif "حذف کلمه" in action:  # Handle delete
                if messagebox.askyesno("تایید حذف", f"آیا مطمئنید می‌خواهید '{word}' را حذف کنید؟"):
                    # Remove from treeview
                    tree.delete(parent)
                    # Remove from dictionary data
                    data.pop(word)
                    # Save updated dictionary
                    save_dict(data)
                    messagebox.showinfo("حذف شد", f"کلمه '{word}' با موفقیت حذف شد.")

    tree.bind("<Button-1>", on_tree_click)

    def show_detail_window(word, field, current_value):
        """Show window for editing meaning/example"""
        win = tk.Toplevel()
        win.title(f"{word} - {field.capitalize()}")
        win.geometry("300x200")
        win.configure(bg = 'darkblue')
        
        tk.Label(win, text=f"{field.capitalize()} for '{word}':").pack(pady=10)
        
        text_box = tk.Text(win, height=5, width=30)
        text_box.pack(pady=5)
        text_box.insert("1.0", current_value)
        
        def save_changes():
            new_value = text_box.get("1.0", "end-1c").strip()
            data[word][field] = new_value
            save_dict(data)
            win.destroy()
            messagebox.showinfo("Saved", f"{field.capitalize()} updated!")
        
        tk.Button(win, text="Save", command=save_changes).pack(pady=5)

    # Bind Enter key to add word
    eng_window.bind('<Return>',lambda e : add_word())

def math():
    #defining equation function
    def equation():
        #defining submit 4 
        def submit4(event = None):

            theEquation = equationInput.get()

            #clearing entry widget
            equationInput.delete(0, 'end')

            try:

                #defining x symbol
                symbol_x = symbols('x')

                #dividing the equation to two parts
                right, left = theEquation.split('=')

                #solving each part
                rightExpression = sp.sympify(right)
                leftExpression = sp.sympify(left)
                eq = Eq(rightExpression, leftExpression)

                solving = solve(eq,symbol_x)

                #displaying the result
                result = Response(solving[0], equationScreen)
                result.result()

            except ValueError:
                messagebox.showerror('ورودی نا معتبر')

        #creating the screen
        equationScreen = tk.Toplevel()
        equationScreen.geometry('500x250')
        equationScreen.configure(bg = 'pink')

        #creating label
        message = tk.Label(equationScreen, text = 'معادله مورد نظر را وارد کنید:', font = farsi_font)
        message.pack(pady = 5)

         #receiving entry
        equationInput = tk.Entry(equationScreen)
        equationInput.pack(pady = 5)

        #confirming and rendering the response
        equation_button = tk.Button(equationScreen, text = 'تایید',font = farsi_font, command = submit4)
        equation_button.pack(pady = 5)

        #connecting enter key to submit function
        equationScreen.bind('<Return>',submit4)

    #defining lcd function
    def lcd():
        #defining submit4
        def submit4(event1 = None):
            try:

                number1,number2 = int(lcdInput.get()), int(lcdInput1.get())

                #clearing entry widget
                lcdInput.delete(0, 'end')
                lcdInput1.delete(0, 'end')

                #the response
                result = number1 * number2 // gcd(number1, number2)

                #displaying the result
                response = Response(result, lcdscreen)
                response.result()
            
            except ValueError:
                messagebox.showerror('ورودی نا معتبر')

        lcdscreen = tk.Toplevel()
        lcdscreen.geometry('500x250')
        lcdscreen.configure(bg = 'gray')

        #creating label
        message = tk.Label(lcdscreen, text = 'عدد اول را وارد کنید:', font= farsi_font)
        message.pack(pady = 5)

         #receiving entry
        lcdInput = tk.Entry(lcdscreen)
        lcdInput.pack(pady = 5)

        message1 = tk.Label(lcdscreen, text = 'عدد دوم را وارد کنید:', font= farsi_font)
        message1.pack(pady = 5)

         #receiving entry
        lcdInput1 = tk.Entry(lcdscreen)
        lcdInput1.pack(pady = 5)

        #confirming and rendering the response
        lcd_Button = tk.Button(lcdscreen, text = 'تایید',font= farsi_font, command = submit4)
        lcd_Button.pack(pady = 5)

        #connecting enter key to submit4 function
        lcdscreen.bind("<Return>", submit4)

    #defining counter function
    def counter():
        #defining sumbmit4 
        def submit4(event2 = None):
            try:
                number = int(counterInput.get())

                #clearing entry widget
                counterInput.delete(0, 'end')

                #creating the result list
                result = [x for x in range(1, number + 1) if number % x == 0]

                #demonstrating the result
                retort = Response(result, counterScreen)
                retort.result()

            except ValueError:
                messagebox.showerror('ورودی نا معتبر')

        #creating the screen
        counterScreen = tk.Toplevel()
        counterScreen.geometry('500x250')
        counterScreen.configure(bg ='orange')

        #creating label
        message = tk.Label(counterScreen, text = 'عدد مورد نظر را وارد کنید:', font= farsi_font)
        message.pack(pady = 5)

         #receiving entry
        counterInput = tk.Entry(counterScreen)
        counterInput.pack(pady = 5)

        #confirming and rendering the response
        counter_button = tk.Button(counterScreen, text = 'تایید',font = farsi_font ,command = submit4)
        counter_button.pack(pady = 5)

        #connecting enter key to the submit4
        counterScreen.bind('<Return>', submit4)

    #definig gcdfunction
    def gcdfunction():
        #defining submit 4 
        def submit4(event3 = None):

            try:

                number1,number2 = int(gcdInput.get()), int(gcdInput1.get())

                #clearing entry widget
                gcdInput.delete(0, 'end')
                gcdInput1.delete(0, 'end')
            
                #displaying the result
                result = Response(gcd(number2, number1), gcdscreen)
                result.result()

            except ValueError:
                messagebox.showerror('ورودی نا معتبر')
    
        gcdscreen = tk.Toplevel()
        gcdscreen.geometry('500x250')
        gcdscreen.configure(bg = 'brown')

        #creating label
        message = tk.Label(gcdscreen, text = 'عدد اول را وارد کنید:', font= farsi_font)
        message.pack(pady = 5)

         #receiving entry
        gcdInput = tk.Entry(gcdscreen)
        gcdInput.pack(pady = 5)

        message1 = tk.Label(gcdscreen,text = 'عدد دوم را وارد کنید:', font= farsi_font)
        message1.pack(pady = 5)

         #receiving entry
        gcdInput1 = tk.Entry(gcdscreen)
        gcdInput1.pack(pady = 5)

        #confirming and rendering the response
        gcd_Button = tk.Button(gcdscreen, text = 'تایید',font = farsi_font ,command = submit4)
        gcd_Button.pack(pady = 5)

        #connect key enter to submit4
        gcdscreen.bind('<Return>', submit4)

    #defining power function
    def power():
        #defining submit4
        def submit4(event4 = None):
            try:
                number1 = int(powerInput.get())
                number2 = int(powerInput1.get())

                #clearing entry widget
                powerInput.delete(0, 'end')
                powerInput1.delete(0, 'end')

                result = Response(number1 ** number2, powerscreen)
                result.result()

            except ValueError:
                messagebox.showerror('ورودی نا معتبر')

        powerscreen = tk.Toplevel()
        powerscreen.geometry('500x250')
        powerscreen.configure(bg = 'lightgreen')

        #creating label
        message = tk.Label(powerscreen, text = 'پایه را وارد کنید:', font = farsi_font)
        message.pack(pady = 5)

         #receiving entry
        powerInput = tk.Entry(powerscreen)
        powerInput.pack(pady = 5)

        message1 = tk.Label(powerscreen, text = 'توان را وارد کنید:', font= farsi_font)
        message1.pack(pady = 5)

         #receiving entry
        powerInput1 = tk.Entry(powerscreen)
        powerInput1.pack(pady = 5)

        #confirming and rendering the response
        power_Button = tk.Button(powerscreen, text = 'تایید',font= farsi_font, command = submit4)
        power_Button.pack(pady = 5)

        #connecting enter key to submit4 func
        powerscreen.bind('<Return>', submit4)

    #defining second root computing function
    def secondroot():
        #defining submit4 function
        def submit4(event5 = None):
            try:
                number = int(secondrootInput.get())

                #clearing entry widget
                secondrootInput.delete(0, 'end')
                
                #the result
                result = Response(number ** 0.5, secondrootScreen)
                result.result()

            except ValueError:
                messagebox.showerror('ورودی نا معتبر!')

        #creating the screen
        secondrootScreen = tk.Toplevel()
        secondrootScreen.geometry('500x250')
        secondrootScreen.configure(bg = 'purple')

        #creating label
        message = tk.Label(secondrootScreen, text = 'عدد مورد نظر را وارد کنید:', font = farsi_font)
        message.pack(pady = 5)

         #receiving entry
        secondrootInput = tk.Entry(secondrootScreen)
        secondrootInput.pack(pady = 5)

        #confirming and rendering the response
        secondroot_Button = tk.Button(secondrootScreen, text = 'تایید',font = farsi_font, command = submit4)
        secondroot_Button.pack(pady = 5)

        #connecting enter key to submit4 func 
        secondrootScreen.bind('<Return>', submit4)

    #defining prime function
    def prime():
        #defining submit3
        def submit3(event6 = None):
            try:
                userinput = int(primeInput.get())

                #clearing entry widget
                primeInput.delete(0, 'end')

                #creatig a list of its counters
                counters = [i for i in range(1, userinput + 1) if userinput % i == 0]

                if len(counters) == 2:
                    if 1 and userinput in counters:
                        response = tk.Label(prime_window, text = 'عدد اول است', font = farsi_font)
                        response.pack(pady = 5)

                else:
                    response1 = tk.Label(prime_window, text = 'عدد اول نیست', font = farsi_font)
                    response1.pack(pady = 5)

            except ValueError:
                messagebox.showerror('ورودی نا معتبر')

        #creating the main screen
        prime_window = tk.Toplevel()
        prime_window.geometry('500x250')
        prime_window.configure(bg = 'lightblue')

        #creating a label
        message = tk.Label(prime_window, text = ':عدد مورد نظر را وارد کنید', font= farsi_font)
        message.pack(pady = 5)

        #receiving entry
        primeInput = tk.Entry(prime_window)
        primeInput.pack(pady = 5)

        #confirming and rendering the response
        prime_Button = tk.Button(prime_window, text = 'تایید',font= farsi_font, command = submit3)
        prime_Button.pack(pady = 5)

        #connecting enter key to submit3 func
        prime_window.bind('<Return>', submit3)

    #creating the screen
    math_window = tk.Toplevel()
    math_window.geometry('400x270')

    #creating buttons
    primeButton = tk.Button(math_window, text = 'اعداد اول',font= farsi_font, bg = 'light blue', command= prime)
    primeButton.pack(fill = 'both')

    secondrootButton = tk.Button(math_window, text = 'محاسبه ریشه دوم عدد',font= farsi_font, bg = 'purple', command = secondroot)
    secondrootButton.pack(fill = 'both')

    powerButton = tk.Button(math_window, text = 'محاسبه توان',font = farsi_font, bg = 'light green', command = power)
    powerButton.pack(fill = 'both')

    gcdButton = tk.Button(math_window, text = 'محاسبه ب.م.م',font =farsi_font ,bg = 'brown', command =gcdfunction)
    gcdButton.pack(fill = 'both')

    counterButton = tk.Button(math_window, text = 'محاسبه شمارنده',font= farsi_font , bg = 'orange',command = counter)
    counterButton.pack(fill = 'both')

    lcdButton = tk.Button(math_window, text = 'محاسبه ک.م.م',font = farsi_font,bg = 'gray', command = lcd)
    lcdButton.pack(fill = 'both')

    equationButton = tk.Button(math_window, text = 'حل معادله',font= farsi_font, bg = 'pink', command = equation)
    equationButton.pack(fill = 'both')

#creating associated buttons
english_button = tk.Button(main_window, text = 'انگلیسی',font = farsi_font, width= 5, height= 5 , fg = 'white', bg = 'black', command = english)
english_button.pack(fill = 'both')

math_button = tk.Button(main_window, text = 'ریاضی',font = farsi_font, width= 5, height= 5 ,command = math)
math_button.pack(fill = 'both')

main_window.mainloop()