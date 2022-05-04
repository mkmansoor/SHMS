# %%
#import modules

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import sqlite3
import datetime
import smtplib
import os
import re


class abstract_class:
    def __init__(self):
        global main_screen
        self.main_screen = Tk()
        self.main_screen.geometry("600x450")
        self.main_screen.title("Account Login")
        Label(text="Welcome to SHMS", bg="green", fg="white",
              width="300", height="2", font=("Calibri", 13)).pack()
        Label(text="").pack()
        Button(text="Docter's Login", height="2",
               width="30", command=self.doc_login).pack()
        Label(text="").pack()
        Button(text="Patient's Login", height="2",
               width="30", command=self.pat_login).pack()
        Label(text="").pack()
        Label(text="").pack()
        Label(text="").pack()
        Label(text="").pack()
        Button(text="Contact Us", height="2", width="30",
               command=self.contact_us).pack()
        Label(text="").pack()

        self.main_screen.mainloop()

    # Designing window for Docter's login
    def doc_login(self):
        global doc_login_screen
        self.doc_login_screen = Toplevel(self.main_screen)
        self.doc_login_screen.title("Docter's Login")
        self.doc_login_screen.geometry("350x300")
        Label(self.doc_login_screen,
              text="Please enter details below to login").pack()
        Label(self.doc_login_screen, text="").pack()

        global doc_username_verify
        global doc_password_verify

        self.doc_username_verify = StringVar()
        self.doc_password_verify = StringVar()

        global doc_username_login_entry
        global doc_password_login_entry

        Label(self.doc_login_screen, text="Username * ").pack()
        self.doc_username_login_entry = Entry(self.doc_login_screen)
        self.doc_username_login_entry.pack()
        Label(self.doc_login_screen, text="").pack()
        Label(self.doc_login_screen, text="Password * ").pack()
        self.doc_password_login_entry = Entry(self.doc_login_screen, show='*')
        self.doc_password_login_entry.pack()
        Label(self.doc_login_screen, text="").pack()
        Button(self.doc_login_screen, text="Login", width=10,
               height=1, command=self.doc_login_verify).pack()
        Label(self.doc_login_screen, text="").pack()

        self.b1 = Button(self.doc_login_screen, text="Docter's Signup",
                         width=20, height=1, command=self.doc_register)
        self.b1.place(x=10, y=250)

        self.b2 = Button(self.doc_login_screen, text="Forgot Password",
                         width=20, height=1, command=self.doc_forgot_password)
        self.b2.place(x=180, y=250)

    # Implementing login verification button
    def doc_login_verify(self):
        global doc_login, doc_pass
        doc_login = self.doc_username_login_entry.get()
    #     print(1)
        global d_un
        d_un = doc_login

        db = sqlite3.connect('shms.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM doc_signup_info where doc_username=? AND doc_password=?",
                       (self.doc_username_login_entry.get(), self.doc_password_login_entry.get()))
        row = cursor.fetchone()

        if row:
            messagebox.showinfo('info', 'login success')
            self.doc_login_screen.destroy()
            # self.doc_final_login()
            self.newWindow = Toplevel(self.main_screen)
            self.b = Doctor(self.newWindow)
        else:
            messagebox.showinfo('info', 'login failed')
            cursor.connection.commit()
            db.close()

    # Designing window for Doctor's registration

    def doc_register(self):
        global doc_register_screen
        self.doc_register_screen = Toplevel(self.main_screen)
        self.doc_register_screen.title("Register")
        self.doc_register_screen.geometry("300x250")

        global doc_username
        global doc_password
        global doc_sp

        global doc_username_entry
        global doc_password_entry
        global doc_sp_entry

        self.doc_username = StringVar()
        self.doc_password = StringVar()
        self.doc_sp = StringVar()

        Label(self.doc_register_screen,
              text="Please enter details below", bg="blue").pack()
        Label(self.doc_register_screen, text="").pack()
        lable = Label(self.doc_register_screen, text="Username * ")
        lable.pack()

        self.doc_username_entry = Entry(
            self.doc_register_screen, textvariable=self.doc_username)
        self.doc_username_entry.pack()

        lable = Label(self.doc_register_screen, text="Password * ")
        lable.pack()

        self.doc_password_entry = Entry(
            self.doc_register_screen, textvariable=self.doc_password, show='*')
        self.doc_password_entry.pack()

        lable = Label(self.doc_register_screen, text="Security Pin * ")
        lable.pack()

        self.doc_sp_entry = Entry(
            self.doc_register_screen, textvariable=self.doc_sp, show='*')
        self.doc_sp_entry.pack()

        Label(self.doc_register_screen, text="").pack()
        Button(self.doc_register_screen, text="Register", width=10,
               height=1, bg="blue", command=self.register_doc_user).pack()
        self.doc_login_screen.destroy()

    # Implementing event on register button
    def register_doc_user(self):
        self.check_counter = 0
        warn = ""
        if self.doc_username.get() == "":
            warn = "Username can't be empty"
        else:
            self.check_counter += 1

        if self.doc_password.get() == "":
            warn = "Password can't be empty"
        else:
            self.check_counter += 1

        if self.doc_sp.get() == "":
            warn = "Security Pin can't be empty"
        else:
            self.check_counter += 1

        if self.check_counter == 3:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("INSERT INTO doc_signup_info VALUES (:doc_username, :doc_password,:doc_sp,NULL,NULL,NULL)", {
                    'doc_username': self.doc_username.get(),
                    'doc_password': self.doc_password.get(),
                    'doc_sp': self.doc_sp.get()
                })
    #             cur.execute("INSERT INTO doc_signup_info VALUES (?,?,NULL)",(doc_username,doc_password))
                con.commit()
                con.close()
                self.doc_register_screen.destroy()
                messagebox.showinfo('confirmation', 'Record Saved')

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def doc_forgot_password(self):
        global doc_forgot_password_screen
        self.doc_forgot_password_screen = Toplevel(self.main_screen)
        self.doc_forgot_password_screen.title("Forgot Password")
        self.doc_forgot_password_screen.geometry("300x250")
        Label(self.doc_forgot_password_screen, text="Forgot Password").pack()

        global doc_username
        global doc_sp
        global doc_np

        global doc_username_entry
        global doc_sp_entry
        global doc_np_entry

        self.doc_username = StringVar()
        self.doc_sp = StringVar()
        self.doc_np = StringVar()

        Label(self.doc_forgot_password_screen, text="Forgot Password").pack()
        lable = Label(self.doc_forgot_password_screen, text="Username * ")
        lable.pack()

        self.doc_username_entry = Entry(
            self.doc_forgot_password_screen, textvariable=self.doc_username)
        self.doc_username_entry.pack()

        lable = Label(self.doc_forgot_password_screen,
                      text="Input Security Pin * ")
        lable.pack()
        lable = Label(self.doc_forgot_password_screen,
                      text="(Only Numerics Allowed)* ")
        lable.pack()

        self.doc_sp_entry = Entry(
            self.doc_forgot_password_screen, textvariable=self.doc_sp)
        self.doc_sp_entry.pack()

        lable = Label(self.doc_forgot_password_screen,
                      text="Enter New Password * ")
        lable.pack()

        self.doc_np_entry = Entry(
            self.doc_forgot_password_screen, textvariable=self.doc_np)
        self.doc_np_entry.pack()

        Button(self.doc_forgot_password_screen, text="Register", width=10,
               height=1, bg="blue", command=self.register_doc_np).pack()

    def register_doc_np(self):
        self.check_counter = 0
        warn = ""
        r = ""
        if self.doc_username.get() == "":
            warn = "Username can't be empty"
        else:
            self.check_counter += 1

        if self.doc_sp.get() == "":
            warn = "Can't be empty"
        else:
            self.a = self.doc_sp.get()
            con = sqlite3.connect('shms.db')
            cur = con.cursor()
            cur.execute(
                "SELECT doc_sp FROM doc_signup_info WHERE  doc_username=? ", (self.doc_username.get(),))
            r = cur.fetchall()
            r1 = str(r)
#             print(r1)
            con.commit()
            con.close()
            self.i = re.sub("[(,'')\[\]]", "", r1)
#             print(self.i)
            if(self.i == self.a):
                self.check_counter += 1
            else:
                messagebox.showerror(
                    '', "Either Username or password is incorrect")

        if self.check_counter == 2:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("UPDATE doc_signup_info SET doc_password = ? WHERE  doc_username=? ",
                            (self.doc_np.get(), self.doc_username.get()))
    #             cur.execute("INSERT INTO doc_signup_info VALUES (?,?,NULL)",(doc_username,doc_password))
                con.commit()
                con.close()
                messagebox.showinfo('confirmation', 'Record Saved')

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)
            # Designing final window for Docter's login

    def doc_disable_button(self):
        self.doc_final_login_screen.destroy()
        messagebox.showinfo('confirmation', 'Logout Successfully')

    def pat_login(self):
        global pat_login_screen
        self.pat_login_screen = Toplevel(self.main_screen)
        self.pat_login_screen.title("Patient's Login")
        self.pat_login_screen.geometry("350x300")
        Label(self.pat_login_screen,
              text="Please enter details below to login").pack()
        Label(self.pat_login_screen, text="").pack()

        global pat_username_verify
        global pat_password_verify

        self.pat_username_verify = StringVar()
        self.pat_password_verify = StringVar()

        global pat_username_login_entry
        global pat_password_login_entry

        Label(self.pat_login_screen, text="Username * ").pack()
        self.pat_username_login_entry = Entry(self.pat_login_screen)
        self.pat_username_login_entry.pack()
        Label(self.pat_login_screen, text="").pack()
        Label(self.pat_login_screen, text="Password * ").pack()
        self.pat_password_login_entry = Entry(self.pat_login_screen, show='*')
        self.pat_password_login_entry.pack()
        Label(self.pat_login_screen, text="").pack()
        Button(self.pat_login_screen, text="Login", width=10,
               height=1, command=self.pat_login_verify).pack()
        Label(self.pat_login_screen, text="").pack()

        self.b1 = Button(self.pat_login_screen, text="Patient's Signup",
                         width=20, height=1, command=self.pat_register)
        self.b1.place(x=10, y=250)

        self.b2 = Button(self.pat_login_screen, text="Forgot Password",
                         width=20, height=1, command=self.pat_forgot_password)
        self.b2.place(x=180, y=250)

    # Implementing event on pationt's login button

    def pat_login_verify(self):
        global login_un, login_pass
        self.login_un = self.pat_username_login_entry.get()
        self.login_pass = self.pat_password_login_entry.get()
        global p_un
        p_un = self.login_un
#         print(self.login_un)

        db = sqlite3.connect('shms.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM pat_signup_info where pat_username=? AND pat_password=?",
                       (self.login_un, self.login_pass))
        row = cursor.fetchone()

        if row:
            messagebox.showinfo('info', 'login success')
