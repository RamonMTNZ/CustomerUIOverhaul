import tkinter as tk
from tkinter import font as tkfont
import tkinter.ttk as ttk
from main.customer.customer import Customer
from main.customer import Login
from main.utils import dialog_warning



customer_instance = None

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)



        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        allframes = [LoginPage, MenuPage, RentPage, ReturnPage, RechargePage,ReportPage]
        for F in allframes:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Frame.config(self, background='#243447', height='540', width='960')
        self.label_1 = tk.Label(self)
        self.label_1.config(background='#243347', font='{Arial} 24 {}', foreground='#c0c0c0', relief='flat')
        self.label_1.config(text='Welcome to 2i Bike Rental')
        self.label_1.place(anchor='n', relx='0.5', rely='0.05', x='0', y='0')
        self.entry_1 = tk.Entry(self)
        self.entry_1.config(background='#c0c0c0')
        self.entry_1.place(anchor='n', height='20', relx='0.55', rely='0.2', width='150', x='0', y='0')
        self.entry_2 = tk.Entry(self)
        self.entry_2.config(background='#c0c0c0', show='•')
        self.entry_2.place(anchor='n', height='20', relx='0.55', rely='0.25', width='150', x='0', y='0')
        self.label_2 = tk.Label(self)
        self.label_2.config(background='#243447', font='{Arial} 10 {}', foreground='#c0c0c0', takefocus=False)
        self.label_2.config(text='Username:')
        self.label_2.place(anchor='n', relx='0.4', rely='0.2', x='0', y='0')
        self.label_3 = tk.Label(self)
        self.label_3.config(background='#243447', font='{Arial} 10 {}', foreground='#c0c0c0', text='Password:')
        self.label_3.place(anchor='n', relx='0.4', rely='0.25', x='0', y='0')
        self.button_1 = tk.Button(self, command=lambda: login_progress(Login.login(self.entry_1, self.entry_2)))
        self.button_1.config(background='#c0c0c0', text='Log In')
        self.button_1.place(anchor='n', relx='0.96', rely='0.95', width='70', x='0', y='0')


        def login_progress(login_result):
            if login_result:
                self.controller.show_frame("MenuPage")
            else:
                dialog_warning("Wrong username or password!")
            self.entry_1.delete('0', 'end')
            self.entry_2.delete('0', 'end')






class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.button_2 = tk.Button(self)
        self.button_2.config(justify='left', text='Rent', command=lambda: controller.show_frame("RentPage"))
        self.button_2.pack(side='top')
        self.button_3 = tk.Button(self)
        self.button_3.config(text='Return', command=lambda: controller.show_frame("ReturnPage"))
        self.button_3.pack(side='top')
        self.button_4 = tk.Button(self)
        self.button_4.config(text='Recharge', command=lambda: controller.show_frame("RechargePage"))
        self.button_4.pack(side='top')
        self.button_5 = tk.Button(self)
        self.button_5.config(text='Report', command=lambda: controller.show_frame("ReportPage"))
        self.button_5.pack(side='top')
        self.button_6 = tk.Button(self)
        self.button_6.config(text='Quit') # TODO: Make this quit the application
        self.button_6.pack(side='top')
        self.label_4 = tk.Label(self)
        self.label_4.config(text='Temp page!!! ')
        self.label_4.pack(side='top')


class RentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Frame.config(self, background='#243447', height='540', width='960')
        self.button_1 = tk.Button(self)
        self.button_1.config(background='#f4f4f4', text='Accept')
        self.button_1.place(anchor='n', relwidth='0.08', relx='0.86', rely='0.95', x='0', y='0')
        self.button_2 = tk.Button(self)
        self.button_2.config(background='#f4f4f4', text='Cancel')
        self.button_2.place(anchor='n', relwidth='0.08', relx='0.95', rely='0.95', x='0', y='0')
        self.combobox_1 = ttk.Combobox(self)
        self.combobox_1.place(anchor='n', relwidth='0.2', relx='0.5', rely='0.22', x='0', y='0')
        self.label_1 = ttk.Label(self)
        self.label_1.config(anchor='w', background='#243447', font='{Arial} 14 {}', foreground='#ffffff')
        self.label_1.config(text='Rent a bike')
        self.label_1.place(anchor='n', relx='0.5', rely='0.03', x='0', y='0')
        self.label_2 = ttk.Label(self)
        self.label_2.config(background='#243447', font='{Arial} 10 {}', foreground='#ffffff', text='Choose your bike:')
        self.label_2.place(anchor='n', relx='0.5', rely='0.16', x='0', y='0')
        c = Customer("konml", 4000010)
        c.init_rent_interface(self.combobox_1)


class ReturnPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        tk.Frame.config(self, background='#243447', height='540', width='960')
        self.message_1 = tk.Message(self)
        self.message_1.config(background='#243447', font='{Arial} 20 {}', foreground='#ffffff', text='Return Bike')
        self.message_1.place(anchor='n', relx='0.5', rely='0.1', width='200', x='0', y='0')
        self.message_2 = tk.Message(self)
        self.message_2.config(background='#243447', font='{Arial} 14 {}', foreground='#ffffff', pady='100')
        self.message_2.config(text='Your current Bike is: 0000000')
        self.message_2.place(anchor='n', relwidth='0.75', relx='0.5', rely='0.2', x='0', y='0')
        self.button_3 = tk.Button(self)
        self.button_3.config(background='#e1f2f7', font='{Arial} 12 {}', justify='center', relief='flat')
        self.button_3.config(text='Return Bike')
        self.button_3.place(anchor='n', height='40', relx='0.5', rely='0.75', width='200', y='0')

class RechargePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        tk.Frame.config(self, background='#243447', height='540', width='960')


class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        tk.Frame.config(self, background='#243447', height='540', width='960')


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()