#             self.pat_final_login()
            self.newWindow = Toplevel(self.main_screen)
            self.b = Patient(self.newWindow)
            self.pat_login_screen.destroy()
        else:
            messagebox.showinfo('info', 'login failed')
            cursor.connection.commit()
            db.close()

    def pat_register(self):
        global pat_register_screen
        self.pat_register_screen = Toplevel(self.main_screen)
        self.pat_register_screen.title("Register")
        self.pat_register_screen.geometry("300x250")

        global pat_username
        global pat_password
        global pat_sp

        global pat_username_entry
        global pat_password_entry
        global pat_sp

        self.pat_username = StringVar()
        self.pat_password = StringVar()
        self.pat_sp = StringVar()

        Label(self.pat_register_screen,
              text="Please enter details below", bg="blue").pack()
        Label(self.pat_register_screen, text="").pack()
        username_lable = Label(self.pat_register_screen, text="Username * ")
        username_lable.pack()
        self.pat_username_entry = Entry(
            self.pat_register_screen, textvariable=self.pat_username)
        self.pat_username_entry.pack()
        self.pat_password_lable = Label(
            self.pat_register_screen, text="Password * ")
        self.pat_password_lable.pack()
        self.pat_password_entry = Entry(
            self.pat_register_screen, textvariable=self.pat_password, show='*')
        self.pat_password_entry.pack()

        self.pat_sp_lable = Label(
            self.pat_register_screen, text="Security Pin * ")
        self.pat_sp_lable.pack()
        self.pat_sp_entry = Entry(
            self.pat_register_screen, textvariable=self.pat_sp, show='*')
        self.pat_sp_entry.pack()

        Label(self.pat_register_screen, text="").pack()
        Button(self.pat_register_screen, text="Register", width=10,
               height=1, bg="blue", command=self.register_pat_user).pack()
        self.pat_login_screen.destroy()

        # Implementing event on register button


#     def pat_reg_disable_button(self):
#         print(1)
#         self.pat_register_screen.destroy()

    def register_pat_user(self):
        check_counter = 0
        warn = ""
        if self.pat_username.get() == "":
            warn = "Username can't be empty"
        else:
            check_counter += 1

        if self.pat_password.get() == "":
            warn = "Password can't be empty"
        else:
            check_counter += 1

        if self.pat_sp.get() == "":
            warn = "Security Pin can't be empty"
        else:
            check_counter += 1

        if check_counter == 3:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("INSERT INTO pat_signup_info VALUES (:pat_username, :pat_password,:pat_sp,NULL,NULL,NULL,NULL,NULL,NULL,NULL)", {
                    'pat_username': self.pat_username.get(),
                    'pat_password': self.pat_password.get(),
                    'pat_sp': self.pat_sp.get()
                })
    #             cur.execute("INSERT INTO doc_signup_info VALUES (?,?,NULL)",(doc_username,doc_password))
                con.commit()
                con.close()

                messagebox.showinfo('confirmation', 'Record Saved')
                self.pat_register_screen.destroy()
                self.pat_login_screen.destroy()

            except Exception as ep:
                messagebox.showerror('', ep)
                self.pat_register_screen.destroy()
                self.pat_login_screen.destroy()

        else:
            messagebox.showerror('Error', warn)

    def pat_forgot_password(self):
        global pat_forgot_password_screen
        self.pat_forgot_password_screen = Toplevel(self.main_screen)
        self.pat_forgot_password_screen.title("Forgot Password")
        self.pat_forgot_password_screen.geometry("300x250")
        Label(self.pat_forgot_password_screen, text="Forgot Password").pack()

        global pat_username
        global pat_sp
        global pat_np

        global pat_username_entry
        global pat_sp_entry
        global pat_np_entry

        self.pat_username = StringVar()
        self.pat_sp = StringVar()
        self.pat_np = StringVar()

        Label(self.pat_forgot_password_screen, text="Forgot Password").pack()
        lable = Label(self.pat_forgot_password_screen, text="Username * ")
        lable.pack()

        self.pat_username_entry = Entry(
            self.pat_forgot_password_screen, textvariable=self.pat_username)
        self.pat_username_entry.pack()

        lable = Label(self.pat_forgot_password_screen,
                      text="Security Question * ")
        lable.pack()
        lable = Label(self.pat_forgot_password_screen,
                      text="Your favourite color * ")
        lable.pack()

        self.pat_sp_entry = Entry(
            self.pat_forgot_password_screen, textvariable=self.pat_sp)
        self.pat_sp_entry.pack()

        lable = Label(self.pat_forgot_password_screen,
                      text="Enter New Password * ")
        lable.pack()

        self.pat_np_entry = Entry(
            self.pat_forgot_password_screen, textvariable=self.pat_np)
        self.pat_np_entry.pack()

        Button(self.pat_forgot_password_screen, text="Register", width=10,
               height=1, bg="blue", command=self.register_pat_np).pack()

    def register_pat_np(self):
        self.check_counter = 0
        warn = ""
        r = ""
        if self.pat_username.get() == "":
            warn = "Username can't be empty"
        else:
            self.check_counter += 1

        if self.pat_sp.get() == "":
            warn = "Can't be empty"
        else:
            self.a = self.pat_sp.get()
            con = sqlite3.connect('shms.db')
            cur = con.cursor()
            cur.execute(
                "SELECT pat_sp FROM pat_signup_info WHERE  pat_username=? ", (self.pat_username.get(),))
            r = cur.fetchall()
            r1 = str(r)
#             print(r1)
            con.commit()
            con.close()
            self.i = re.sub("[(,'')\[\]]", "", r1)
#             print(self.i)
            if(self.i == self.a):
                self.check_counter += 1
            else:
                messagebox.showerror(
                    '', "Either Username or Password is incorrect")

        if self.check_counter == 2:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("UPDATE pat_signup_info SET pat_password = ? WHERE  pat_username=? ",
                            (self.pat_np.get(), self.pat_username.get()))
                con.commit()
                con.close()
                messagebox.showinfo('confirmation', 'Record Saved')

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)
            # Designing final window for Docter's login

    def contact_us(self):
        global contact_us_screen
        self.contact_us_screen = Toplevel(self.main_screen)
        self.contact_us_screen.title("Contact Us")
        self.contact_us_screen.geometry("400x450")

        # creating the frames in the master
        self.left = Frame(self.contact_us_screen, width=400,
                          height=450, bg='cadet blue')
        self.left.pack(side=LEFT)

        # labels for the window
        self.heading = Label(self.left, text="Contact US",
                             font=('arial 20 bold'), fg='black')
        self.heading.place(x=150, y=20)
        # patients name
        self.name = Label(self.left, text="Name",
                          font=('arial 14 bold'), fg='black')
        self.name.place(x=20, y=100)
        # location
        self.location = Label(self.left, text="Location",
                              font=('arial 14 bold'), fg='black')
        self.location.place(x=20, y=140)

        # phone
        self.phone = Label(self.left, text="Phone Number",
                           font=('arial 14 bold'), fg='black')
        self.phone.place(x=20, y=180)

        # Entries for all labels============================================================
        self.name_ent = Entry(self.left, width=30)
        self.name_ent.place(x=200, y=100)

        self.location_ent = Entry(self.left, width=30)
        self.location_ent.place(x=200, y=140)

        self.phone_ent = Entry(self.left, width=30)
        self.phone_ent.place(x=200, y=180)

        # button to perform a command
        self.submit = Button(self.left, text="Submit Form",
                             width=20, height=2, command=self.add_query)
        self.submit.place(x=200, y=220)

    # funtion to call when the submit button is clicked
    def add_query(self):
        # getting the user inputs
        self.val1 = self.name_ent.get()
        self.val2 = self.location_ent.get()
        self.val3 = self.phone_ent.get()

        # checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '':
            tkinter.messagebox.showinfo("Warning", "Please Fill Up All Boxes")
        else:
            # now we add to the database
            con = sqlite3.connect('shms.db')
            cur = con.cursor()
#             print(12)
            sql = "INSERT INTO 'query' (name,location,phone) VALUES(?,?,?)"
            cur.execute(sql, (self.val1, self.val2, self.val3))
            con.commit()
            con.close()

            messagebox.showinfo(
                "Success", "Our Team will contact you " + str(self.val1))
            self.contact_us_screen.destroy()


# %%
class Doctor:
    def __init__(self, master):
        self.master = master
        self.master.title("Docter's Screen")
        self.master.geometry("600x500+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")

        self.b1 = Button(self.master, text="Send Bill",
                         width=20, height=1, command=self.send_bill)
        self.b1.place(x=10, y=10)
        self.b2 = Button(self.master, text="Update Bill",
                         width=20, height=1, command=self.update_send_bill)
        self.b2.place(x=10, y=50)
        self.b3 = Button(self.master, text="Delete Bill",
                         width=20, height=1, command=self.del_send_bill)
        self.b3.place(x=10, y=90)

        self.b4 = Button(self.master, text="Prescribe Medicine",
                         width=20, height=1, command=self.send_priscription)
        self.b4.place(x=10, y=130)
        self.b5 = Button(self.master, text="Update Prescription",
                         width=20, height=1, command=self.update_send_priscription)
        self.b5.place(x=10, y=170)
        self.b6 = Button(self.master, text="Delete Prescription",
                         width=20, height=1, command=self.del_send_priscription)
        self.b6.place(x=10, y=210)

        self.b7 = Button(self.master, text="Suggest Diet Plan",
                         width=20, height=1, command=self.send_diet_plan)
        self.b7.place(x=10, y=250)
        self.b8 = Button(self.master, text="Update Diet Plan",
                         width=20, height=1, command=self.update_send_diet_plan)
        self.b8.place(x=10, y=290)
        self.b9 = Button(self.master, text="Delete Diet Plan",
                         width=20, height=1, command=self.del_send_diet_plan)
        self.b9.place(x=10, y=330)

        self.b10 = Button(self.master, text="Sugest Lab Test",
                          width=20, height=1, command=self.send_lab_test)
        self.b10.place(x=200, y=10)
        self.b11 = Button(self.master, text="Update Lab Test",
                          width=20, height=1, command=self.update_send_lab_test)
        self.b11.place(x=200, y=50)
        self.b12 = Button(self.master, text="Delete Lab Test",
                          width=20, height=1, command=self.del_send_lab_test)
        self.b12.place(x=200, y=90)

        self.b13 = Button(self.master, text="Update Profile",
                          width=20, height=1, command=self.update_doc_profile)
        self.b13.place(x=200, y=130)

        self.b14 = Button(self.master, text="Send Email",
                          width=20, height=1, command=self.pat_mail)
        self.b14.place(x=200, y=170)

        self.b15 = Button(self.master, text="View Appointment Log",
                          width=20, height=1, command=self.appointment_log)
        self.b15.place(x=200, y=210)

        self.b16 = Button(self.master, text="Download Appointment Log",
                          width=21, height=1, command=self.download_appointment_log)
        self.b16.place(x=197, y=250)

        self.b17 = Button(self.master, text="Log Out", width=20, height=1,
                          fg="white", bg="black", command=self.doc_disable_button)
        self.b17.place(x=100, y=370)

        self.b18 = Button(self.master, text="Delet Account", width=20,
                          height=1, fg="black", bg="red", command=self.del_doc_account)
        self.b18.place(x=100, y=410)

#             self.doc_login_screen.withdraw()
#             self.doc_final_login_screen.attributes("-topmost", True)

        self.frame.pack()
#             print("yes")

    def send_bill(self):
        global send_bill_screen
        self.send_bill_screen = Toplevel(self.master)
        self.send_bill_screen.title("Invoice")
        self.send_bill_screen.geometry("300x250")
        self.send_bill_screen.attributes('-topmost', True)

        global bill

        global bill_entry
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
#                 print(self.a)
            self.t = self.a
#                 print(type(self.t))
        # Dropdown menu options
        options = self.result_set
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(self.send_bill_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.send_bill_screen,
                             text="confirm", command=show).pack()

        self.bill = StringVar()

        Label(self.send_bill_screen,
              text="Please enter details below", bg="blue").pack()
        Label(self.send_bill_screen, text="").pack()
        lable = Label(self.send_bill_screen, text="Consultation Charges * ")
        lable.pack()
        self.bill_entry = Entry(self.send_bill_screen, textvariable=self.bill)
        self.bill_entry.pack()
        Label(self.send_bill_screen, text="").pack()
        Button(self.send_bill_screen, text="send to patient", width=10,
               height=1, bg="blue", command=self.bill_register).pack()

    def bill_register(self):
        self.check_counter = 0
        warn = ""
        self.b = self.bill_entry.get()
        if self.bill_entry.get() == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

        import re
        self.i = re.sub("[(,'')]", "", self.t)
#             print(self.i)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET invoice = ? WHERE  pat_username=? ", (self.b, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.send_bill_screen.destroy()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def update_send_bill(self):
        global update_send_bill_screen
        self.update_send_bill_screen = Toplevel(self.master)
        self.update_send_bill_screen.title("Update Invoice")
        self.update_send_bill_screen.geometry("300x250")
        self.update_send_bill_screen.attributes('-topmost', True)

        global update_bill

        global update_bill_entry
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
#                 print(self.a)
            self.t = self.a
#                 print(type(self.t))
        # Dropdown menu options
        options = self.result_set
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.update_send_bill_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.update_send_bill_screen,
                             text="confirm", command=show).pack()

        self.update_bill = StringVar()

        Label(self.update_send_bill_screen,
              text="Please enter details below", bg="blue").pack()
        Label(self.update_send_bill_screen, text="").pack()
        lable = Label(self.update_send_bill_screen,
                      text="Consultation Charges * ")
        lable.pack()
        self.update_bill_entry = Entry(
            self.update_send_bill_screen, textvariable=self.update_bill)
        self.update_bill_entry.pack()
        Label(self.update_send_bill_screen, text="").pack()
        Button(self.update_send_bill_screen, text="send to patient", width=10,
               height=1, bg="blue", command=self.update_bill_register).pack()

    def update_bill_register(self):
        self.check_counter = 0
        warn = ""
        self.b = self.update_bill_entry.get()
        if self.update_bill_entry.get() == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

        import re
        self.i = re.sub("[(,'')]", "", self.t)
#             print(self.i)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET invoice = ? WHERE  pat_username=? ", (self.b, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.update_send_bill_screen.destroy()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def del_send_bill(self):
        global del_send_bill_screen
        self.del_send_bill_screen = Toplevel(self.master)
        self.del_send_bill_screen.title("Delete Invoice")
        self.del_send_bill_screen.geometry("300x250")
        self.del_send_bill_screen.attributes('-topmost', True)

        global del_bill

        global del_bill_entry
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
#                 print(self.a)
            self.t = self.a
#                 print(type(self.t))
        # Dropdown menu options
        options = self.result_set
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(self.del_send_bill_screen,
                               self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.del_send_bill_screen,
                             text="confirm", command=show).pack()

        self.del_bill = StringVar()

        Label(self.del_send_bill_screen, text="").pack()
        Button(self.del_send_bill_screen, text="Delete Invoice", width=10,
               height=1, bg="blue", command=self.del_bill_register).pack()

    def del_bill_register(self):

        import re
        self.i = re.sub("[(,'')]", "", self.t)

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute(
            "UPDATE pat_signup_info SET invoice = ? WHERE  pat_username=? ", (0, self.i))
        con.commit()
        con.close()
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        messagebox.showinfo('confirmation', 'Invoice Deleted')
        self.del_send_bill_screen.destroy()

        # Send Prescription

    def send_priscription(self):
        self.check_counter = 0
        warn = ""
        global send_priscription_screen
        self.send_priscription_screen = Toplevel(self.master)
        self.send_priscription_screen.title("Priscription")
        self.send_priscription_screen.geometry("300x250")
        self.send_priscription_screen.attributes('-topmost', True)

        global priscription
        global priscription_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
    #         print(a)
            self.t = self.a
    #         print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.send_priscription_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.send_priscription_screen,
                             text="confirm", command=show).pack()

        def printInput():
            global inp
            inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Provided prescription: "+inp)
    #         print (inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.send_priscription_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

#             Button Creation
        self.printButton = tk.Button(self.send_priscription_screen,
                                     text="confirm Priscription",
                                     command=printInput)

        self.printButton.pack()

        self.printButton2 = tk.Button(self.send_priscription_screen,
                                      text="confirm Priscription",
                                      command=self.priscription_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.send_priscription_screen, text="")
        lbl.pack()
        self.send_priscription_screen.mainloop()
#             print(1 , selfinp)

    def priscription_register(self):
        self.check_counter = 0
        warn = ""
        import re
        self.i = re.sub("[(,'')]", "", self.t)

        #inp = inputtxt.get(1.0, "end-1c")
        #lbl.config(text = "Provided Input: "+inp)
        #b = inp.get()
        if inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET priscription = ? WHERE  pat_username=? ", (inp, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.send_priscription_screen.destroy()
#                     cur.execute("SELECT * FROM pat_signup_info")
#                     result_set = cur.fetchall()
#                     print(result_set)
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def update_send_priscription(self):
        self.check_counter = 0
        warn = ""
        global update_send_priscription_screen
        self.update_send_priscription_screen = Toplevel(self.master)
        self.update_send_priscription_screen.title("Update Priscription")
        self.update_send_priscription_screen.geometry("300x250")
        self.update_send_priscription_screen.attributes('-topmost', True)

        global update_priscription
        global update_priscription_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
    #         print(a)
            self.t = self.a
    #         print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.update_send_priscription_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.update_send_priscription_screen,
                             text="confirm", command=show).pack()

        def printInput():
            global inp
            inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Provided prescription: "+inp)
    #         print (inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.update_send_priscription_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

#             Button Creation
        self.printButton = tk.Button(self.update_send_priscription_screen,
                                     text="confirm Priscription",
                                     command=printInput)

        self.printButton.pack()

        self.printButton2 = tk.Button(self.update_send_priscription_screen,
                                      text="confirm Priscription",
                                      command=self.update_priscription_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.update_send_priscription_screen, text="")
        lbl.pack()
        self.update_send_priscription_screen.mainloop()
#             print(1 , selfinp)

    def update_priscription_register(self):
        self.check_counter = 0
        warn = ""
        import re
        self.i = re.sub("[(,'')]", "", self.t)

        #inp = inputtxt.get(1.0, "end-1c")
        #lbl.config(text = "Provided Input: "+inp)
        #b = inp.get()
        if inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET priscription = ? WHERE  pat_username=? ", (inp, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.update_send_priscription_screen.destroy()
#                     cur.execute("SELECT * FROM pat_signup_info")
#                     result_set = cur.fetchall()
#                     print(result_set)
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def del_send_priscription(self):
        self.check_counter = 0
        warn = ""
        global del_send_priscription_screen
        self.del_send_priscription_screen = Toplevel(self.master)
        self.del_send_priscription_screen.title("Delete Priscription")
        self.del_send_priscription_screen.geometry("300x250")
        self.del_send_priscription_screen.attributes('-topmost', True)

        global del_priscription
        global del_priscription_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
    #         print(a)
            self.t = self.a
    #         print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.del_send_priscription_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.del_send_priscription_screen,
                             text="confirm", command=show).pack()

        self.printButton2 = tk.Button(self.del_send_priscription_screen,
                                      text="Delete Priscription",
                                      command=self.del_priscription_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.del_send_priscription_screen, text="")
        lbl.pack()
        self.del_send_priscription_screen.mainloop()
#             print(1 , selfinp)

    def del_priscription_register(self):

        import re
        self.i = re.sub("[(,'')]", "", self.t)
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute(
            "UPDATE pat_signup_info SET priscription = ? WHERE  pat_username=? ", ("", self.i))
        con.commit()
        con.close()
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        messagebox.showinfo('confirmation', 'Priscription Deleted')
        self.del_send_priscription_screen.destroy()
        con.close()

# Send Diet Plan
    def send_diet_plan(self):
        self.check_counter = 0
        warn = ""
        global send_diet_plan_screen
        self.send_diet_plan_screen = Toplevel(self.master)
        self.send_diet_plan_screen.title("Diet Plan")
        self.send_diet_plan_screen.geometry("300x250")
        self.send_diet_plan_screen.attributes('-topmost', True)

        global diet_plan
        global diet_plan_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
            # print(self.a)
            self.t = self.a
            # print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.send_diet_plan_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.send_diet_plan_screen,
                             text="confirm", command=show).pack()

        def printInput():
            global dp_inp
            dp_inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Provided Diet Plan: "+dp_inp)
#                 #print (dp_inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.send_diet_plan_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

        # Button Creation
        self.printButton = tk.Button(self.send_diet_plan_screen,
                                     text="confirm Diet Plan",
                                     command=printInput)

        self.printButton.pack()
        self.printButton2 = tk.Button(self.send_diet_plan_screen,
                                      text="confirm Diet Plan",
                                      command=self.diet_plan_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.send_diet_plan_screen, text="")
        lbl.pack()
        self.send_diet_plan_screen.mainloop()
    #     print(1 , dp_inp)

    def diet_plan_register(self):
        self.check_counter = 0
        warn = ""
        import re
        self.i = re.sub("[(,'')]", "", self.t)

        #inp = inputtxt.get(1.0, "end-1c")
        #lbl.config(text = "Provided Input: "+inp)
        #b = inp.get()
        if dp_inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                # cur.execute("INSERT INTO pat_signup_info VALUES (:invoice) WHERE pat_id =?", {
                #                   'bill': bill_entry.get(),t
                # })
                #cur.execute("INSERT INTO doc_signup_info VALUES (?,?,NULL)",(doc_username,doc_password))
                #cur.execute("INSERT INTO pat_signup_info VALUES (NULL,NULL,NULL,?) WHERE pat_id = ?",(bill_entry.get(),t))
                #cur.execute("UPDATE pat_signup_info SET invoice = ? WHERE  pat_username=? ",(b,t ) )
                cur.execute(
                    "UPDATE pat_signup_info SET diet_plan = ? WHERE  pat_username=? ", (dp_inp, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.send_diet_plan_screen.destroy()
#                     cur.execute("SELECT * FROM pat_signup_info")
#                     result_set = cur.fetchall()
#                     print(result_set)
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def update_send_diet_plan(self):
        self.check_counter = 0
        warn = ""
        global update_send_diet_plan_screen
        self.update_send_diet_plan_screen = Toplevel(self.master)
        self.update_send_diet_plan_screen.title("Update Diet Plan")
        self.update_send_diet_plan_screen.geometry("300x250")
        self.update_send_diet_plan_screen.attributes('-topmost', True)

        global update_diet_plan
        global update_diet_plan_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
            # print(self.a)
            self.t = self.a
            # print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.update_send_diet_plan_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.update_send_diet_plan_screen,
                             text="confirm", command=show).pack()

        def printInput():
            global dp_inp
            dp_inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Provided Diet Plan: "+dp_inp)
#                 #print (dp_inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.update_send_diet_plan_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

        # Button Creation
        self.printButton = tk.Button(self.update_send_diet_plan_screen,
                                     text="confirm Diet Plan",
                                     command=printInput)

        self.printButton.pack()
        self.printButton2 = tk.Button(self.update_send_diet_plan_screen,
                                      text="confirm Diet Plan",
                                      command=self.update_diet_plan_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.update_send_diet_plan_screen, text="")
        lbl.pack()
        self.update_send_diet_plan_screen.mainloop()
    #     print(1 , dp_inp)

    def update_diet_plan_register(self):
        self.check_counter = 0
        warn = ""
        import re
        self.i = re.sub("[(,'')]", "", self.t)

        #inp = inputtxt.get(1.0, "end-1c")
        #lbl.config(text = "Provided Input: "+inp)
        #b = inp.get()
        if dp_inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET diet_plan = ? WHERE  pat_username=? ", (dp_inp, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.update_send_diet_plan_screen.destroy()
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def del_send_diet_plan(self):
        self.check_counter = 0
        warn = ""
        global del_send_diet_plan_screen
        self.del_send_diet_plan_screen = Toplevel(self.master)
        self.del_send_diet_plan_screen.title("Delete Diet Plan")
        self.del_send_diet_plan_screen.geometry("300x250")
        self.del_send_diet_plan_screen.attributes('-topmost', True)

        global del_diet_plan
        global del_diet_plan_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
            # print(self.a)
            self.t = self.a
            # print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.del_send_diet_plan_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.del_send_diet_plan_screen,
                             text="confirm", command=show).pack()

        self.printButton2 = tk.Button(self.del_send_diet_plan_screen,
                                      text="Delete Diet Plan",
                                      command=self.del_diet_plan_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.del_send_diet_plan_screen, text="")
        lbl.pack()
        self.del_send_diet_plan_screen.mainloop()
    #     print(1 , dp_inp)

    def del_diet_plan_register(self):

        import re
        self.i = re.sub("[(,'')]", "", self.t)

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute(
            "UPDATE pat_signup_info SET diet_plan = ? WHERE  pat_username=? ", ("", self.i))
        con.commit()
        con.close()
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        messagebox.showinfo('confirmation', 'Diet Plan Deleted')
        self.del_send_diet_plan_screen.destroy()
        con.close()

    def update_doc_profile(self):
        global update_doc_profile_screen
        self.update_doc_profile_screen = Toplevel(self.master)
        self.update_doc_profile_screen.title("Update Docters profile")
        self.update_doc_profile_screen.geometry("400x350")
        self.update_doc_profile_screen.attributes('-topmost', True)

        global doc_mob
        global doc_spl

        self.doc_mob = StringVar()
        self.doc_spl = StringVar()

        global doc_mob_entry
        global doc_spl_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT doc_username FROM doc_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        Label(self.update_doc_profile_screen,
              text="Please Update the details", bg="blue").pack()
        Label(self.update_doc_profile_screen, text="").pack()

        lable = Label(self.update_doc_profile_screen, text="Mobile Number * ")
        lable.pack()
        self.doc_mob_entry = Entry(
            self.update_doc_profile_screen, textvariable=self.doc_mob)
        self.doc_mob_entry.pack()
        Label(self.update_doc_profile_screen, text="").pack()

        lable = Label(self.update_doc_profile_screen, text="Specialisation * ")
        lable.pack()
        self.doc_spl_entry = Entry(
            self.update_doc_profile_screen, textvariable=self.doc_spl)
        self.doc_spl_entry.pack()
        Label(self.update_doc_profile_screen, text="").pack()

        Button(self.update_doc_profile_screen, text="Update", width=10,
               height=1, bg="blue", command=self.update_doc_profile_register).pack()

    def update_doc_profile_register(self):
        self.check_counter = 0
        warn = ""
    #     b = bill_entry.get()
        if self.doc_mob.get() == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

        if self.doc_spl.get() == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 2:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                # cur.execute("INSERT INTO pat_signup_info VALUES (:invoice) WHERE pat_id =?", {
                #                   'bill': bill_entry.get(),t
                # })
                #cur.execute("INSERT INTO doc_signup_info VALUES (?,?,NULL)",(doc_username,doc_password))
                #cur.execute("INSERT INTO pat_signup_info VALUES (NULL,NULL,NULL,?) WHERE pat_id = ?",(bill_entry.get(),t))
                #cur.execute("UPDATE pat_signup_info SET invoice = ? WHERE  pat_username=? ",(b,t ) )
                cur.execute("UPDATE doc_signup_info SET doc_mob = ?, doc_spl = ? WHERE  doc_username=? ",
                            (self.doc_mob.get(), self.doc_spl.get(), d_un))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.update_doc_profile_screen.destroy()
#                     cur.execute("SELECT * FROM pat_signup_info")
#                     result_set = cur.fetchall()
#                     print(result_set)
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def doc_disable_button(self):
        self.master.destroy()
        messagebox.showinfo('confirmation', 'Logout Sucessfully')

    def doc_disable_button1(self):
        self.master.destroy()
#             messagebox.showinfo('confirmation', 'Logout Sucessfully')

    def del_doc_account(self):
        db = sqlite3.connect('shms.db')
        cursor = db.cursor()
        cursor.execute(
            "DELETE from doc_signup_info where doc_username=?", (d_un,))
        self.doc_disable_button1()
        cursor.connection.commit()
        db.close()
        messagebox.showinfo("Account Permanently Deleted")

    def pat_mail(self):
        global pat_mail_screen
        self.pat_mail_screen = Toplevel(self.master)
        self.pat_mail_screen.title("Send Mail to Doctor")
        self.pat_mail_screen.geometry("500x500")
        self.pat_mail_screen.attributes('-topmost', True)

        def send_mail_pat():

            self.data = self.inputtxt.get("1.0", "end-1c")
#                 print(self.data)

            self.address_info = self.address.get()

            #email_body_info = email_body.get()

#                 print(self.address_info,self.data)

            sender_email = "mnsrkhnmohammad@gmail.com"

            sender_password = "mansoorkhan123"

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender_email, sender_password)

            print("Login successful")

            server.sendmail(sender_email, self.address_info, self.data)

            print("Message sent")

            self.address_entry.delete(0, END)
            self.inputtxt.delete('1.0', END)
            messagebox.showinfo('confirmation', 'Mail Sent Sucessfully')
            self.pat_mail_screen.destroy()

        address_field = Label(self.pat_mail_screen, text="Recipient Address :")
        email_body_field = Label(self.pat_mail_screen, text="Email Body :")

        address_field.place(x=15, y=70)
        email_body_field.place(x=15, y=140)

        self.address = StringVar()
        self.email_body = StringVar()

        self.address_entry = Entry(
            self.pat_mail_screen, textvariable=self.address, width="30")
        #email_body_entry = Entry(textvariable=email_body,width="30")

    #     l = Label(text = "Priscription ")
        self.inputtxt = Text(self.pat_mail_screen, height=10,
                             width=25)

        self.address_entry.place(x=15, y=100)
        self.inputtxt.place(x=15, y=180)

        self.button = Button(self.pat_mail_screen, text="Send Email",
                             command=send_mail_pat, width="30", height="2", bg="grey")
#             print("yes")

        self.button.place(x=15, y=380)


# Send Diet Plan

    def send_lab_test(self):
        self.check_counter = 0
        warn = ""
        global send_lab_test_screen
        self.send_lab_test_screen = Toplevel(self.master)
        self.send_lab_test_screen.title("Lab Test")
        self.send_lab_test_screen.geometry("300x250")
        self.send_lab_test_screen.attributes('-topmost', True)

        global lab_test
        global lab_test_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
            # print(self.a)
            self.t = self.a
            # print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(self.send_lab_test_screen,
                               self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.send_lab_test_screen,
                             text="confirm", command=show).pack()

        def printInput():
            global lt_inp
            lt_inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Sugest Lab Test: "+lt_inp)
#                 #print (dp_inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.send_lab_test_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

        # Button Creation
        self.printButton = tk.Button(self.send_lab_test_screen,
                                     text="confirm Lab Test",
                                     command=printInput)

        self.printButton.pack()
        self.printButton2 = tk.Button(self.send_lab_test_screen,
                                      text="confirm Lab Test",
                                      command=self.lab_test_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.send_lab_test_screen, text="")
        lbl.pack()
        self.send_lab_test_screen.mainloop()

    def lab_test_register(self):
        self.check_counter = 0
        warn = ""
        import re
        self.i = re.sub("[(,'')]", "", self.t)

        if lt_inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET lab_test = ? WHERE  pat_username=? ", (lt_inp, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Lab Test Saved')
                self.send_lab_test_screen.destroy()
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def update_send_lab_test(self):
        self.check_counter = 0
        warn = ""
        global update_send_lab_test_screen
        self.update_send_lab_test_screen = Toplevel(self.master)
        self.update_send_lab_test_screen.title("Update Lab Test")
        self.update_send_lab_test_screen.geometry("300x250")
        self.update_send_lab_test_screen.attributes('-topmost', True)

        global update_lab_test
        global update_lab_test_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
            # print(self.a)
            self.t = self.a
            # print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.update_send_lab_test_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.update_send_lab_test_screen,
                             text="confirm", command=show).pack()

        def printInput():
            global lt_inp
            lt_inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Sugest Lab Test: "+lt_inp)
#                 #print (dp_inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.update_send_lab_test_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

        # Button Creation
        self.printButton = tk.Button(self.update_send_lab_test_screen,
                                     text="confirm Lab Test",
                                     command=printInput)

        self.printButton.pack()
        self.printButton2 = tk.Button(self.update_send_lab_test_screen,
                                      text="confirm Lab Test",
                                      command=self.update_lab_test_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.update_send_lab_test_screen, text="")
        lbl.pack()
        self.update_send_lab_test_screen.mainloop()
    #     print(1 , dp_inp)

    def update_lab_test_register(self):
        self.check_counter = 0
        warn = ""
        import re
        self.i = re.sub("[(,'')]", "", self.t)

        #inp = inputtxt.get(1.0, "end-1c")
        #lbl.config(text = "Provided Input: "+inp)
        #b = inp.get()
        if lt_inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE pat_signup_info SET lab_test = ? WHERE  pat_username=? ", (lt_inp, self.i))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Lab Test Updated')
                self.update_send_lab_test_screen.destroy()
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def del_send_lab_test(self):
        self.check_counter = 0
        warn = ""
        global del_send_lab_test_screen
        self.del_send_lab_test_screen = Toplevel(self.master)
        self.del_send_lab_test_screen.title("Lab Test")
        self.del_send_lab_test_screen.geometry("300x250")
        self.del_send_lab_test_screen.attributes('-topmost', True)

        global del_lab_test
        global del_lab_test_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def show():
            global t
            self.a = self.clicked.get()
            # print(self.a)
            self.t = self.a
            # print(type(t))
        # Dropdown menu options
        options = self.result_set

        # datatype of menu text
        self.clicked = StringVar()

        # initial menu text
        self.clicked.set("Select patient")

        # Create Dropdown menu
        self.drop = OptionMenu(
            self.del_send_lab_test_screen, self.clicked, *options)
        self.drop.pack()

       # Create button, it will change label text
        self.button = Button(self.del_send_lab_test_screen,
                             text="confirm", command=show).pack()

        lbl = tk.Label(self.del_send_lab_test_screen, text="")
        lbl.pack()

        # Button Creation
        self.printButton2 = tk.Button(self.del_send_lab_test_screen,
                                      text="Delete Lab Test",
                                      command=self.del_lab_test_register)
        self.printButton2.pack()

        # Label Creation

        self.del_send_lab_test_screen.mainloop()

    def del_lab_test_register(self):

        import re
        self.i = re.sub("[(,'')]", "", self.t)
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute(
            "UPDATE pat_signup_info SET lab_test = ? WHERE  pat_username=? ", ("", self.i))
        con.commit()
        con.close()
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        messagebox.showinfo('confirmation', 'Lab Test Deleted')
        self.del_send_lab_test_screen.destroy()
        con.close()

    def view_vitals(self):

        self.r = tk.Tk()
        self.r.title("Vital Data")
        self.r.geometry("600x250")

        self.db = sqlite3.connect('shms.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("select * from add_vital")

        self.tree = ttk.Treeview(self.r)
        self.tree["columns"] = ("pat_username", "add_vital", "date")
        self.tree.column("pat_username", width=0,
                         minwidth=100, anchor=tk.CENTER)
        self.tree.column("add_vital", width=100,
                         minwidth=200, anchor=tk.CENTER)
        self.tree.column("date", width=220, minwidth=190, anchor=tk.CENTER)

        self.tree.heading(
            "pat_username", text="pat_username", anchor=tk.CENTER)
        self.tree.heading("add_vital", text="add_vital", anchor=tk.CENTER)
        self.tree.heading("date", text="date", anchor=tk.CENTER)

        i = 0
        for row in self.cursor:
            self.tree.insert("", i, text="", values=(row[0], row[1], row[2]))
            i = i+1
        self.tree.pack()
        self.r.mainloop()

    def appointment_log(self):

        self.r = tk.Tk()
        self.r.title("Appointment Log")
        self.r.geometry("600x250")

        self.db = sqlite3.connect('shms.db')
        self.cursor = self.db.cursor()
        self.cursor.execute("select * from appointments")

        self.tree = ttk.Treeview(self.r)
        self.tree["columns"] = ("pat_username", "name", "age", "gender",
                                "location", "schedule_time", "phone", "appointment_status")
        self.tree.column("pat_username", width=100,
                         minwidth=100, anchor=tk.CENTER)
        self.tree.column("name", width=100, minwidth=100, anchor=tk.CENTER)
        self.tree.column("age", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("gender", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("location", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("schedule_time", width=100,
                         minwidth=100, anchor=tk.CENTER)
        self.tree.column("phone", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("appointment_status", width=100,
                         minwidth=100, anchor=tk.CENTER)

        self.tree.heading("pat_username", text="Username", anchor=tk.CENTER)
        self.tree.heading("name", text="Name", anchor=tk.CENTER)
        self.tree.heading("age", text="Age", anchor=tk.CENTER)
        self.tree.heading("gender", text="Gender", anchor=tk.CENTER)
        self.tree.heading("location", text="Location", anchor=tk.CENTER)
        self.tree.heading(
            "schedule_time", text="Scheduled Time", anchor=tk.CENTER)
        self.tree.heading("phone", text="Contact Number", anchor=tk.CENTER)
        self.tree.heading("appointment_status",
                          text="Status", anchor=tk.CENTER)

        i = 0
        for row in self.cursor:
            self.tree.insert("", i, text="", values=(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            i = i+1
        self.tree.pack()
        self.r.mainloop()

    def download_appointment_log(self):
        global download_appointment_log_screen
        self.download_appointment_log_screen = Toplevel(self.master)
        self.download_appointment_log_screen.title("Download Priscription")
        self.download_appointment_log_screen.geometry("400x350")
        self.download_appointment_log_screen.attributes('-topmost', True)
        Button(self.download_appointment_log_screen, text="Download Appointmet Log",
               width=20, height=1, bg="blue", command=self.dl_appointment_log).pack()

    def dl_appointment_log(self):
        con = sqlite3.connect('shms.db')
        cur2 = con.cursor()
    #         u = self.login_un
        cur2.execute("select * from appointments")
        result_set = cur2.fetchall()
        con.commit()
        con.close()

    #   print(result_set,234)
        a = str(result_set)
#             print(a)
        with open("Appointment_log.txt", 'w', encoding='utf-8') as f:
            f.write(a)
            f.write("\n\n")
        messagebox.showinfo("Downloaded Sucessfully")
        self.master.destroy()
        self.main_screen3 = Tk()
        self.b = Doctor(self.main_screen3)


# %%
class Patient:
    def __init__(self, master):
        self.master = master
        self.master.title("Patient's Screen")
        self.master.geometry("500x550+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")

        self.b1 = Button(self.master, text="Update Profile",
                         width=20, height=1, command=self.update_pat_profile)
        self.b1.place(x=10, y=50)
        self.b2 = Button(self.master, text="Send Email",
                         width=20, height=1, command=self.doc_mail)
        self.b2.place(x=10, y=90)
        self.b5 = Button(self.master, text="Appointment",
                         width=20, height=1, command=self.call)
        self.b5.place(x=10, y=130)
        self.b6 = Button(self.master, text="Vitals",
                         width=20, command=self.call2)
        self.b6.place(x=10, y=170)
        self.b8 = Button(self.master, text="Calculate BMI",
                         width=20, height=1, command=self.bmi)
        self.b8.place(x=10, y=210)


#             self.b3 = Button(self.master, text="Request Medicine", width=20, height=1)
#             self.b3.place(x=10, y=130)
#             self.b4 = Button(self.master, text="Set Reminder", width=20, height=1)
#             self.b4.place(x=10, y=170)
#             self.b7 = Button(self.master, text="Maps and Location", width=20, height=1)
#             self.b7.place(x=10, y=290)
#             self.b9 = Button(self.master, text="Apply Coupon", width=20, height=1)
#             self.b9.place(x=10, y=370)

        self.b10 = Button(self.master, text="Emergency Contact",
                          width=20, height=1, command=self.emergency_contact)
        self.b10.place(x=10, y=250)

        self.b11 = Button(self.master, text="Delet Account", width=20,
                          height=1, fg="black", bg="red", command=self.del_pat_account)
        self.b11.place(x=10, y=450)

        self.b12 = Button(self.master, text="Log Out", width=20, height=1,
                          fg="white", bg="black", command=self.pat_disable_button)
        self.b12.place(x=10, y=490)

    def call(self):

        global main_screen2
        self.main_screen2 = Tk()
        self.main_screen2.geometry("600x450")
        self.main_screen2.title("Account Login")

        #self.newWindow = Toplevel(self.master)
        self.b = Appointments(self.main_screen2)
        self.master.destroy()

    def call2(self):

        global main_screen3
        self.main_screen3 = Tk()
        self.main_screen3.geometry("600x450")
        self.main_screen3.title("Feedback")

        self.b = Vital(self.main_screen3)
        self.master.destroy()

    def doc_mail(self):
        global doc_mail_screen
        self.doc_mail_screen = Toplevel(self.master)
        self.doc_mail_screen.title("Send Mail to Doctor")
        self.doc_mail_screen.geometry("500x500")
        self.doc_mail_screen.attributes('-topmost', True)

        def send_mail_doc():

            self.data = self.inputtxt.get("1.0", "end-1c")
#                 print(self.data)

            self.address_info = self.address.get()

            #email_body_info = email_body.get()

#                 print(self.address_info,self.data)

            sender_email = "mnsrkhnmohammad@gmail.com"

            sender_password = "mansoorkhan123"

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender_email, sender_password)

            print("Login successful")

            server.sendmail(sender_email, self.address_info, self.data)

            print("Message sent")

            self.address_entry.delete(0, END)
            self.inputtxt.delete('1.0', END)

        address_field = Label(self.doc_mail_screen, text="Recipient Address :")
        email_body_field = Label(self.doc_mail_screen, text="Email Body :")

        address_field.place(x=15, y=70)
        email_body_field.place(x=15, y=140)

        self.address = StringVar()
        self.email_body = StringVar()

        self.address_entry = Entry(
            self.doc_mail_screen, textvariable=self.address, width="30")
        #email_body_entry = Entry(textvariable=email_body,width="30")

    #     l = Label(text = "Priscription ")
        self.inputtxt = Text(self.doc_mail_screen, height=10,
                             width=25)

        self.address_entry.place(x=15, y=100)
        self.inputtxt.place(x=15, y=180)

        self.button = Button(self.doc_mail_screen, text="Send Email",
                             command=send_mail_doc, width="30", height="2", bg="grey")
#             print("yes")

        self.button.place(x=15, y=380)

    def update_pat_profile(self):
        global update_pat_profile_screen
        self.update_pat_profile_screen = Toplevel(self.master)
        self.update_pat_profile_screen.title("Update patients profile")
        self.update_pat_profile_screen.geometry("400x350")
        self.update_pat_profile_screen.attributes('-topmost', True)

        global pat_mob
        global pat_gender

        self.pat_mob = StringVar()
        self.pat_gender = StringVar()

        global pat_mob_entry
        global pat_gender_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        result_set = cur.fetchall()
        con.close()

        Label(self.update_pat_profile_screen,
              text="Please Update the details", bg="blue").pack()
        Label(self.update_pat_profile_screen, text="").pack()

        lable = Label(self.update_pat_profile_screen, text="Mobile Number * ")
        lable.pack()
        self.pat_mob_entry = Entry(
            self.update_pat_profile_screen, textvariable=self.pat_mob)
        self.pat_mob_entry.pack()
        Label(self.update_pat_profile_screen, text="").pack()

        lable = Label(self.update_pat_profile_screen, text="Gender * ")
        lable.pack()
        self.pat_gender_entry = Entry(
            self.update_pat_profile_screen, textvariable=self.pat_gender)
        self.pat_gender_entry.pack()
        Label(self.update_pat_profile_screen, text="").pack()

        Button(self.update_pat_profile_screen, text="Update", width=10,
               height=1, bg="blue", command=self.update_pat_profile_register).pack()

    def update_pat_profile_register(self):
        check_counter = 0
        warn = ""
    #     b = bill_entry.get()
        if self.pat_mob.get() == "":
            warn = "Can't be empty"
        else:
            check_counter += 1

        if self.pat_gender.get() == "":
            warn = "Can't be empty"
        else:
            check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if check_counter == 2:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("UPDATE pat_signup_info SET pat_mob = ?, pat_gender = ? WHERE  pat_username=? ",
                            (self.pat_mob.get(), self.pat_gender.get(), p_un))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.update_pat_profile_screen.withdraw()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def medicine_progress(self):
        global medicine_progress_screen
        self.medicine_progress_screen = Toplevel(self.master)
        self.medicine_progress_screen.title("Register")
        self.medicine_progress_screen.geometry("300x250")

        global medicine_name
        global no_of_days
        global dosage

        global medicine_name_entry
        global no_of_days_entry
        global dosage_entry

        self.medicine_name = StringVar()
        self.no_of_days = StringVar()
        self.dosage = StringVar()

        Label(self.medicine_progress_screen,
              text="Please fill the details below", bg="blue").pack()
        Label(self.medicine_progress_screen, text="").pack()
        lable = Label(self.medicine_progress_screen,
                      text="Name of Medicine * ")
        lable.pack()
        self.medicine_name_entry = Entry(
            self.medicine_progress_screen, textvariable=self.medicine_name)
        self.medicine_name_entry.pack()
        lable = Label(self.medicine_progress_screen,
                      text="Medicine usage form no of days.? * ")
        lable.pack()
        self.no_of_days_entry = Entry(
            self.medicine_progress_screen, textvariable=self.no_of_days)
        self.no_of_days_entry.pack()
        lable = Label(self.medicine_progress_screen,
                      text="No of Medicine taken each day * ")
        lable.pack()
        self.dosage_entry = Entry(
            self.medicine_progress_screen, textvariable=self.dosage)
        self.dosage_entry.pack()
        Label(self.medicine_progress_screen, text="").pack()
        Button(self.medicine_progress_screen, text="Save", width=10, height=1,
               bg="blue", command=self.medicine_progress_register).pack()
        self.medicine_progress_screen.attributes("-topmost", True)

    # Implementing event on register button
    def medicine_progress_register(self):
        check_counter = 0
        warn = ""
        if self.medicine_name_entry.get() == "":
            warn = " can't be empty"
        else:
            check_counter += 1

        if self.no_of_days.get() == "":
            warn = " can't be empty"
        else:
            check_counter += 1

        if self.dosage.get() == "":
            warn = " can't be empty"
        else:
            check_counter += 1

        if check_counter == 3:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("INSERT INTO medicine_progress VALUES (:pat_username,:medicine_name, :no_of_days, :dosage, :time, NULL)", {
                    'pat_username': p_un,
                    'medicine_name': self.medicine_name.get(),
                    'no_of_days': self.no_of_days.get(),
                    'dosage': self.dosage.get(),
                    'time': datetime.datetime.now()


                })
                con.commit()
                con.close()
                messagebox.showinfo('confirmation', 'Record Saved')

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def bmi(self):
        global bmi_screen, w, h
        self.bmi_screen = Toplevel(self.master)
        self.bmi_screen.title("BMI Calculatio")
        self.bmi_screen.geometry("400x300")
        self.bmi_screen.attributes('-topmost', True)

        def reset_entry():
            self.age_tf.delete(0, 'end')
            self.height_tf.delete(0, 'end')
            self.weight_tf.delete(0, 'end')

        def calculate_bmi():
            self.kg = float(self.weight_tf.get())
            self.m = float(self.height_tf.get())/100
            self.bmi = self.kg/(self.m*self.m)
            self.bmi = round(self.bmi, 1)
            bmi_index(self.bmi)

        def exit_bmi():
            self.bmi_screen.destroy()

        def bmi_index(bmi):

            if self.bmi < 18.5:
                messagebox.showinfo('bmi-pythonguides',
                                    f'BMI = {self.bmi} is Underweight')
                self.bmi_screen.destroy()
            elif (self.bmi > 18.5) and (self.bmi < 24.9):
                messagebox.showinfo('bmi-pythonguides',
                                    f'BMI = {self.bmi} is Normal')
                self.bmi_screen.destroy()
            elif (self.bmi > 24.9) and (self.bmi < 29.9):
                messagebox.showinfo('bmi-pythonguides',
                                    f'BMI = {self.bmi} is Overweight')
                self.bmi_screen.destroy()
            elif (self.bmi > 29.9):
                messagebox.showinfo('bmi-pythonguides',
                                    f'BMI = {self.bmi} is Obesity')
                self.bmi_screen.destroy()
            else:
                messagebox.showerror('bmi-pythonguides',
                                     'something went wrong!')
                self.bmi_screen.destroy()

        self.var = IntVar()

        self.frame = Frame(
            self.bmi_screen,
            padx=10,
            pady=10
        )
        self.frame.pack(expand=True)

        age_lb = Label(
            self.frame,
            text="Enter Age (2 - 120)"
        )
        age_lb.grid(row=1, column=1)

        self.age_tf = Entry(
            self.frame,
        )
        self.age_tf.grid(row=1, column=2, pady=5)

        gen_lb = Label(
            self.frame,
            text='Select Gender'
        )
        gen_lb.grid(row=2, column=1)

        self.frame2 = Frame(
            self.frame
        )
        self.frame2.grid(row=2, column=2, pady=5)

        self.male_rb = Radiobutton(
            self.frame2,
            text='Male',
            variable=self.var,
            value=1
        )
        self.male_rb.pack(side=LEFT)

        self.female_rb = Radiobutton(
            self.frame2,
            text='Female',
            variable=self.var,
            value=2
        )
        self.female_rb.pack(side=RIGHT)

        height_lb = Label(
            self.frame,
            text="Enter Height (cm)  "
        )
        height_lb.grid(row=3, column=1)

        weight_lb = Label(
            self.frame,
            text="Enter Weight (kg)  ",

        )
        weight_lb.grid(row=4, column=1)

        self.height_tf = Entry(
            self.frame,
        )
        self.height_tf.grid(row=3, column=2, pady=5)

        self.weight_tf = Entry(
            self.frame,
        )

        self.weight_tf.grid(row=4, column=2, pady=5)

        self.frame3 = Frame(
            self.frame
        )
        self.frame3.grid(row=5, columnspan=3, pady=10)

        self.cal_btn = Button(
            self.frame3,
            text='Calculate',
            command=calculate_bmi
        )
        self.cal_btn.pack(side=LEFT)

        self.reset_btn = Button(
            self.frame3,
            text='Reset',
            command=reset_entry
        )
        self.reset_btn.pack(side=LEFT)

        self.exit_btn = Button(
            self.frame3,
            text='Exit',
            command=exit_bmi
        )
        self.exit_btn.pack(side=RIGHT)

        self.bmi_screen.mainloop()

    def emergency_contact(self):
        global emergency_contact_screen
        self.emergency_contact_screen = Toplevel(self.master)
        self.emergency_contact_screen.title("Emergency Contact Details")
        self.emergency_contact_screen.geometry("450x300")

        Label(self.emergency_contact_screen,
              text="Emergency Contact Details").pack()
        Label(self.emergency_contact_screen, text="").pack()
        Label(self.emergency_contact_screen, text="Welcome to SHMS").pack()
        Label(self.emergency_contact_screen,
              text="Contact No: +91 12345 12345").pack()
        Label(self.emergency_contact_screen,
              text="Alternate Contact No: +91 12345 54321").pack()
        Label(self.emergency_contact_screen, text="").pack()
        Button(self.emergency_contact_screen, text="exit", width=10,
               height=1, command=self.pat_ec_disable_button).pack()
        self.emergency_contact_screen.attributes("-topmost", True)

    def pat_ec_disable_button(self):
        self.emergency_contact_screen.destroy()

    def del_pat_account(self):
        db = sqlite3.connect('shms.db')
        cursor = db.cursor()
        cursor.execute(
            "DELETE from pat_signup_info where pat_username=?", (p_un,))
        self.pat_final_login_screen.destroy()
        cursor.connection.commit()
        db.close()
        messagebox.showinfo("Account Permanently Delete")

    def pat_disable_button(self):
        self.master.destroy()
        messagebox.showinfo('confirmation', 'Logout Successfully')


# %%
class Appointments:
    def __init__(self, master):
        self.master = master
        self.master.title("Docter's Screen")
        self.master.geometry("600x500+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")

        self.b1 = Button(self.master, text="Book Appointment",
                         width=20, height=1, command=self.book_appointment)
        self.b1.place(x=10, y=50)
        self.b2 = Button(self.master, text="Cancel Appointment",
                         width=20, height=1, command=self.cancel_appointment)
        self.b2.place(x=10, y=90)
        self.b3 = Button(self.master, text="Reschedule Appointment",
                         width=20, height=1, command=self.update_appointmnt)
        self.b3.place(x=10, y=130)

        self.b3 = Button(self.master, text="Check Appointment Status",
                         width=20, height=1, command=self.appointment_status)
        self.b3.place(x=10, y=170)

        self.b4 = Button(self.master, text="Close", width=20, height=1,
                         command=self.appointment_disable_button, fg="white", bg="black")
        self.b4.place(x=10, y=210)

        self.b5 = Button(self.master, text="Back", width=20, height=1,
                         command=self.back_button, fg="white", bg="black")
        self.b5.place(x=10, y=250)

    def book_appointment(self):

        # creating the frames in the master
        self.left = Frame(self.master, width=800, height=720, bg='cadet blue')
        self.left.pack(side=LEFT)

        self.right = Frame(self.master, width=400, height=720, bg='steelblue')
        self.right.pack(side=RIGHT)

        # labels for the window
        self.heading = Label(self.left, text="SHMS Appointments",
                             font=('arial 40 bold'), fg='black')
        self.heading.place(x=0, y=0)
        # patients name
        self.name = Label(self.left, text="Patient's Name",
                          font=('arial 18 bold'), fg='black')
        self.name.place(x=0, y=100)

        # age
        self.age = Label(self.left, text="Age",
                         font=('arial 18 bold'), fg='black')
        self.age.place(x=0, y=140)

        # gender
        self.gender = Label(self.left, text="Gender",
                            font=('arial 18 bold'), fg='black')
        self.gender.place(x=0, y=180)

        # location
        self.location = Label(self.left, text="Location",
                              font=('arial 18 bold'), fg='black')
        self.location.place(x=0, y=220)

        # appointment time
        self.time = Label(self.left, text="Appointment Time",
                          font=('arial 18 bold'), fg='black')
        self.time.place(x=0, y=260)

        # phone
        self.phone = Label(self.left, text="Phone Number",
                           font=('arial 18 bold'), fg='black')
        self.phone.place(x=0, y=300)

        # Entries for all labels============================================================
        self.name_ent = Entry(self.left, width=30)
        self.name_ent.place(x=250, y=100)

        self.age_ent = Entry(self.left, width=30)
        self.age_ent.place(x=250, y=140)

        self.gender_ent = Entry(self.left, width=30)
        self.gender_ent.place(x=250, y=180)

        self.location_ent = Entry(self.left, width=30)
        self.location_ent.place(x=250, y=220)

        self.time_ent = Entry(self.left, width=30)
        self.time_ent.place(x=250, y=260)

        self.phone_ent = Entry(self.left, width=30)
        self.phone_ent.place(x=250, y=300)

        # button to perform a command
        self.submit = Button(self.left, text="Book Appointment",
                             width=20, height=2, command=self.add_appointment)
        self.submit.place(x=300, y=340)

    # funtion to call when the submit button is clicked
    def add_appointment(self):
        # getting the user inputs
        self.val1 = self.name_ent.get()
        self.val2 = self.age_ent.get()
        self.val3 = self.gender_ent.get()
        self.val4 = self.location_ent.get()
        self.val5 = self.time_ent.get()
        self.val6 = self.phone_ent.get()

        # checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
            tkinter.messagebox.showinfo("Warning", "Please Fill Up All Boxes")
        else:
            # now we add to the database
            self.add_appointment_to_db(p_un)

            messagebox.showinfo("Success", "Appointment for " +
                                str(self.val1) + " has been created" + ' at ' + str(self.val5))
            self.master.destroy()
            self.main_screen3 = Tk()
#                 self.main_screen3.geometry("600x450")
#                 self.main_screen3.title("Feedback")
            self.b = Patient(self.main_screen3)

    def add_appointment_to_db(self, pat_login_un):
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
#                 print(12)
        sql = "INSERT INTO 'appointments' (pat_username,name, age, gender, location, scheduled_time, phone) VALUES(?,?, ?, ?, ?, ?, ?)"
        cur.execute(sql, (pat_login_un, self.val1, self.val2,
                          self.val3, self.val4, self.val5, self.val6))
        con.commit()
        con.close()

    def cancel_appointment(self):
        global cancel_appointment_screen
        self.cancel_appointment_screen = Toplevel(self.master)
#             self.cancel_appointment_screen("Register")
        self.cancel_appointment_screen.geometry("300x250")
        self.b1 = Button(self.cancel_appointment_screen, text="Confirm Cancel Appointment",
                         width=30, height=1, command=self.can_app).pack()

    def can_app(self):
        self.cancel_appointent_from_db(p_un)
        messagebox.showinfo("Appointment Cancelled")

    def cancel_appointent_from_db(self, pat_un):
        db = sqlite3.connect('shms.db')
        cursor = db.cursor()
        cursor.execute(
            "DELETE from appointments where pat_username=?", (pat_un,))
        cursor.connection.commit()
        db.close()

    def update_appointmnt(self):
        global reschedule_appointment_screen
        self.reschedule_appointment_screen = Toplevel(self.master)
        self.reschedule_appointment_screen.geometry("400x350")
        self.reschedule_appointment_screen.attributes('-topmost', True)

        global time
        self.time = StringVar()
        global time_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM appointments")
        self.result_set = cur.fetchall()
        con.close()

        Label(self.reschedule_appointment_screen,
              text="Please Update the details", bg="blue").pack()
        Label(self.reschedule_appointment_screen, text="").pack()
        lable = Label(self.reschedule_appointment_screen, text="Time * ")
        lable.pack()
        self.time_entry = Entry(
            self.reschedule_appointment_screen, textvariable=self.time)
        self.time_entry.pack()
        Label(self.reschedule_appointment_screen, text="").pack()

        Button(self.reschedule_appointment_screen, text="Update appointment time",
               width=20, height=1, command=self.update_appointmnt_register).pack()

    def update_appointmnt_register(self):
        self.check_counter = 0
        warn = ""
        self.a = self.time_entry.get()
#             print(self.a)
        if self.time_entry.get() == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

        if self.check_counter == 1:
            try:
                self.update_appointment_db(self.time.get(), p_un)
                messagebox.showinfo('confirmation', 'Record Saved')
                self.master.destroy()
                self.main_screen3 = Tk()
#                     self.main_screen3.geometry("600x450")
#                     self.main_screen3.title("Feedback")
                self.b = Patient(self.main_screen3)
#                     cur.execute("SELECT * FROM pat_signup_info")
#                     result_set = cur.fetchall()
#                     print(result_set)

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def update_appointment_db(self, time, pat_un):
        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute(
            "UPDATE appointments SET scheduled_time = ? WHERE  pat_username=? ", (time, pat_un))
        con.commit()
        con.close()

    def appointment_disable_button(self):
        self.master.destroy()

    def back_button(self):
        self.master.destroy()
        global main_screen3
        self.main_screen3 = Tk()
        self.main_screen3.geometry("600x450")
        self.main_screen3.title("Feedback")
        self.b = Patient(self.main_screen3)

    def appointment_status(self):

        self.r = tk.Tk()
        self.r.title("Customer Data")
        self.r.geometry("700x350")

        self.db = sqlite3.connect('shms.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(
            "SELECT * FROM appointments where pat_username=?", (p_un,))

        self.tree = ttk.Treeview(self.r)
        self.tree["columns"] = ("pat_username", "name", "age", "gender",
                                "location", "schedule_time", "phone", "appointment_status")
        self.tree.column("pat_username", width=100,
                         minwidth=100, anchor=tk.CENTER)
        self.tree.column("name", width=100, minwidth=100, anchor=tk.CENTER)
        self.tree.column("age", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("gender", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("location", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("schedule_time", width=100,
                         minwidth=100, anchor=tk.CENTER)
        self.tree.column("phone", width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column("appointment_status", width=100,
                         minwidth=100, anchor=tk.CENTER)

        self.tree.heading("pat_username", text="Username", anchor=tk.CENTER)
        self.tree.heading("name", text="Name", anchor=tk.CENTER)
        self.tree.heading("age", text="Age", anchor=tk.CENTER)
        self.tree.heading("gender", text="Gender", anchor=tk.CENTER)
        self.tree.heading("location", text="Location", anchor=tk.CENTER)
        self.tree.heading(
            "schedule_time", text="Scheduled Time", anchor=tk.CENTER)
        self.tree.heading("phone", text="Contact Number", anchor=tk.CENTER)
        self.tree.heading("appointment_status",
                          text="Status", anchor=tk.CENTER)

        i = 0
        for row in self.cursor:
            self.tree.insert("", i, text="", values=(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
            i = i+1
        self.tree.pack()
        self.r.mainloop()


# %%
class Vital:
    def __init__(self, master):
        self.master = master
        self.master.title("Vital Screen")
        self.master.geometry("600x500+0+0")
        self.master.config(bg="cadet blue")
        self.frame = Frame(self.master, bg="cadet blue")

        self.b1 = Button(self.master, text="Add Vitals",
                         width=20, height=1, command=self.add_vital)
        self.b1.place(x=10, y=50)

        self.b2 = Button(self.master, text="Update Vitals",
                         width=20, height=1, command=self.update_vital)
        self.b2.place(x=10, y=90)

        self.b3 = Button(self.master, text="Daily Data",
                         width=20, height=1, command=self.daily_report)
        self.b3.place(x=10, y=130)

        self.b4 = Button(self.master, text="delete Data",
                         width=20, height=1, command=self.del_pat_daily_report)
        self.b4.place(x=10, y=170)

        self.b5 = Button(self.master, text="Previous Data",
                         width=20, height=1, command=self.previous_data)
        self.b5.place(x=10, y=210)

        self.b6 = Button(self.master, text="Download Priscription",
                         width=20, height=1, command=self.download_priscription)
        self.b6.place(x=200, y=50)

        self.b7 = Button(self.master, text="Download Diet Plan",
                         width=20, height=1, command=self.download_diet_plan)
        self.b7.place(x=200, y=90)

        self.b8 = Button(self.master, text="Download Invoice",
                         width=20, height=1, command=self.download_invoice)
        self.b8.place(x=200, y=130)

        self.b9 = Button(self.master, text="Feedback to Doctor",
                         width=20, height=1, command=self.feedback)
        self.b9.place(x=200, y=210)

        self.b10 = Button(self.master, text="Close", width=20, height=1,
                          command=self.vital_disable_button, fg="white", bg="black")
        self.b10.place(x=120, y=250)

        self.b11 = Button(self.master, text="Back", width=20, height=1,
                          command=self.back_button, fg="white", bg="black")
        self.b11.place(x=120, y=290)


# Adding Vital Information

    def add_vital(self):
        self.check_counter = 0
        warn = ""
        global add_vital_screen
        self.add_vital_screen = Toplevel(self.master)
        self.add_vital_screen.title("Add Vital Informatiom")
        self.add_vital_screen.geometry("300x250")
        self.add_vital_screen.attributes('-topmost', True)

        global add_vital
        global add_vital_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def printInput(self):
            global av_inp
            self.av_inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Add Vital Information: "+av_inp)
#               print (av_inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.add_vital_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

        self.printButton2 = tk.Button(self.add_vital_screen,
                                      text="confirm ",
                                      command=self.add_vital_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.add_vital_screen, text="")
        lbl.pack()
        self.add_vital_screen.mainloop()
    #     print(1 , av_inp)

    def add_vital_register(self):
        self.av_inp = self.inputtxt.get(1.0, "end-1c")
        self.check_counter = 0
        warn = ""
        import re
#             self.i=re.sub("[(,'')]","",t)

        #inp = inputtxt.get(1.0, "end-1c")
        #lbl.config(text = "Provided Input: "+inp)
        #b = inp.get()
        if self.av_inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("INSERT INTO add_vital VALUES (:pat_username,:add_vital,:time)", {
                    'pat_username': p_un,
                    'add_vital': self.av_inp,
                    'time': datetime.datetime.now()
                })

                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.master.destroy()
                self.main_screen3 = Tk()
                self.b = Vital(self.main_screen3)

                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def daily_report(self):
        global daily_report_screen
        self.daily_report_screen = Toplevel(self.master)
        self.daily_report_screen.title("Register")
        self.daily_report_screen.geometry("300x250")

        global bp
        global sugar
        global temp

        global bp_entry
        global sugar_entry
        global temp_entry

        self.bp = StringVar()
        self.sugar = StringVar()
        self.temp = StringVar()

        Label(self.daily_report_screen,
              text="Please fill the details below", bg="blue").pack()
        Label(self.daily_report_screen, text="").pack()
        lable = Label(self.daily_report_screen, text="BP * ")
        lable.pack()
        self.bp_entry = Entry(self.daily_report_screen, textvariable=self.bp)
        self.bp_entry.pack()
        lable = Label(self.daily_report_screen, text="Sugar * ")
        lable.pack()
        self.sugar_entry = Entry(
            self.daily_report_screen, textvariable=self.sugar)
        self.sugar_entry.pack()
        lable = Label(self.daily_report_screen, text="Temprature * ")
        lable.pack()
        self.temp_entry = Entry(
            self.daily_report_screen, textvariable=self.temp)
        self.temp_entry.pack()
        Label(self.daily_report_screen, text="").pack()
        Button(self.daily_report_screen, text="Register", width=10,
               height=1, bg="blue", command=self.daily_report_register).pack()
        self.daily_report_screen.attributes("-topmost", True)

    # Implementing event on register button
    def daily_report_register(self):
        self.check_counter = 0
        warn = ""
        if self.bp_entry.get() == "":
            warn = " can't be empty"
        else:
            self.check_counter += 1

        if self.sugar_entry.get() == "":
            warn = " can't be empty"
        else:
            self.check_counter += 1

        if self.temp_entry.get() == "":
            warn = " can't be empty"
        else:
            self.check_counter += 1

        if self.check_counter == 3:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("INSERT INTO daily_report VALUES (:pat_username,:bp, :sugar, :temp, :time, NULL)", {
                    'pat_username': p_un,
                    'bp': self.bp_entry.get(),
                    'sugar': self.sugar_entry.get(),
                    'temp': self.temp_entry.get(),
                    'time': datetime.datetime.now()


                })
                con.commit()
                con.close()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.master.destroy()
                self.main_screen3 = Tk()
                self.b = Vital(self.main_screen3)

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def del_pat_daily_report(self):
        db = sqlite3.connect('shms.db')
        cursor = db.cursor()
        cursor.execute(
            "DELETE from daily_report where pat_username=?", (p_un,))
        cursor.connection.commit()
        db.close()
        messagebox.showinfo("Data Permanently Delete")
        self.master.destroy()
        self.main_screen3 = Tk()
        self.b = Vital(self.main_screen3)

    def update_vital(self):
        global update_vital_screen
        self.update_vital_screen = Toplevel(self.master)
        self.update_vital_screen.title("Update Vital Data")
        self.update_vital_screen.geometry("400x350")
        self.update_vital_screen.attributes('-topmost', True)

        global add_vital
        global add_vital_entry

        con = sqlite3.connect('shms.db')
        cur = con.cursor()
        cur.execute("SELECT pat_username FROM pat_signup_info")
        self.result_set = cur.fetchall()
        con.close()

        def printInput(self):
            global av_inp
            self.av_inp = self.inputtxt.get(1.0, "end-1c")
            lbl.config(text="Update Vital Information: "+av_inp)
#               print (av_inp)

        # TextBox Creation
        self.inputtxt = tk.Text(self.update_vital_screen,
                                height=5,
                                width=20)

        self.inputtxt.pack()

        self.printButton2 = tk.Button(self.update_vital_screen,
                                      text="confirm ",
                                      command=self.update_vital_register)

        self.printButton2.pack()

        # Label Creation
        lbl = tk.Label(self.update_vital_screen, text="")
        lbl.pack()
        self.update_vital_screen.mainloop()
    #     print(1 , av_inp)

    def update_vital_register(self):
        self.av_inp = self.inputtxt.get(1.0, "end-1c")
        self.check_counter = 0
        warn = ""
#             import re
#             self.i=re.sub("[(,'')]","",t)

        if self.av_inp == "":
            warn = "Can't be empty"
        else:
            self.check_counter += 1

    #     import re
    #     i=re.sub("[(,'')]","",t)

        if self.check_counter == 1:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute(
                    "UPDATE add_vital SET add_vital = ?WHERE  pat_username=? ", (self.av_inp, p_un))
                con.commit()
                con.close()
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                messagebox.showinfo('confirmation', 'Record Saved')
                self.master.destroy()
                self.main_screen3 = Tk()
                self.b = Vital(self.main_screen3)
#                     cur.execute("SELECT * FROM pat_signup_info")
#                     result_set = cur.fetchall()
#                     print(result_set)
                con.close()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def download_priscription(self):
        global download_priscription_screen
        self.download_priscription_screen = Toplevel(self.master)
        self.download_priscription_screen.title("Download Priscription")
        self.download_priscription_screen.geometry("400x350")
        self.download_priscription_screen.attributes('-topmost', True)
        Button(self.download_priscription_screen, text="Download",
               width=10, height=1, bg="blue", command=self.dl_pris).pack()

    def dl_pris(self):
        con = sqlite3.connect('shms.db')
        cur2 = con.cursor()
    #         u = self.login_un
        cur2.execute(
            "SELECT priscription FROM pat_signup_info where pat_username = ?", (p_un,))

        #cursor.execute("SELECT * FROM pat_signup_info where pat_username = ?",('was',))
        result_set = cur2.fetchall()
        con.commit()
        con.close()

    #   print(result_set,234)
        a = str(result_set)
#             print(a)
        with open("Priscription.txt", 'w', encoding='utf-8') as f:
            f.write(a)
            f.write("\n\n")
        messagebox.showinfo("Downloaded")
        self.master.destroy()
        self.main_screen3 = Tk()
        self.b = Vital(self.main_screen3)
#             self.download_priscription_screen.destroy()

    def download_diet_plan(self):
        global download_diet_plan_screen
        self.download_diet_plan_screen = Toplevel(self.master)
        self.download_diet_plan_screen.title("Download Priscription")
        self.download_diet_plan_screen.geometry("400x350")
        self.download_diet_plan_screen.attributes('-topmost', True)
        Button(self.download_diet_plan_screen, text="Confirm Download",
               width=10, height=1, command=self.dl_dp).pack()

    def dl_dp(self):
        con = sqlite3.connect('shms.db')
        cur2 = con.cursor()
    #         u = self.login_un
        cur2.execute(
            "SELECT diet_plan FROM pat_signup_info where pat_username = ?", (p_un,))

        #cursor.execute("SELECT * FROM pat_signup_info where pat_username = ?",('was',))
        result_set = cur2.fetchall()
        con.commit()
        con.close()

    #   print(result_set,234)
        a = str(result_set)
#             print(a)
        with open("Diet_plan.txt", 'w', encoding='utf-8') as f:
            f.write(a)
            f.write("\n\n")
        messagebox.showinfo("Downloaded")
        self.download_diet_plan_screen.destroy()

    def download_invoice(self):
        global download_invoice_screen
        self.download_invoice_screen = Toplevel(self.master)
        self.download_invoice_screen.title("Download Priscription")
        self.download_invoice_screen.geometry("400x350")
        self.download_invoice_screen.attributes('-topmost', True)
        Button(self.download_invoice_screen, text="Confirm Download",
               width=20, height=1, command=self.dl_invoice).pack()

    def dl_invoice(self):
        con = sqlite3.connect('shms.db')
        cur2 = con.cursor()
    #         u = self.login_un
        cur2.execute(
            "SELECT invoice FROM pat_signup_info where pat_username = ?", (p_un,))

        #cursor.execute("SELECT * FROM pat_signup_info where pat_username = ?",('was',))
        result_set = cur2.fetchall()
        con.commit()
        con.close()

    #   print(result_set,234)
        a = str(result_set)
#             print(a)
        with open("Invoice.txt", 'w', encoding='utf-8') as f:
            f.write(a)
            f.write("\n\n")
        messagebox.showinfo("Downloaded")
        self.master.destroy()
        self.main_screen3 = Tk()
        self.b = Vital(self.main_screen3)
#             self.download_invoice_screen.destroy()

    def feedback(self):
        global feedback_screen
        self.feedback_screen = Toplevel(self.master)
        self.feedback_screen.title("Feedback to doctor")
        self.feedback_screen.geometry("500x350")

        global med_working
        global improvement
        global side_effects

        global med_working_entry
        global improvement_entry
        global side_effects_entry

        self.med_working = StringVar()
        self.improvement = StringVar()
        self.side_effects = StringVar()

        Label(self.feedback_screen,
              text="Please fill below feedback form", bg="blue").pack()
        Label(self.feedback_screen, text="").pack()
        lable = Label(self.feedback_screen,
                      text="Are the medicine working will.? * ")
        lable.pack()
        self.med_working_entry = Entry(
            self.feedback_screen, textvariable=self.med_working)
        self.med_working_entry.pack()
        lable = Label(self.feedback_screen,
                      text="Any improvement in health condition.? * ")
        lable.pack()
        self.improvement_entry = Entry(
            self.feedback_screen, textvariable=self.improvement)
        self.improvement_entry.pack()
        lable = Label(self.feedback_screen,
                      text="Did you absorve any side effects.? * ")
        lable.pack()
        lable = Label(self.feedback_screen, text="If yes please specify * ")
        lable.pack()
        self.side_effects_entry = Entry(
            self.feedback_screen, textvariable=self.side_effects)
        self.side_effects_entry.pack()
        Label(self.feedback_screen, text="").pack()
        Button(self.feedback_screen, text="Send to doctor", width=10,
               height=1, bg="blue", command=self.feedback_register).pack()
        self.feedback_screen.attributes("-topmost", True)

    # Implementing event on register button
    def feedback_register(self):
        check_counter = 0
        warn = ""
        if self.med_working_entry.get() == "":
            warn = " can't be empty"
        else:
            check_counter += 1

        if self.improvement_entry.get() == "":
            warn = " can't be empty"
        else:
            check_counter += 1

        if self.side_effects_entry.get() == "":
            warn = " can't be empty please write YES or NO"
        else:
            check_counter += 1

        if check_counter == 3:
            try:
                con = sqlite3.connect('shms.db')
                cur = con.cursor()
                cur.execute("INSERT INTO feedback VALUES (:pat_username,:med_working, :improvement, :side_effects, :time, NULL)", {
                    'pat_username': p_un,
                    'med_working': self.med_working_entry.get(),
                    'improvement': self.improvement_entry.get(),
                    'side_effects': self.side_effects_entry.get(),
                    'time': datetime.datetime.now()


                })
    #             cur.execute("INSERT INTO doc_signup_info VALUES (?,?,NULL)",(doc_username,doc_password))
                con.commit()
                con.close()
                messagebox.showinfo(
                    'confirmation', 'Feedback Sent Sucessfully')
                self.master.destroy()
                self.main_screen3 = Tk()
                self.b = Vital(self.main_screen3)
#                     self.feedback_screen.destroy()

            except Exception as ep:
                messagebox.showerror('', ep)
        else:
            messagebox.showerror('Error', warn)

    def vital_disable_button(self):
        self.master.destroy()

    def back_button(self):
        self.master.destroy()
        global main_screen3
        self.main_screen3 = Tk()
        self.main_screen3.geometry("600x450")
        self.main_screen3.title("Feedback")
        self.b = Patient(self.main_screen3)

    def previous_data(self):

        self.r = tk.Tk()
        self.r.title("Customer Data")
        self.r.geometry("600x250")

        self.db = sqlite3.connect('shms.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(
            "SELECT * FROM daily_report where pat_username=?", (p_un,))

        self.tree = ttk.Treeview(self.r)
        self.tree["columns"] = ("pat_username", "bp", "sugar", "temp", "time")
        self.tree.column("pat_username", width=0,
                         minwidth=150, anchor=tk.CENTER)
        self.tree.column("bp", width=50, minwidth=100, anchor=tk.CENTER)
        self.tree.column("sugar", width=80, minwidth=100, anchor=tk.CENTER)
        self.tree.column("temp", width=100, minwidth=100, anchor=tk.CENTER)
        self.tree.column("time", width=150, minwidth=100, anchor=tk.CENTER)

        self.tree.heading("pat_username", text="username", anchor=tk.CENTER)
        self.tree.heading("bp", text="Blood Pressure", anchor=tk.CENTER)
        self.tree.heading("sugar", text="Blood Sugar", anchor=tk.CENTER)
        self.tree.heading("temp", text="Temperature", anchor=tk.CENTER)
        self.tree.heading("time", text="Date and Time", anchor=tk.CENTER)

        i = 0
        for row in self.cursor:
            self.tree.insert("", i, text="", values=(row[0], row[1], row[2]))
            i = i+1
        self.tree.pack()
        self.r.mainloop()


# %%
b = abstract_class()  # object creation


# %%


# %%
