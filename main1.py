from tkinter import *
from tkinter import ttk
import tkinter
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import customtkinter
import random
import tempfile
import os
import sqlite3
import logging
import datetime as dt
from PIL import ImageTk, Image
import string
import calendar
import geocoder
from geopy.geocoders import Nominatim
import re

#print("Intial updated")

# logging.basicConfig(filename='apollo_log.log',level=logging.DEBUG,
# format='%(asctime)s:%(levelname)s:%(message)s')

logging.basicConfig(filename='apollo_log.log',format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

def main():
    root = Tk()
    app = Login_Window(root)
    root.mainloop()

class Database():
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql_products = """
        CREATE TABLE IF NOT EXISTS products(
            id Integer Primary Key,
            product_name text,
            product_quantity text,
            product_mrp_price text,
            product_details text,
            product_cgst text,
            product_sgst text,
            product_purchase_price text
        )
        """

        sql_edit_products = """
        CREATE TABLE IF NOT EXISTS edit_products(
            id Integer Primary Key,
            product_name text,
            product_quantity text,
            product_mrp_price text,
            product_details text,
            product_cgst text,
            product_sgst text,
            product_purchase_disscount text,
            total_price text,
            profit_amount text
        )
        """

        sql_users_admins_super_admin = """
        CREATE TABLE IF NOT EXISTS users_admins_super_admin(
            user_id Integer Primary Key,
            username text,
            password text,
            email text,
            phone_no text,
            address text,
            admin text,
            user text,
            super_admin text,
            active text
        )
        """

        sql_customer_datas = """
        CREATE TABLE IF NOT EXISTS customer_datas(
            id Integer Primary Key,
            phone text,
            bill_no text,
            items text,
            quantity text,
            price text,
            total_price text,
            tax text,
            pay_amount,
            date_time text,
            username text,
            CGST text,
            SGST text,
            coupon_disscount_amount text,
            coupon_disscount_percentage text,
            final_pay text,
            float_price text

        )
        """
        sql_users = """
        CREATE TABLE IF NOT EXISTS users(
            id Integer Primary Key,
            username text,
            password text,
            email text,
            phone_no text,
            address text,
            active text,
            salary text
        )
        """
        
        sql_users_sal = """
        CREATE TABLE IF NOT EXISTS users_sal(
            id Integer Primary Key,
            username text,
            clockin_date text,
            clockin_time text,
            salary_per_day text
        )
        """
        sql_users_clockout = """
        CREATE TABLE IF NOT EXISTS users_clockout(
            id Integer Primary Key,
            username text,
            clockOut_date text,
            clockOut_time text,
            salary_per_day text
        )
        """
       
        sql_admins = """
        CREATE TABLE IF NOT EXISTS admins(
            id Integer Primary Key,
            username text,
            password text,
            email text,
            phone_no text,
            address text,
            active text
        )
        """

        sql_coupons = """
        CREATE TABLE IF NOT EXISTS coupons(
            id Integer Primary Key,
            coupon_code text,
            coupon_amount text

        )
        """

        sql_revenue = """
        CREATE TABLE IF NOT EXISTS revenue(
            id Integer Primary Key,
            date_time text,
            day_date text,
            bill_number text,
            total_sheet text,
            total_amount text,
            tax  text,
            mrp_amount text,
            given_disscount_amount text,
            got_disscount_amount text,
            profit_amount text,
            paid_amount text,
            float_price text

        )
        """

        sql_revenue_edit = """
        CREATE TABLE IF NOT EXISTS revenue_edit(
            id Integer Primary Key,
            date_time text,
            day_date text,
            bill_number text,
            total_sheet text,
            total_amount text,
            tax  text,
            mrp_amount text,
            given_disscount_amount text,
            got_disscount_amount text,
            profit_amount text,
            paid_amount text,
            float_price text

        )
        """
        sql_sal_structure = """
        CREATE TABLE IF NOT EXISTS sal_structure(
            id Integer Primary Key,
            basic_sal text, 
            hra text, 
            conveyance_allowance text, 
            medical_allowance text, 
            performance_bonus text, 
            PF text, 
            Esi text, 
            Tax text

        )
        """

        sql_admins_users = """
        CREATE TABLE IF NOT EXISTS admins_users(
            id Integer Primary Key,
            username text,
            password text,
            email text,
            phone_no text,
            address text,
            active text,
            salary text
        )
        """

        sql_queries = [sql_products, sql_edit_products, sql_users_admins_super_admin, sql_customer_datas, sql_users, sql_users_sal,sql_users_clockout, sql_admins, sql_coupons, sql_revenue, sql_revenue_edit, sql_sal_structure, sql_admins_users]
        for i in sql_queries:
            self.cur.execute(i)
            self.con.commit()
 
    def insert_income(self, date_time, day_date, bill_number, total_sheet, total_amount, tax, mrp_amount,given_disscount_amount,got_disscount_amount, profit_amount,paid_amount,float_price):
        '''Insert Function'''
        if  self.cur.execute("insert into Revenue values (NULL,?,?,?,?,?,?,?,?,?,?,?,?)",(date_time, day_date, bill_number, total_sheet, total_amount, tax,mrp_amount, given_disscount_amount, got_disscount_amount, profit_amount,paid_amount,float_price)):
            self.con.commit()
            logging.info('income history inserted successfully')

    def insert_income_edit(self, date_time, day_date, bill_number, total_sheet, total_amount, tax, mrp_amount,given_disscount_amount,got_disscount_amount, profit_amount,paid_amount,float_price):
        '''Insert Function'''
        if  self.cur.execute("insert into revenue_edit values (NULL,?,?,?,?,?,?,?,?,?,?,?,?)",(date_time, day_date, bill_number, total_sheet, total_amount, tax,mrp_amount, given_disscount_amount, got_disscount_amount, profit_amount,paid_amount,float_price)):
            self.con.commit()
            logging.info('income history inserted successfully')

    def insert_image(self, coupon_code, coupon_amount):
        '''Insert Function'''
        if  self.cur.execute("insert into images values (NULL,?,?)",(coupon_code, coupon_amount)):
            self.con.commit()
            logging.info('image generated successfully')

    def insert_coupon(self, coupon_code, coupon_amount):
        '''Insert Function'''
        if  self.cur.execute("insert into coupons values (NULL,?,?)",(coupon_code, coupon_amount)):
            self.con.commit()
            logging.info('Coupon generated successfully')
        else:
            logging.error('Coupon not generated by admin')

    def insert_User_register(self, username, password, email, phone_no, address, active, salary):
        '''Insert Function'''
        if  self.cur.execute("insert into USERS values (NULL,?,?,?,?,?,?,?)",(username, password, email, phone_no, address, active,salary)):
            self.con.commit()
            logging.info('User added successfully to the database')
        else:
            logging.error('User not added')
    #=============================Salary===============================
    # def insert_User_register(self, username, password, email, phone_no, address, active, salary,basic_sal,hra,conveyance_allowance,medical_allowance,performance_bonus,PF,Esi,Tax):
    #     '''Insert Function'''
    #     if  self.cur.execute("insert into USERS values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(username, password, email, phone_no, address, active, salary, basic_sal, hra, conveyance_allowance, medical_allowance, performance_bonus, PF, Esi, Tax)):
    #         self.con.commit()
    #         logging.debug('User added successfully to the database')
    #     else:
    #         logging.error('User not added')


    def insert_sal_structure(self, basic_sal, hra, conveyance_allowance, medical_allowance, performance_bonus, PF, Esi, Tax):
        '''Insert Function'''
        if  self.cur.execute("insert into sal_structure values (NULL,?,?,?,?,?,?,?,?)",(basic_sal, hra, conveyance_allowance, medical_allowance, performance_bonus, PF, Esi, Tax)):
            self.con.commit()
            logging.info('Sal Structure added successfully to the database')
        else:
            logging.error('Sal Structure not added')
    #=============================Salary==============================

    def insert_User_sal(self, username, clockin_date, clockin_time, salary_per_day):
        '''Insert Function'''
        if  self.cur.execute("insert into users_sal values (NULL,?,?,?,?)",(username, clockin_date, clockin_time, salary_per_day)):
            self.con.commit()
            logging.debug('User clocked-in successfully')
        else:
            logging.error('User not clocked-in')

    def insert_User_Clockout(self, username, clockin_date, clockin_time, salary_per_day):
        '''Insert Function'''
        if  self.cur.execute("insert into users_clockOut values (NULL,?,?,?,?)",(username, clockin_date, clockin_time, salary_per_day)):
            self.con.commit()
            #logging.debug('User clock-out successfully')
        else:
            logging.error('User not clock-out')

    def insert_admin_register(self, username, password, email, phone_no, address, active):
        '''Insert Function'''
        if  self.cur.execute("insert into admins values (NULL,?,?,?,?,?,?)",(username, password, email, phone_no, address, active)):
            self.con.commit()
            logging.info('product added successfully to the database')
        else:
            logging.error('item not added')

    def insert(self, product_name, product_quantity, product_mrp_price, product_details, product_cgst, product_sgst, product_purchase_price):
        '''Insert Function'''
        if  self.cur.execute("insert into products values (NULL,?,?,?,?,?,?,?)",(product_name, product_quantity, product_mrp_price, product_details, product_cgst, product_sgst, product_purchase_price)):
            self.con.commit()
            logging.info('product added successfully to the database')
        else:
            logging.error('item not added')

    def insert_to_edit_billing_area(self, items,quantity,price,Sheet):
        ''' inserting into edit area'''
        sheet_no = 0
        sheet_no = sheet_no+(int(Sheet))

        total_price=0
        total_price=total_price+(int(price)*int(Sheet))
        total_price=str(total_price)
        
        if  self.cur.execute("insert into edit_products values (NULL,?,?,?,?)",
                         (items,sheet_no,price,total_price)):
            self.con.commit()
            logging.info('item added successfully to the cart')
        else:
            logging.error('item not added to the cart')

    def insert_to_edit_area(self, items,Sheet,price,tablet_details,CGST_Amount,SGST_Amount,amount_purchased):  #(self, items,tablet_details,price,CGST_Amount,Sheet,SGST_Amount,amount_purchased):    #(self, items,quantity,price,Sheet):
        ''' inserting into edit area'''
        sheet_no = 0
        sheet_no = sheet_no+(int(Sheet))

        total_price=0
        total_price=total_price+(float(price)*int(Sheet))
        total_price=str(total_price)
       
        disscount_price = 0
        abc = float(amount_purchased) * 0.01
        disscount_price = float(total_price) * float(abc)
        print("disscount_price:",disscount_price)
        profit_price = float(total_price) - float(disscount_price)
        print("profit_price:",profit_price)

        if  self.cur.execute("insert into edit_products values (NULL,?,?,?,?,?,?,?,?,?)", #amount_purchased,CGST_Amount,SGST_Amount
                         (items,sheet_no,price,tablet_details,CGST_Amount,SGST_Amount,amount_purchased,total_price,disscount_price)):
            self.con.commit()
            logging.info('item added successfully to the cart')
        else:
            logging.error('item not added to the cart')

    def insert_to_customer_data(self,phone,bill_no,items,quantity,price,total_price,tax,totalbill1,bill_date,username,CGST,SGST,coupon_disscount_total,matched_coupon,final_pay_bill_amount,float_price):
        '''Customer data storing'''
        if self.cur.execute("insert into customer_datas values (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (phone,bill_no,items,quantity,price,total_price,tax,totalbill1,bill_date,username,CGST,SGST,coupon_disscount_total,matched_coupon,final_pay_bill_amount,float_price)):
            self.con.commit()
            logging.info('Customer data and bill added successfully in to the database')
        else:
            logging.error('Customer data and bill not added in to the database')

    def fetch(self):
        ''' Fetch All Data from DB'''
        self.cur.execute("SELECT * from products")
        rows = self.cur.fetchall()
        return rows

    def fetch_cupon(self):
        ''' Fetch All Data from DB'''
        self.cur.execute("SELECT * from coupons")
        rows = self.cur.fetchall()
        return rows

    def fetch_user(self):
        ''' Fetch All Data from DB'''
        self.cur.execute("SELECT id, username, email, phone_no, address, active from users")
        rows = self.cur.fetchall()
        return rows

    def fetch_admin(self):
        ''' Fetch All Data from DB'''
        self.cur.execute("SELECT id, username, email, phone_no, address, active from admins")
        rows = self.cur.fetchall()
        return rows

    def edit_fetch(self):
        self.cur.execute("SELECT * from edit_products")
        rows = self.cur.fetchall()
        return rows

    def edit_fetch_income(self):
        self.cur.execute("SELECT * from revenue_edit")
        rows = self.cur.fetchall()
        return rows

    def find_income(self):
        self.cur.execute("SELECT * from Revenue")
        rows = self.cur.fetchall()
        return rows

    def search_data(self):
        self.search_by = StringVar()
        self.search_txt = StringVar()
        if  self.cur.execute("SELECT * from products where "+str(self.search_by.get())+" LIKE '%"+str(self.search_txt.get())+"%'"):
            rows = self.cur.fetchall()
            logging.info('Searched items successfully from database')
            return rows
        else:
            logging.error('Cannot searched items successfully from database')

    def search_income(self,*args):
            self.search_day = StringVar()
            self.income_amounts = StringVar()
            self.cur.execute("SELECT * from Revenue where "+str(self.search_day.get())+" LIKE '%"+self.income_amounts.get()+"%'")
            rows=self.cur.fetchall()
            print("main:",rows)
            return rows

    def remove(self, id):
        '''Delete a Record in DB'''
        if self.cur.execute("delete from products where id=?", (id,)):
            self.con.commit()
            logging.info('Product removed successfully from database')
        else:
            logging.error('item not removed from database')

    def remove_oneitem_edit_area(self,id):
        if self.cur.execute("delete from edit_products where id=?", (id,)):
            self.con.commit()
            logging.info('item removed successfully from cart')
        else:
            logging.error('item not removed from cart')

    def remove_edit_area(self):
        if  self.cur.execute("delete from edit_products"):
            self.con.commit()
            logging.info('item removed successfully from cart')
        else:
            logging.error('item not removed from cart')

    def remove_edit_income(self):
        if  self.cur.execute("delete from revenue_edit"):
            self.con.commit()
            logging.info('item removed successfully from revenue_edit')
        else:
            logging.error('item not removed from revenue_edit')

    def remove_user(self, id):
        '''Delete a Record in DB'''
        if self.cur.execute("delete from users where id=?", (id,)):
            self.con.commit()
            logging.info('Product removed successfully from database')
        else:
            logging.error('item not removed from database')

    def remove_admin(self, id):
        '''Delete a Record in DB'''
        if self.cur.execute("delete from admins where id=?", (id,)):
            self.con.commit()
            logging.info('Product removed successfully from database')
        else:
            logging.error('item not removed from database')

    def remove_coupons(self, id):
        '''Delete a Record in DB'''
        if self.cur.execute("delete from coupons where id=?", (id,)):
            self.con.commit()
            logging.info('Product removed successfully from database')
        else:
            logging.error('item not removed from database')

    def update(self, product_name, product_quantity, product_mrp_price, product_details, product_cgst, product_sgst, product_purchase_price,id):
        '''Update a Record in DB'''
        if self.cur.execute("update products set product_name=?, product_quantity=?, product_mrp_price=?, product_details=?, product_cgst=?, product_sgst=?, product_purchase_price=? where id=?",
            (product_name, product_quantity, product_mrp_price, product_details, product_cgst, product_sgst, product_purchase_price, id)):
            self.con.commit()
            logging.info('Product updated successfully from database')
        else:
            logging.error('Product not updated from database')

    def update_quantity(self, product_quantity,id):
        '''Update a Record in DB'''
        if self.cur.execute("update products set  product_quantity=? where id=?",
            ( product_quantity, id)):
            self.con.commit()

    def update_user(self, username,password,email,phone_no,address,active,id):
        '''Update a Record in DB'''
        if self.cur.execute("update users set username=?, password=?, email=?, phone_no=?, address=?, active=? where id=?",
            (username,password,email,phone_no,address,active,id)):
            self.con.commit()
            logging.info('User updated successfully from database')
        else:
            logging.error('User not updated from database')


    #=========================================================================Salary Structure===================================
    def update_sal_structure(self, basic_sal, hra, conveyance_allowance, medical_allowance, performance_bonus, PF, Esi, Tax,id):
        '''Update a Record in DB'''
        if self.cur.execute("update sal_structure set basic_sal=?, hra=?, conveyance_allowance=?, medical_allowance=?, performance_bonus=?, PF=?, Esi=?, performance_bonus=?, Tax=? where id=?",
            (basic_sal, hra, conveyance_allowance, medical_allowance, performance_bonus, PF, Esi, Tax,id)):
            self.con.commit()
            logging.info('Updated sal structure successfully from database')
        else:
            logging.error('Sal structure not updated from database')
    #=============================================================================Salary Structure================================

    def update_user_edit(self, password,email,phone_no,address,id):
        '''Update a Record in DB'''
        if self.cur.execute("update users set password=?, email=?, phone_no=?, address=? where id=?",
            (password,email,phone_no,address,id)):
            self.con.commit()
            logging.info('User updated successfully from database')
        else:
            logging.error('User not updated from database')

    def update_admin(self, username,password,email,phone_no,address,active,id):
        '''Update a Record in DB'''
        if self.cur.execute("update admins set username=?, password=?, email=?, phone_no=?, address=?, active=? where id=?",
            (username,password,email,phone_no,address,active,id)):
            self.con.commit()
            logging.info('Admin updated successfully from database')
        else:
            logging.error('Admin not updated from database')

    def update_to_edit_area(self, items,number_of_sheets,per_sheet_price,id):
        total_price=0
        total_price=total_price+(int(number_of_sheets)*int(per_sheet_price))
        total_price=str(total_price)

        if  self.cur.execute("update edit_products set items=?, number_of_sheets=?, per_sheet_price=?, total_price=? where id=?",
                (items,number_of_sheets,per_sheet_price,total_price, id)):
            self.con.commit()
            logging.info('item updated successfully from cart')
        else:
            logging.error('item not updated from cart')


class Login_Window:
    def __init__(self,master):
        self.master = master
        self.master.title("Medical billing login page")
        self.master.geometry("1820x750")
        self.master.config(bg = 'powder blue')
        
        self.user_name = StringVar()
        self.password = StringVar()
        connection = sqlite3.connect('apollo.db')
        cursor = connection.cursor()

#====================================================================
        cursor.execute("SELECT username from admins_users")
        user_name=cursor.fetchall()
        print("user_name:",user_name)
        usr_na = ('Vishal',)

        if usr_na in user_name:
            print("User already exist")
        else:
            #cursor.execute("INSERT INTO admins_users VALUES('2','Vinodkumar', '123', 'vinod@gmail.com', '7529527927', 'Bangalore 7', 'Yes', 'Yes', 'No', '20000')")
            cursor.execute("insert into admins_users values (NULL,?,?,?,?,?,?,?,?,?)",('Vishal', '123', 'vishal@gmail.com', '7529527927', 'Bangalore 7', 'Yes', 'Yes', 'No', '20000'))
            connection.commit()
            print("Automatic user added")
        #===============droping table====================
        # cursor.execute("DROP TABLE users")
        # connection.commit()

        #================================================

        # command1 = """CREATE TABLE IF NOT EXISTS
        #         admins( id Integer Primary Key, username text, password text, email text, phone_no text, address text, active text)
        # """

        # cursor.execute(command1)
        #cursor.execute("INSERT INTO Revenue VALUES('8','2023-01-28 17:13:58.668627', '2023-01-28','1257','2','50','24','100','11','11','22','0.7')")
        #cursor.execute("INSERT INTO users VALUES('1','Vinod', '123', 'vinod@gmail.com', '7529527927', 'Bangalore 7', 'Yes', '20000')")
        # cursor.execute("INSERT INTO users VALUES('1','Vinod', '123', 'vinod@gmail.com', '7529527927', 'Bangalore 7', 'Yes', '20000','50','25','6','0','10','6','0.69','0.75')")
        #cursor.execute("INSERT INTO admins_users VALUES('2','Vinodkumar', '123', 'vinod@gmail.com', '7529527927', 'Bangalore 7', 'Yes', 'Yes', 'No', '20000')")
        #cursor.execute("INSERT INTO admins VALUES('1','Vinodkumar', '123', 'vinod@gmail.com', '7529527927', 'Bangalore 7', 'Yes')")
        #cursor.execute("INSERT INTO users_admins_super_admin VALUES('3','user', '123', 'vishal@gmail.com', '7575229997', 'Bangalore 77', 'No','Yes','No','Yes')")
        #cursor.execute("INSERT INTO users_sal VALUES('1','Vishal', '2023-02-08', '21:13:51.810933', '714.285714285714')")
        #cursor.execute("DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste')
        #cursor.execute("DELETE FROM users_sal where username LIKE '%"+str('Vishal')+"%'")
        #connection.commit()
#============================================================

        # img = Image.open('pic.jpg')
        try:
            img = Image.open('images/medical.webp')
            logo = img.resize((1100, 750), Image.Resampling.LANCZOS)
            logo = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.master,image=logo)
            logo_label.image = logo
            logo_label.place(width=1100, height=750)
        except Exception as e:
            logging.info(f'Error,{e}')
            print(e)

        self.frame1 = tkinter.Frame(self.master, bg = 'light blue')
        self.frame1.place(x=130, y=20, width=790, height=80)
        space = (9*" ")
        lblName = Label(master=self.frame1, text=f"{space} WELCOME TO APOLLO MEDICAL", font=("Calibri", 34), bg="powder blue", fg="black")
        lblName.grid(row=0, column=0,padx=10, pady=10)

        self.frame = tkinter.Frame(self.master, bg = 'powder blue')
        self.frame.place(x=1111, y=0, width=720, height=750)

        lblName = Label(master=self.frame, text="", font=("Calibri", 10), bg="powder blue", fg="black")
        lblName.grid(row=0, column=0,padx=10, pady=10)
        lblName = Label(master=self.frame, text="LOGIN", font=("Calibri", 32,'bold'), bg="powder blue", fg="black")
        lblName.grid(row=1, column=0,padx=10, pady=10)
        lblName = Label(master=self.frame, text="", font=("Calibri", 10), bg="powder blue", fg="black")
        lblName.grid(row=2, column=0,padx=10, pady=10)
        
        space1=(18*'_')
        lblName = Label(master=self.frame, text=f"{space1}User Name{space1}", font=("Calibri", 10), bg="powder blue", fg="black")
        lblName.grid(row=3, column=0,padx=10, pady=10)
        #lblName.pack()

        global user_name1
        user_name1 = customtkinter.CTkEntry(master=self.frame,placeholder_text="Username",border_color="black",textvariable=self.user_name,
        text_font=('Helvetica',18),width=300,height=50,border_width=2,corner_radius=10)
        user_name1.grid(row=4, column=0, sticky="w")
        #user_name1.pack()

        lblName = Label(master=self.frame, text=f"{space1}Password{space1}", font=("Calibri", 10), bg="powder blue", fg="black")
        lblName.grid(row=5, column=0,padx=10, pady=10)
        #lblName.pack(padx=0, pady=0)

        password1 = customtkinter.CTkEntry(master=self.frame,placeholder_text="Password",border_color="black",textvariable=self.password,
        text_font=('Helvetica', 18),width=300,height=50,show="*",border_width=2,corner_radius=10)
        password1.grid(row=6, column=0,padx=10, pady=10)

        lblName = Label(master=self.frame, text="", font=("Calibri", 10), bg="powder blue", fg="black")
        lblName.grid(row=7, column=0,padx=10, pady=10)

        button = customtkinter.CTkButton(master=self.frame,width=300,height=50,border_width=0,fg_color="Blue",text_color='white',corner_radius=8,
        text="Log In",text_font=('Helvetica', 14),command=lambda:[self.button_event()])
        button.grid(row=8, column=0,padx=10, pady=10)
        
        
#==============text===============================================================
    #     F11=LabelFrame(self.master, bd=10,relief=GROOVE, text="Customer Details",font=("times new roman", 10,"bold"),fg="white", bg="#535c68")
    #     F11.place(x=10,y=10, width=550)
    #     self.canvas=Canvas(F11,bg='black')
    #     self.canvas.pack(fill=BOTH, expand=1)
    #     text_var="Hey there Delilah!,What's it like in New York City."
    #     text=self.canvas.create_text(0,-2000,text=text_var,font=('Times New Roman',20,'bold'),fill='white',tags=("marquee",),anchor='w')
    #     x1,y1,x2,y2 = self.canvas.bbox("marquee")
    #     width = x2-x1
    #     height = y2-y1
    #     self.canvas['width']=width
    #     self.canvas['height']=height
    #     self.fps=40    #Change the fps to make the animation faster/slower
    #     self.shift()
    
    # def shift(self):
    #     x1,y1,x2,y2 = self.canvas.bbox("marquee")
    #     if(x2<0 or y1<0): #reset the coordinates
    #         x1 = self.canvas.winfo_width()
    #         y1 = self.canvas.winfo_height()//2
    #         self.canvas.coords("marquee",x1,y1)
    #     else:
    #         self.canvas.move("marquee", -2, 0)
    #     self.canvas.after(1000//self.fps,self.shift)
#======================text close===============================================

#==========================================================================================
        self.frame_auto_text = tkinter.Frame(self.master, bg = 'powder blue')
        self.frame_auto_text.place(x=1111, y=500, width=400, height=25)

        self.canvas=Canvas(self.frame_auto_text,bg='powder blue')
        self.canvas.pack(fill=BOTH, expand=1)
        text_var="Please provide your user name and password"
        text=self.canvas.create_text(0,-2000,text=text_var,font=('Times New Roman',14,'bold'),fill='Red',tags=("marquee",),anchor='w')
        x1,y1,x2,y2 = self.canvas.bbox("marquee")
        width = x2-x1
        height = y2-y1
        self.canvas['width']=width
        self.canvas['height']=height
        self.fps=70    #Change the fps to make the animation faster/slower
        self.shift()
    
    def shift(self):
        x1,y1,x2,y2 = self.canvas.bbox("marquee")
        if(x2<0 or y1<0): #reset the coordinates
            x1 = self.canvas.winfo_width()
            y1 = self.canvas.winfo_height()//2
            self.canvas.coords("marquee",x1,y1)
        else:
            self.canvas.move("marquee", -2, 0)
        self.canvas.after(1000//self.fps,self.shift)

#===========================================================================================
    # def button_event(self):
    #     try:
    #         connection = sqlite3.connect('apollo.db')
    #         cursor = connection.cursor()
    #         cursor.execute("SELECT * FROM admins where username LIKE '%"+str(self.user_name.get())+"%'")
    #         results = cursor.fetchall()
    #         print("results:",results)
    #         for result in results:
    #             global b
    #             b = self.user_name
    #             if self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[6]=='Yes':
    #                 logging.info('Login done by admins successfully from database')
    #                 Super_Admin_Window(self.master)

    #             else:
    #                 connection = sqlite3.connect('apollo.db')
    #                 cursor = connection.cursor()
    #                 cursor.execute("SELECT * from users where username LIKE '%"+str(self.user_name.get())+"%'")
    #                 results = cursor.fetchall()
    #                 print("User:",results)
    #                 self.a = StringVar()
    #                 for result in results:
    #                     if self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[6]=='Yes':
    #                         global a,ai, user_pass_edit, user_email_edit,user_ph_no,user_address_edit,user_admin_edit,user_name_edit,user_password_edit
    #                         a = self.user_name
    #                         print("userssssssssssssssssssss:",a.get())
    #                         user_pass_edit = self.password
    #                         user_name_edit = result[1]
    #                         user_password_edit = result[2]
    #                         user_email_edit = result[3]
    #                         user_ph_no = result[4]
    #                         user_address_edit = result[5]
    #                         user_admin_edit = result[6]
    #                         ai = result[0]
    #                         logging.info('Login done by users successfully')
    #                         User_Window(self.master)
        # except Exception as ex:
        #     print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        #     logging.info('Please provide correct data')
        #     #logging.info(f'Error due to {str(ex)}, Please provide username and password')
        #     messagebox.showerror("Error",f"Error due to {str(ex)}")
        # finally: 
        #     if results == []:
        #         logging.info('Provided usersname and password are not correct')
        #         messagebox.showerror("Error","Please provide correct username or password")



    # def button_event(self):
    #     connection = sqlite3.connect('apollo.db')
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * from users_admins_super_admin")
    #     results = cursor.fetchall()

    #     self.a = StringVar()

    #     for result in results:
    #         global user_name, password_user, admin_w, active_user
    #         user_name = result[1]
    #         password_user = result[2]
    #         admin_w = result[6]
    #         active_user = result[9]
    #         if self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[7]=='Yes' and result[9]=='Yes':
    #             global a,ai, user_pass_edit, user_email_edit,user_ph_no,user_address_edit,user_admin_edit,user_name_edit,user_password_edit

    #             a = self.user_name
    #             print("userssssssssssssssssssss:",a.get())
    #             user_pass_edit = self.password
    #             user_name_edit = result[1]
    #             user_password_edit = result[2]
    #             user_email_edit = result[3]
    #             user_ph_no = result[4]
    #             user_address_edit = result[5]
    #             user_admin_edit = result[6]
    #             ai = result[0]

    #             User_Window(self.master)
    #             logging.info('Login done by users successfully')

    #         if self.user_name.get() ==  user_name and self.password.get() == password_user and admin_w=='Yes' and result[9]=='Yes':
    #             # connection = sqlite3.connect('apollo.db')
    #             # cursor = connection.cursor()
    #             # cursor.execute("SELECT * from users_admins_super_admin")
    #             # results = cursor.fetchall()
    #             #self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[6]=='Yes' and result[9]=='Yes'
    #             Window_admin(self.master) 

    #         else:
    #             connection = sqlite3.connect('apollo.db')
    #             cursor = connection.cursor()
    #             cursor.execute("SELECT * FROM users_admins_super_admin where username LIKE '%"+str(self.user_name.get())+"%'")
    #             #cursor.execute("SELECT * from admins")
    #             results = cursor.fetchall()
    #             for result in results:
    #                 global b
    #                 b = self.user_name.get()
    #                 if self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[8]=='Yes' and result[9]=='Yes':
    #                     logging.debug('Login done by admins successfully from database')
    #                     Super_Admin_Window(self.master)
    
    def button_event(self):
        try:
            connection = sqlite3.connect('apollo.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admins_users where username LIKE '%"+str(self.user_name.get())+"%'")
            results = cursor.fetchall()
            print("results:",results)
            for result in results:
                global b, a, user_name_display
                user_name_display = self.user_name.get()
                a = self.user_name.get()
                print("a:",a)
                b = self.user_name.get()
                print(b)
                if self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[6]=='Yes' and result[7]=='Yes':
                    logging.info('Login done by admins successfully from database')
                    Super_Admin_Window(self.master)
                else:
                    a = self.user_name.get()
                    self.user_name.get() ==  result[1] and self.password.get() == result[2] and result[6]=='Yes' and result[8]=='Yes'
                    User_Window(self.master)

        except Exception as ex:
            print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
            logging.info('Please provide correct data')
            #logging.info(f'Error due to {str(ex)}, Please provide username and password')
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        finally: 
            if results == []:
                logging.error('Provided usersname and password are not correct')
                messagebox.showerror("Error","Please provide correct username or password")

    def new_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Super_Admin_Window(self.newWindow)

    def new_user_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = User_Window(self.newWindow)

    def new_user_data(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_user_register(self.newWindow)

    def edit_user_data(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_user_edit(self.newWindow)

    def coupon_data(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_coupon_edit(self.newWindow)

    def back_button(self):
        self.newWindow = Toplevel(self.master)
        self.app = Login_Window(self.newWindow)

    def income_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_income(self.newWindow)
        
    def add_product_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_add_products(self.newWindow)

    def admin_bill_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_admin(self.newWindow)

    def admin_bill_search(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_Bill_Search(self.newWindow)

    def emp_salary(self):
        self.newWindow = Toplevel(self.master)
        self.app = Window_emp(self.newWindow)


class Super_Admin_Window(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("1920x1080+0+0")
        self.master.config(bg = '#2c3e50')

        # img = Image.open('tablet.jpg')
        # img = Image.open('pic.jpg')
        img = Image.open('images/a2.webp')
        logo = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.master,image=logo)
        logo_label.image = logo
        logo_label.place(width=1920, height=1080)

        date_timing = dt.datetime.now()
        date_time_login = date_timing.strftime("%H:%M:%S:%p:%A")
        
        self.entries_frame1 = Frame(self.master,bg="#535c68")
        self.entries_frame1.place(x=0, y=0, width=457, height=935)

        img = Image.open('images/a1.jpg')
        logo = img.resize((150, 150), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.entries_frame1,image=logo)
        logo_label.image = logo
        logo_label.place(x=50,y=50,width=150, height=150)
        '''Empty'''
        self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=0, column=0,padx=10,pady=100, sticky="w")

        self.lblAdmin = Label(self.entries_frame1, textvariable=b, font=("Times new roman", 22,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=1, column=0,padx=10, sticky="w")

        label = Label(self.entries_frame1, text=f"{date_time_login}", font=("Times new roman", 18,'bold'), bg="white", fg="black")
        label.grid(row=2, column=0,padx=10,pady=10, sticky="w")

        self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=3, column=1,padx=10,pady=150, sticky="w")

        self.button = customtkinter.CTkButton(self.entries_frame1,width=18,height=30,border_width=0,fg_color="red",text_color="white",corner_radius=18,
        text="Logout",text_font=('Times new roman', 18,'bold'),command=self.exit).grid(row=4, column=0,padx=2)

        self.entries_frame_label = Frame(self.master,bg="sky blue")
        self.entries_frame_label.place(x=470, y=10, width=1075, height=70)
        title = Label(self.entries_frame_label, text="APOLLO MEDICAL HITECH-CITY GACHIBOWLI HYDERABAD", font=("Times new roman", 24, "bold"), bg="sky blue", fg="black")
        title.grid(row=0, columnspan=2, sticky="w")
        #==========================================Automatic timer===============================
        # self.canvas=Canvas(self.entries_frame_label,bg='black')
        # self.canvas.pack(fill=BOTH, expand=1)
        # text_var="APOLLO MEDICAL HITECH-CITY GACHIBOWLI HYDERABAD 500084"
        # text=self.canvas.create_text(0,-2000,text=text_var,font=('Times New Roman',26,'bold'),fill='white',tags=("marquee",),anchor='w')
        # x1,y1,x2,y2 = self.canvas.bbox("marquee")
        # width = x2-x1
        # height = y2-y1
        # self.canvas['width']=width
        # self.canvas['height']=height
        # self.fps=60    #Change the fps to make the animation faster/slower
        # self.shift()
    
    #==================================automatic timer close========================================

        self.entries_frame = Frame(self.master,bg="sky blue")
        self.entries_frame.place(x=600, y=150, width=720, height=360)

        photo_add_cart = PhotoImage(file = r"images/cart.png").subsample(4, 4)
        self.button = customtkinter.CTkButton(self.entries_frame,width=18,height=30,border_width=0,corner_radius=0,fg_color="green",text_color="white",image = photo_add_cart,
        text="Add Product",text_font=('times new roman', 14,'bold'),command=lambda:[self.add_product_window()]).grid(row=0, column=0,padx=20,pady=30, sticky="w")
        
        photoimage_user = PhotoImage(file = r"images/add user.png").subsample(4, 4)
        self.button = customtkinter.CTkButton(self.entries_frame,width=18,height=30,border_width=0,corner_radius=0,fg_color="green",text_color="white",image = photoimage_user,
        text="Add User",text_font=('times new roman', 14,'bold'),command=lambda:[self.new_user_data()]).grid(row=0, column=1,padx=20,pady=30, sticky="w")

        photo_coupon = PhotoImage(file = r"images/coupons.png").subsample(4, 4)
        self.button = customtkinter.CTkButton(self.entries_frame,width=18,height=30,border_width=0,corner_radius=0,fg_color="green",text_color="white",image = photo_coupon,
        text="Disscount%",text_font=('times new roman', 14,'bold'),command=lambda:[self.coupon_data()]).grid(row=0, column=2,padx=20,pady=30, sticky="w")
        
        '''income'''
        photoimage = PhotoImage(file = r"images/revenuee.png").subsample(4, 4)
        self.button = customtkinter.CTkButton(self.entries_frame,width=18,height=30,border_width=0,corner_radius=0,fg_color="green",text_color="white", image = photoimage,
        text="Revenue ",text_font=('Times new roman', 14,'bold'),command=lambda:[self.income_window()]).grid(row=1, column=1,padx=20,pady=30, sticky="w")
        
        photo_search = PhotoImage(file = r"images/search.png").subsample(4, 4)
        self.button = customtkinter.CTkButton(self.entries_frame,width=18,height=30,border_width=0,corner_radius=0,fg_color="green",text_color="white",image = photo_search,
        text="Bill History ",text_font=('Times new roman', 14,'bold'),command=lambda:[self.admin_bill_search()]).grid(row=1, column=0,padx=30,pady=20, sticky="w")
        
        photo_sal = PhotoImage(file = r"images/emp sal.png").subsample(4, 4)
        self.button = customtkinter.CTkButton(self.entries_frame,width=18,height=30,border_width=0,corner_radius=0,fg_color="green",text_color="white",image = photo_sal,
        text="Emp Salary",text_font=('Times new roman', 14,'bold'),command=lambda:[self.emp_salary()]).grid(row=1, column=2,padx=20,pady=30, sticky="w")
        
    def exit(self):
        if messagebox.askyesno('Exit','Do you really want to exit'):
            self.master.destroy()
            logging.info('Exited Successfully')

    def shift(self):
        x1,y1,x2,y2 = self.canvas.bbox("marquee")
        if(x2<0 or y1<0):
            x1 = self.canvas.winfo_width()
            y1 = self.canvas.winfo_height()//2
            self.canvas.coords("marquee",x1,y1)
        else:
            self.canvas.move("marquee", -2, 0)
        self.canvas.after(1000//self.fps,self.shift)


class Window_admin(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("1920x1080+0+0")
        self.master.config(bg = '#2c3e50')

        self.items = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.search_bill = StringVar()
        self.search_by1 = StringVar()
        self.Total_price=StringVar()
        self.total_price=StringVar()
        self.tablet_details=StringVar()
        self.user_name = StringVar()
        
        self.Sheet=StringVar()

        self.c_phone=StringVar()
        self.bill_no=StringVar()

        self.tax2=StringVar()
        self.totalbill=StringVar()
        self.total_quantity=StringVar()

        self.coupons=StringVar()
        self.coupon_total_pay = StringVar()
        self.amount_purchased = StringVar()
        self.CGST_Amount = StringVar()
        self.SGST_Amount = StringVar()

        self.entries_frame1 = Frame(self.master,bg="#535c68")
        self.entries_frame1.place(x=986, y=0, width=557, height=135)
        '''Empty'''
        self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=0, column=0,padx=1, sticky="w")

        self.lblAdmin = Label(self.entries_frame1, text = "Welcome",font=("Times new roman", 18,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=1, column=0,padx=1, sticky="w")

        self.lblAdmin = Label(self.entries_frame1, textvariable=b, font=("Times new roman", 18,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=1, column=1,padx=1, sticky="w")

        '''Empty'''
        self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="#535c68", fg="white")
        self.lblAdmin.grid(row=2, column=0,padx=1, sticky="w")

        self.button = customtkinter.CTkButton(self.entries_frame1,width=8,height=20,border_width=0,fg_color="red",text_color="white",corner_radius=8,
        text="Logout",text_font=('Helvetica', 12,'bold'),command=self.exit).grid(row=3, column=2,padx=2)

        self.button = customtkinter.CTkButton(self.entries_frame1,width=8,height=20,border_width=0,corner_radius=8,
        text="Register User",text_font=('Helvetica', 12,'bold'),command=self.new_user_data).grid(row=3, column=1,padx=2)

        self.button = customtkinter.CTkButton(self.entries_frame1,width=8,height=20,border_width=0,corner_radius=8,
        text="Create Coupon",text_font=('Helvetica', 12,'bold'),command=self.coupon_data).grid(row=3, column=0,padx=2)

        # self.button = customtkinter.CTkButton(self.entries_frame1,width=8,height=20,border_width=0,corner_radius=8,
        # text="Create Coupon",text_font=('Helvetica', 12,'bold'),command=self.clockin).grid(row=3, column=1,padx=2)
        #============================login display close=============================
        #==================login display=================================
        # self.entries_frame1 = Frame(self.master,bg="purple")
        # self.entries_frame1.place(x=1116, y=0, width=557, height=135)
        # '''Empty'''
        # self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="purple", fg="white")
        # self.lblAdmin.grid(row=0, column=0,padx=1, sticky="w")

        # self.lblAdmin = Label(self.entries_frame1, text = "Welcome",font=("Times new roman", 18,'bold'), bg="purple", fg="white")
        # self.lblAdmin.grid(row=1, column=0,padx=1, sticky="w")

        # self.lblAdmin = Label(self.entries_frame1, textvariable=a, font=("Times new roman", 18,'bold'), bg="purple", fg="white")
        # self.lblAdmin.grid(row=1, column=1,padx=1, sticky="w")
        
        # '''Empty'''
        # self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="purple", fg="white")
        # self.lblAdmin.grid(row=2, column=0,padx=1, sticky="w")
        
        # self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        # text="Logout",text_font=('Helvetica', 12),command=self.exit).grid(row=3, column=1,padx=10)

        # self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        # text="Clockin",text_font=('Helvetica', 12),command=lambda:[self.clockin()]).grid(row=3, column=2,padx=10)
        # self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        # text="Clockin",text_font=('Helvetica', 12),command=lambda:[self.clockin1()]).grid(row=3, column=3,padx=10)

        # self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "green",text_color = "White",corner_radius=8,
        # text="Edit profile",text_font=('Helvetica', 12),command=self.edit_user_data).grid(row=3, column=0,padx=10)
        #===============================login display close===================================
        
        self.entries_frame = Frame(self.master,bg="#535c68")
        self.entries_frame.place(x=0, y=0, width=975, height=225)
        
        title = Label(self.entries_frame, text="BILLING SYSTEM", font=("Calibri", 14, "bold"), bg="#535c68", fg="white")
        title.grid(row=0, columnspan=2, sticky="w")
        
        self.lblName = Label(self.entries_frame, text="Product_Name", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblName.grid(row=1, column=0,pady = 5, sticky="w")
        self.txtName = Entry(self.entries_frame, textvariable=self.items, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtName.grid(row=1, column=1,pady = 5, sticky="w")

        self.lblMrp_Price = Label(self.entries_frame, text="Product_MRP_Price", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblMrp_Price.grid(row=2, column=0,pady = 5, sticky="w")
        self.txtMrp_Price = Entry(self.entries_frame, textvariable=self.price, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtMrp_Price.grid(row=2, column=1,pady = 5, sticky="w")

        self.lblQuantity = Label(self.entries_frame, text="Product_Quantity", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblQuantity.grid(row=3, column=0,pady = 5, sticky="w")
        self.txtQuantity = Entry(self.entries_frame, textvariable=self.quantity, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtQuantity.grid(row=3, column=1,pady = 5, sticky="w")
 
        self.lblamount_purchased = Label(self.entries_frame, text="Purchased_disscount%", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblamount_purchased.grid(row=1, column=2,pady = 5, sticky="w")
        self.txtamount_purchased = Entry(self.entries_frame, textvariable=self.amount_purchased, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtamount_purchased.grid(row=1, column=3,pady = 5, sticky="w")

        self.lblCGST = Label(self.entries_frame, text="CGST%", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblCGST.grid(row=2, column=2,pady = 5, sticky="w")
        self.txtCGST = Entry(self.entries_frame, textvariable=self.CGST_Amount, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtCGST.grid(row=2, column=3,pady = 5, sticky="w")

        self.lblSGST = Label(self.entries_frame, text="SGST%", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblSGST.grid(row=3, column=2,pady = 5, sticky="w")
        self.txtSGST = Entry(self.entries_frame, textvariable=self.SGST_Amount, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtSGST.grid(row=3, column=3,pady = 5, sticky="w")
        '''Sheet'''

        self.lblSheet = Label(self.entries_frame, text="Strip/Sheet", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblSheet.grid(row=4, column=2,padx=1, sticky="w")

        self.txtSheet = Entry(self.entries_frame, textvariable=self.Sheet, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtSheet.grid(row=4, column=3, sticky="w")

       
        self.lblTablet_details = Label(self.entries_frame, text="Tablet_details", font=("Calibri", 10), bg="#535c68", fg="white")
        self.lblTablet_details.grid(row=4, column=0, sticky="w")
        self.txtTablet_deatails = Entry(self.entries_frame, textvariable=self.tablet_details, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtTablet_deatails.grid(row=4, column=1, sticky="w")
        

        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Add Product",text_font=('Helvetica', 8,'bold'),command=self.add_items).grid(row=1, column=6,padx=2)

        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Update Product",text_font=('Helvetica', 8,'bold'),command=self.update_items).grid(row=2, column=6,padx=2)
        
        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Delete Product",text_font=('Helvetica', 8,'bold'),command=self.delete_items).grid(row=3, column=6,padx=2)

        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Clear Product",text_font=('Helvetica', 8,'bold'),command=self.clearAll).grid(row=4, column=6,padx=2)

        '''Table Frame (displaying data from data base)'''
        tree_frame = Frame(self.master,bg="#535c68")
        tree_frame.place(x=0, y=235, width=535, height=390)

        lbl_search=Label(tree_frame,text="Search Products",bg="green",fg="white",font=("times new roman",14,"bold"))
        lbl_search.grid(row=0,column=0,pady=5,padx=5,sticky="w")

        txt_Search= Entry(tree_frame,textvariable=self.search_txt,width=20,font=("times new roman",10,"bold") ,bd=5,relief=GROOVE)
        txt_Search.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        txt_Search.bind("<Key>",self.search)

        '''Table Show Data'''
        Table_Frame=Frame(tree_frame,relief=RIDGE,bg="crimson")
        Table_Frame.place(x=10,y=70,width=515,height=300)
        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        self.billing_table=ttk.Treeview(Table_Frame,columns=("ProductID","Products","Quantity","MRP_Price","product_details","CGST","SGST","Purchase_price"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)

        self.billing_table.heading("ProductID",text="ProductID")
        self.billing_table.heading("Products",text="Products")
        self.billing_table.heading("Quantity",text="quantity")
        self.billing_table.heading("MRP_Price",text="MRP_Price")
        self.billing_table.heading("product_details",text="product_details")
        self.billing_table.heading("CGST",text="CGST")
        self.billing_table.heading("SGST",text="SGST")
        self.billing_table.heading("Purchase_price",text="Purchase_price")
        self.billing_table['show']='headings'
        self.billing_table.column("ProductID",width=2)
        self.billing_table.column("Products",width=100)
        self.billing_table.column("Quantity",width=10)
        self.billing_table.column("MRP_Price",width=20)
        self.billing_table.column("product_details",width=20)
        self.billing_table.column("CGST",width=10)
        self.billing_table.column("SGST",width=20)
        self.billing_table.column("Purchase_price",width=20)
        self.billing_table.pack(fill=BOTH,expand=1)
        self.billing_table.bind("<ButtonRelease-1>",self.getData)

        '''displaying bill area and dimenions'''
        '''Customer Details'''
        F1=LabelFrame(self.master, bd=10,relief=GROOVE, text="Customer Details",font=("times new roman", 10,"bold"),fg="white", bg="#535c68")
        F1.place(x=980,y=136, width=550)

        self.cphn_lbl=Label(F1,text="Phone No.",bg="#535c68",fg="white", font=("times new roman",15,"bold")).grid(row=0,column=2,padx=20,pady=5)
        self.txtPhone=Entry(F1,width=15,font="arial 15",bd=7,relief=SUNKEN,textvariable=self.c_phone).grid(row=0, column=3,pady=5,padx=10)

        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.master,bg="#535c68",bd=10,relief=GROOVE)
        self.billing_area.place(x=980, y=214, width=550, height=470)
        self.billing_tiltle=Label(self.billing_area,text="Bill Area",font="arial 15 bold",fg="white",bg="#535c68",bd=7,relief=GROOVE).pack(fill=X)

        scroll_y=Scrollbar(self.billing_area,orient=VERTICAL)
        self.billing_area=Text(self.billing_area,yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH,expand=1)
        self.welcome_default()

        '''Bill Menu'''
        self.button_frame=LabelFrame(self.master,bg="#535c68",bd=10,relief=GROOVE)
        self.button_frame.place(x=980,y=685,width=550,height=100)

        '''Total Calculate Menue'''
        self.button_Total_frame=LabelFrame(self.master,bg="#535c68",bd=10,relief=GROOVE)
        self.button_Total_frame.place(x=0,y=630,width=975,height=157)

        self.cphn_lbl1=Label(self.button_Total_frame,text="Total",bg="#535c68",fg="white", font=("times new roman",18,"bold")).grid(row=0,column=2,padx=20,pady=5)
        self.cphn_ibl1=Entry(self.button_Total_frame,textvariable=self.Total_price,width=15,font="arial 15",bd=7,relief=SUNKEN).grid(row=0, column=3,pady=5,padx=10)

        self.cphn_lbl2=Label(self.button_Total_frame,text="Tax",bg="#535c68",fg="white", font=("times new roman",18,"bold")).grid(row=1,column=2,padx=20,pady=5)
        self.cphn_ibl2=Entry(self.button_Total_frame,textvariable=self.tax2,width=15,font="arial 15",bd=7,relief=SUNKEN).grid(row=1, column=3,pady=5,padx=10)

        self.cphn_lbl3=Label(self.button_Total_frame,text="Total Quantity",bg="#535c68",fg="white", font=("times new roman",18,"bold")).grid(row=0,column=4,padx=20,pady=5)
        self.cphn_ibl3=Entry(self.button_Total_frame,textvariable=self.total_quantity,width=15,font="arial 15",bd=7,relief=SUNKEN).grid(row=0, column=5,pady=5,padx=10)

        self.cphn_lbl3=Label(self.button_Total_frame,text="Amount",bg="#535c68",fg="white", font=("times new roman",18,"bold")).grid(row=1,column=4,padx=20,pady=5)
        self.cphn_ibl3=Entry(self.button_Total_frame,textvariable=self.totalbill,width=15,font="arial 15",bd=7,relief=SUNKEN).grid(row=1, column=5,pady=5,padx=10)
        '''Coupons_Button'''
        self.lblcphn_Coupon=Label(self.button_Total_frame,text="Disscount%",bg="#535c68",fg="white", font=("times new roman",18,"bold")).grid(row=0,column=6,padx=5,pady=5)
        self.txtcphn_coupon=Entry(self.button_Total_frame,textvariable=self.coupons,width=10,font="arial 15",bd=7,relief=SUNKEN).grid(row=0, column=7,pady=5,padx=5)

        self.cphn_Coupon_Total=Label(self.button_Total_frame,text="Amount",bg="#535c68",fg="white", font=("times new roman",18,"bold")).grid(row=1,column=6,padx=5,pady=5)
        self.cphn_coupon_total=Entry(self.button_Total_frame,textvariable=self.coupon_total_pay,width=10,font="arial 15",bd=7,relief=SUNKEN).grid(row=1, column=7,pady=5,padx=5)

        '''Buttons'''
        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,
        text="Total",text_font=('Times new roman', 18),command=self.total).grid(row=0, column=0,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,
        text="Bill",text_font=('Times new roman', 18),command=lambda:[self.gbill(),self.add_income(),self.store_customer_data(),self.disable_text(),self.delete_edit_area()]).grid(row=0, column=1,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,
        text="Print",text_font=('Times new roman', 18),command=self.print_bill).grid(row=0, column=2,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,
        text="Clear",text_font=('Times new roman', 18),command=lambda:[self.clear_bill(),self.clear_bill_text()]).grid(row=0, column=3,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,
        text="ApplyCoupon",text_font=('Times new roman', 18),command=lambda:[self.conform_coupon()]).grid(row=0, column=4,padx=5,pady=5)
        
        '''CART'''
        '''displaying data of edit area'''
        '''displaying edit area'''
        self.billing_edit = Frame(self.master,bg="#535c68")
        self.billing_edit.place(x=538, y=235, width=440, height=390)

        self.lbl_edit=Label(self.billing_edit,text="Cart",bg="#535c68",fg="white",font=("times new roman",14,"bold"))
        self.lbl_edit.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        button = customtkinter.CTkButton(self.billing_edit,width=8,height=20,border_width=0,corner_radius=8,
        text="Add Cart",text_font=('Helvetica', 8),command=lambda:[self.update_items_quantity(),self.add_to_edit_area()]).grid(row=1, column=0,padx=2)

        button = customtkinter.CTkButton(self.billing_edit,width=8,height=20,border_width=0,corner_radius=8,
        text="Update Cart",text_font=('Helvetica', 8),command=self.update_edit_area).grid(row=1, column=1,padx=2)

        button = customtkinter.CTkButton(self.billing_edit,width=8,height=20,border_width=0,corner_radius=8,
        text="Delete Cart",text_font=('Helvetica', 8),command=lambda:[self.update_items_quantity_after_delete_cart(),self.delete_oneitem_edit_area()]).grid(row=1, column=2,padx=2)

        self.combo_search=ttk.Combobox(self.billing_edit,textvariable=self.search_by1,width=7,font=("times new roman",11,"bold"),state='readonly')
        self.combo_search['values']=("bill_no")
        self.combo_search.grid(row=0,column=1,padx=5,pady=5)
        self.search_btn = Button(self.billing_edit,text="Search_Customer_Bill",bg="skyblue", width=17,pady=5,command=lambda:[self.user_bill()]).grid(row=0, column=3,padx=5,pady=5)
        self.txtBillSearch=Entry(self.billing_edit,width=9,font="arial 11",bd=7,relief=SUNKEN,textvariable=self.search_bill).grid(row=0, column=2,pady=5,padx=10)

        self.edit_Table_Frame=Frame(self.billing_edit,relief=RIDGE,bg="white")
        self.edit_Table_Frame.place(x=10,y=79,width=421,height=290)
        scroll_x=Scrollbar(self.edit_Table_Frame,orient=HORIZONTAL)
        
        self.edit_billing_table=ttk.Treeview(self.edit_Table_Frame,columns=("ProductID","Products","Quantity","MRP_Price","product_details","CGST","SGST","Purchase_price","total_price"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
       
        scroll_x.config(command=self.edit_billing_table.xview)

        self.edit_billing_table.heading("ProductID",text="ProductID")
        self.edit_billing_table.heading("Products",text="Products")
        self.edit_billing_table.heading("Quantity",text="quantity")
        self.edit_billing_table.heading("MRP_Price",text="MRP_Price")
        self.edit_billing_table.heading("product_details",text="product_details")
        self.edit_billing_table.heading("CGST",text="CGST")
        self.edit_billing_table.heading("SGST",text="SGST")
        self.edit_billing_table.heading("Purchase_price",text="Purchase_price")
        self.edit_billing_table.heading("total_price",text="total_price")
        self.edit_billing_table['show']='headings'
        self.edit_billing_table.column("ProductID",width=2)
        self.edit_billing_table.column("Products",width=100)
        self.edit_billing_table.column("Quantity",width=10)
        self.edit_billing_table.column("MRP_Price",width=20)
        self.edit_billing_table.column("product_details",width=20)
        self.edit_billing_table.column("CGST",width=10)
        self.edit_billing_table.column("SGST",width=20)
        self.edit_billing_table.column("Purchase_price",width=20)
        self.edit_billing_table.column("total_price",width=20)
        
        self.edit_billing_table.pack(fill=BOTH,expand=1)
        self.edit_billing_table.bind("<ButtonRelease-1>",self.edit_area_getData)
        self.dispalyAll_edit_area()

        self.style = ttk.Style()
        self.style.configure("Treeview",background='#7FFFD4', foreground='black', font=('Calibri', 12),rowheight=20)
        self.style.configure("Treeview.Heading",background='blue', foreground='purple',relief='flat', font=('Calibri', 12))

    def remove_edit_area(self):
        '''Deletes the products from cart'''
        if  self.cur.execute("delete from edit_products"):
            self.con.commit()
            logging.info('item removed successfully from cart')
        else:
            logging.error('item not removed from cart')

    def getData(self,event):
        '''It will get data from database and display it'''
        self.clearAll()
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]
        print(row)
        global quantity_set
        quantity_set = row[2]
        self.items.set(row[1])
        self.quantity.set(row[2])
        self.price.set(row[3])
        self.tablet_details.set(row[4])   
        self.SGST_Amount.set(row[5])           
        self.CGST_Amount.set(row[6])
        self.amount_purchased.set(row[7])

    def edit_area_getData(self):
        self.clearAll()
        selected_row = self.edit_billing_table.focus()
        data = self.edit_billing_table.item(selected_row)
        global row
        row = data["values"]

        self.items.set(row[1])
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.items.get())+"%'")
        quantity_rows1 = cur.fetchall()
        for quantity_row in quantity_rows1:
            self.quantity.set(quantity_row[2])
        
        self.price.set(row[3])
        self.tablet_details.set(row[4])   
        self.SGST_Amount.set(row[5])           
        self.CGST_Amount.set(row[6])
        self.amount_purchased.set(row[7])
        self.total_price.set(row[8])
        self.Sheet.set(row[2])

    def dispalyAll(self):
        ''' This method will display all aitems from database'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.fetch():
            self.billing_table.insert("", END, values=row)

    def dispalyAll_edit_area(self):
        self.edit_billing_table.delete(*self.edit_billing_table.get_children())
        for row in self.db.edit_fetch():
            self.edit_billing_table.insert("", END, values=row)

    def search_dispalyAll(self):
        '''It will search the products from database according to there alphabets'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.search_data():
            self.billing_table.insert("", END, values=row)

    def add_items(self):
        '''This method will add products'''
        if self.txtName.get() == "":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        txt_Name = float(self.txtMrp_Price.get())
        self.db.insert(self.txtName.get(),self.txtQuantity.get(),txt_Name,self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get())
        self.clearAll()
        self.dispalyAll()

    def update_items(self):
        '''This method will update products'''
        self.db.update(self.txtName.get(),self.txtQuantity.get(),self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),row[0])
        messagebox.showinfo("Success", "Record Update")
        logging.info('Updated products successfully')
        self.clearAll()
        self.dispalyAll()

    '''update_quantity'''
    def update_items_quantity(self):
        '''This method will update quantity'''
        quantity_reduce = int(self.txtQuantity.get()) - int(self.txtSheet.get())
        self.db.update(self.txtName.get(),quantity_reduce,self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),row[0])
    
    def update_items_quantity_after_delete_cart(self):
        '''This method will update quantity'''
        quantity_add = int(self.txtQuantity.get()) + int(self.txtSheet.get())
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.items.get())+"%'")
        quantity_rows = cur.fetchall()
        for quantity_row in quantity_rows:
            quanti = quantity_row[0]
        self.db.update(self.txtName.get(),quantity_add,self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),quantity_row[0])

    def update_edit_area(self):
        if self.txtSheet.get()=="":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        self.db.update_to_edit_area(self.txtName.get(),self.txtQuantity.get(),self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),row[0])
        
        messagebox.showinfo("Success", "Record Update")
        logging.info('Updated products from cart')
        self.clearAll()
        self.dispalyAll_edit_area()

    def delete_items(self):
        self.db.remove(row[0])
        self.clearAll()
        self.dispalyAll()

    def delete_oneitem_edit_area(self):
        '''This method will delete perticular product from the cart'''
        self.db.remove_oneitem_edit_area(row[0])
        self.clearAll()
        self.dispalyAll_edit_area()

    def delete_edit_area(self):
        '''This method deletes all data from cart'''
        self.db.remove_edit_area()
        self.clearAll()
        self.dispalyAll_edit_area()

    def clearAll(self):
        self.items.set("")
        self.quantity.set("")
        self.price.set("")
        self.Sheet.set("")

    def exit(self):
        if messagebox.askyesno('Exit','Do you really want to exit'):
            self.master.destroy()
            logging.info('Exited Successfully')

    '''Edit area all information'''
    def add_to_edit_area(self):
        if self.txtSheet.get() == "":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        txt_mrp_price = float(self.txtMrp_Price.get())
        self.db.insert_to_edit_area(self.txtName.get(),self.txtSheet.get(),txt_mrp_price,self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get())
        self.clearAll()
        self.dispalyAll_edit_area()

    def total(self):
        '''Total Bill'''
        global sum1,sheet_price
        sum1=0
        global quantity1,CGST,SGST,Profit_Price
        quantity1=0
        Profit_Price = 0
        for row in self.db.edit_fetch():
            sum1=sum1+float(row[8])
            print("Total amount from database sum1:",row[8])
            quantity1=quantity1+int(row[2])
            print("Total quantity from database quantity1:",quantity1)
            sheet_price = 0
            sheet_price = sheet_price+float(row[3])
            print("The per_sheet_price from database per_sheet_price:",sheet_price)
            CGST = float(row[5])*0.01
            print("cgst_tax:",CGST)
            SGST = float(row[6])*0.01
            print("sgst_tax:",SGST)
            Profit_Price = Profit_Price + float(row[9])

        global tax, tax1, totalbill1, tax2
        tax=CGST + SGST
        tax1 = sum1*tax
        self.tax2.set(tax1)
        totalbill1=sum1+tax1
        self.Total_price.set(sum1)
        self.totalbill.set(totalbill1)
        self.total_quantity.set(quantity1)

    def gbill(self):
            '''This method will Generate Bill'''
            self.welcome()
            #rupee = u"\u20B9"
            for row in self.db.edit_fetch():
                self.billing_area.insert(END, f"\n{row[1]}\t\t{row[2]}\t\t{row[3]}\t{row[8]}\t\t\n")
            self.billing_area.insert(END, f"\n========================================================\n")
            self.billing_area.insert(END, f"\nTotal\t\t{quantity1}\t\t\t{sum1}\t\t\n")
            self.billing_area.insert(END, f"\n=========================================================\n")
            self.billing_area.insert(END, f"\nTax:{round(tax,2)}% \tTotal Products Amount: Rs. {sum1}\n")
            self.billing_area.insert(END, f"\nCGST :  {CGST}% \t  SGST : {SGST}%\n")
            self.billing_area.insert(END, f"\nTotal Amount:\t\t Rs. {totalbill1}\n")
            self.billing_area.insert(END, f"\n==========================================================\n")
            self.billing_area.insert(END, f"\nCoupon Disscount :\t\t{matched_coupon}%\n")
            self.billing_area.insert(END, f"\nTotal Paybill Amount:\t\t Rs. {Final_pay}\n")
            self.billing_area.insert(END, f"\n==========================================================\n")
            self.billing_area.insert(END, f"\n\tTHANK YOU\n")
            self.billing_area.insert(END, f"\n==========================================================\n")
            logging.info('Bill generated successfully')
            print(self.billing_area.get('1.0','end-1c'))

    def user_bill(self):
        '''This method will generate user bill histroy and display it'''
        self.user_bill_history()

        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from customer_datas where "+str(self.search_by1.get())+" LIKE '%"+self.search_bill.get()+"%'")
        rows1 = cur.fetchall()
        #rupee = u"\u20B9"
        for row in rows1:
            print(row[3])
            self.billing_area.insert(END, f"\n{row[3]}\t\t{row[4]}\t\t{row[5]}\t\t\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\nTax:{(row[7])}% \t Total Products Amount: Rs. {row[6]}\n")
        self.billing_area.insert(END, f"\nCGST :  {row[11]}% \t  SGST : {row[12]}%\n")
        self.billing_area.insert(END, f"\nTotal Amount :\t\t Rs. {row[8]}\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\nCoupon Disscount :\t\t{row[14]}%\n")
        self.billing_area.insert(END, f"\nTotal Paybill Amount :\t\t Rs. {row[15]}\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\n\tTHANK YOU\n")
        self.billing_area.insert(END, f"\n======================================\n")
        logging.info('Customer bill searched successfully')

    def user_bill_history(self):
        '''Method will display searched bill history'''
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from customer_datas where "+str(self.search_by1.get())+" LIKE '%"+self.search_bill.get()+"%'")
        rows1 = cur.fetchall()
        for row in rows1:

            self.billing_area.delete(1.0,END)
            self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
            self.billing_area.insert(END,"\t  Hitech City Anjaiya Nagar\n")
            self.billing_area.insert(END,"\t    Hyderabad 500084\n")
            self.billing_area.insert(END,f"\n\nBill Number:\t\t{row[2]}")
            self.billing_area.insert(END,f"\nPhone Number:\t\t{row[1]}")
            self.billing_area.insert(END,f"\nBill_Date:{row[9]}")
            self.billing_area.insert(END,f"\n\n======================================")
            self.billing_area.insert(END,"\nProduct\t\tQTY\t\tPrice Rs.")
            self.billing_area.insert(END,f"\n======================================\n")
            self.billing_area.configure(font='arial 12 bold')

    def store_customer_data(self):
        '''Save customer data and bill data to the database'''
        # for col in self.db.fetch_admin():
        #     print(col)
        for i in self.db.edit_fetch():
            self.db.insert_to_customer_data(self.c_phone.get(),self.bill_no.get(),i[1],i[2],i[3],i[8],tax,totalbill1,date,user_name1.get(),CGST,SGST,coupon_disscount_total,matched_coupon,Final_pay,float_amount)

    def add_income(self):
        '''Stores revenue data'''
        self.db.insert_income(date, day,self.bill_no.get(), quantity1, final_pay_bill_amount, tax_amount, tax_total_amount,coupon_disscount_total, Profit_Price,Total_Profit_Price,float_amount)

    def print_bill(self):
        '''Save the bill in PC'''
        q=self.billing_area.get('1.0','end-1c')
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,'Print')
        logging.info('Printing generated bill')

    def clear_bill(self):
        self.c_phone.set('')
        self.items.set('')
        self.price.set('')
        self.tax2.set('')
        self.total_quantity.set('')
        self.totalbill.set('')
        self.Total_price.set('')
        self.coupon_total_pay.set('')
        self.coupons.set('')
        x=random.randint(1000,9999)
        self.bill_no.set(str(x))
        self.welcome()
        logging.info('Cleared bill area')

    def search(self,*args):
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            try:
                cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.search_txt.get())+"%'")
                row=cur.fetchall()
                if len(row)>0:
                    self.billing_table.delete(*self.billing_table.get_children())
                    for i in row:
                        self.billing_table.insert("",END,values=i)
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}")
                
    def conform_coupon(self,*args):
        global coupon_disscount
        coupon_disscount=0
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM coupons")
            row=cur.fetchall()
            for i in row:
            
                if i[1] == self.coupons.get():
                    coupon_disscount=coupon_disscount+int(i[2])*float(0.01)
                    global matched_coupon,coupon_disscount_total, final_pay_bill, final_pay_bill_amount,float_amount, Final_pay
                    matched_coupon = i[2]
                    coupon_disscount_total = totalbill1 * coupon_disscount
                    final_pay_bill = totalbill1 - coupon_disscount_total
                    final_pay_bill_amount = round(final_pay_bill, 2)
                    
                    '''Final pay amount with round up'''
                    # Final_pay = math.ceil(final_pay_bill_amount)
                    Final_pay = final_pay_bill_amount
                    float_amount = round((float(Final_pay)) - float(final_pay_bill_amount),2)
                    self.coupon_total_pay.set(final_pay_bill_amount)

                    global tax_amount, tax_total_amount, disscount_amount, Total_Profit_Price
                    disscount_amount = sum1 * (float(matched_coupon)*0.01)
                    tax_amount = float(sum1)*float(tax)
                    tax_total_amount =  float(totalbill1)-float(tax_amount)
                    Total_Profit_Price = float(Profit_Price) - float(coupon_disscount_total)
                    logging.info('Coupon applied successfully')
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
            logging.error('Have an error, coupon not matched')
    
    def disable_text(self):
        self.billing_area.config(state= DISABLED)

    def clear_bill_text(self):
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0','end')
        logging.info('Bill area cleared')

    def welcome_default(self):
        self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END,"\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END,"\t       Hyderabad 500084\n")
        self.billing_area.configure(font='arial 12 bold')

    def welcome(self):
        global date,month_word,day,month,year
        date = dt.datetime.now()
        month_word = date.strftime("%B")
        day = str(date.date())
        month = date.month
        year = date.year

        self.bill_no=StringVar()
        x=random.randint(1000,9999)
        self.bill_no.set(str(x))
        self.billing_area.delete(1.0,END)
        self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END,"\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END,"\t   Hyderabad 500084\n")
        self.billing_area.insert(END,f"\n\nBill Number:\t\t{self.bill_no.get()}")
        self.billing_area.insert(END,f"\nPhone Number:\t\t{self.c_phone.get()}")
        self.billing_area.insert(END,f"\nBill_Date:{date}")
        self.billing_area.insert(END,f"\nBill_Date:{day}")
        self.billing_area.insert(END,f"\n\n======================================")
        self.billing_area.insert(END,"\nProduct\t\tQTY\t\tPrice")
        self.billing_area.insert(END,f"\n======================================\n")
        self.billing_area.configure(font='arial 12 bold')

class User_Window(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("1920x1080+0+0")
        self.master.config(bg = '#2c3e50')
        
        self.items = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.search_bill = StringVar()
        self.search_by1 = StringVar()
        self.Total_price=StringVar()
        self.total_price=StringVar()
        self.user_change_pass = StringVar()

        self.c_phone=StringVar()
        self.bill_no=StringVar()

        self.coupons=StringVar()
        self.coupon_total_pay = StringVar()
    
        self.tax2=StringVar()
        self.totalbill=StringVar()
        self.total_quantity=StringVar()
        self.Sheet=StringVar()
        self.tablet_details=StringVar()

        self.user_name = StringVar()
        self.password = StringVar()

        self.SGST_Amount = StringVar()          
        self.CGST_Amount = StringVar()
        self.amount_purchased = StringVar()
        self.pay_amount = StringVar()

        self.entries_frame_main = Frame(self.master,bg="black")
        self.entries_frame_main.place(x=0, y=0, width=1920, height=1080)

        self.entries_frame = Frame(self.master,bg="sky blue")
        self.entries_frame.place(x=0, y=0, width=975, height=225)

        '''login display'''
        self.entries_frame1 = Frame(self.master,bg="sky blue")
        self.entries_frame1.place(x=986, y=0, width=557, height=135)
        # '''Empty'''
        # self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        # self.lblAdmin.grid(row=0, column=0,padx=1, sticky="w")
        print("aaaaaaaaaaaaaaaaaaaaaaaaaa:",a)
        self.lblAdmin = Label(self.entries_frame1, text = "Welcome",font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        self.lblAdmin.grid(row=0, column=0,padx=1, sticky="w")

        self.lblAdmin = Label(self.entries_frame1, textvariable=user_name_display, font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        self.lblAdmin.grid(row=0, column=1,padx=1, sticky="w")
        
        '''Empty'''
        self.lblAdmin = Label(self.entries_frame1, text = "",font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        self.lblAdmin.grid(row=1, column=0,padx=1, sticky="w")
        
        self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        text="Logout",text_font=('Helvetica', 12),command=self.exit).grid(row=2, column=1,padx=10)

        self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        text="Clockin",text_font=('Helvetica', 12),command=lambda:[self.track_location(),self.clockin()]).grid(row=2, column=2,padx=10)

        self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        text="ClockOut",text_font=('Helvetica', 12),command=lambda:[self.clockOut()]).grid(row=2, column=3,padx=10)

        # self.lblAdmin = Label(self.entries_frame1, textvariable=clockin_timing, font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        # self.lblAdmin.grid(row=3, column=0,padx=1, sticky="w")

        # self.lblAdmin = Label(self.entries_frame1, textvariable=clockout_timing, font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        # self.lblAdmin.grid(row=3, column=1,padx=1, sticky="w")
        
        # self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "red",text_color = "White",corner_radius=8,
        # text="Clockinaaa",text_font=('Helvetica', 12),command=lambda:[self.clockin1()]).grid(row=3, column=3,padx=10)

        self.button = customtkinter.CTkButton(self.entries_frame1,width=12,height=30,border_width=0,fg_color = "green",text_color = "White",corner_radius=8,
        text="Edit profile",text_font=('Helvetica', 12),command=self.edit_user_data).grid(row=2, column=0,padx=10)
        
        self.title = Label(self.entries_frame, text="BILLING SYSTEM", font=("times new roman", 14, "bold"), bg="sky blue", fg="black")
        self.title.grid(row=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.lblName = Label(self.entries_frame, text="Product_Name", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblName.grid(row=1, column=0,pady = 5, sticky="w")
        self.txtName = Entry(self.entries_frame, textvariable=self.items, font=("times new roman", 12,'bold'),bd=7,bg = "sky blue",relief=SUNKEN, width=15)
        self.txtName.grid(row=1, column=1,pady = 5, sticky="w")

        self.lblMrp_Price = Label(self.entries_frame, text="Product_MRP_Price", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblMrp_Price.grid(row=2, column=0,pady = 5, sticky="w")
        self.txtMrp_Price = Entry(self.entries_frame, textvariable=self.price, font=("times new roman", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtMrp_Price.grid(row=2, column=1,pady = 5, sticky="w")

        self.lblQuantity = Label(self.entries_frame, text="Product_Quantity", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblQuantity.grid(row=3, column=0,pady = 5, sticky="w")
        self.txtQuantity = Entry(self.entries_frame, textvariable=self.quantity, font=("times new roman", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtQuantity.grid(row=3, column=1,pady = 5, sticky="w")
 
        self.lblamount_purchased = Label(self.entries_frame, text="Purchased_disscount%", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblamount_purchased.grid(row=1, column=2,pady = 5, sticky="w")
        self.txtamount_purchased = Entry(self.entries_frame, textvariable=self.amount_purchased, font=("times new roman", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtamount_purchased.grid(row=1, column=3,pady = 5, sticky="w")

        self.lblCGST = Label(self.entries_frame, text="CGST%", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblCGST.grid(row=2, column=2,pady = 5, sticky="w")
        self.txtCGST = Entry(self.entries_frame, textvariable=self.CGST_Amount, font=("times new roman", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtCGST.grid(row=2, column=3,pady = 5, sticky="w")

        self.lblSGST = Label(self.entries_frame, text="SGST%", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblSGST.grid(row=3, column=2,pady = 5, sticky="w")
        self.txtSGST = Entry(self.entries_frame, textvariable=self.SGST_Amount, font=("times new roman", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtSGST.grid(row=3, column=3,pady = 5, sticky="w")
        '''Sheet'''

        self.lblSheet = Label(self.entries_frame, text="Strip/Sheet", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblSheet.grid(row=4, column=2,padx=1, sticky="w")

        self.txtSheet = Entry(self.entries_frame, textvariable=self.Sheet, font=("times new roman", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtSheet.grid(row=4, column=3, sticky="w")

       
        self.lblTablet_details = Label(self.entries_frame, text="Tablet_details", font=("times new roman", 12,'bold'), bg="sky blue", fg="black")
        self.lblTablet_details.grid(row=4, column=0, sticky="w")
        self.txtTablet_deatails = Entry(self.entries_frame, textvariable=self.tablet_details, font=("Calibri", 12,'bold'),bd=7,relief=SUNKEN, width=15)
        self.txtTablet_deatails.grid(row=4, column=1, sticky="w")

        '''Table Frame (displaying data from data base)'''
        tree_frame = Frame(self.master,bg="sky blue")
        tree_frame.place(x=0, y=235, width=535, height=370)
        
        lbl_search=Label(tree_frame,text="Search Products",bg="green",fg="white",font=("times new roman",14,"bold"))
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        txt_Search= Entry(tree_frame,textvariable=self.search_txt,width=20,font=("times new roman",10,"bold") ,bd=5,relief=GROOVE)
        txt_Search.grid(row=0, column=2, padx=20, pady=10, sticky="w")
        txt_Search.bind("<Key>",self.search)

        '''Table Show Data'''
        Table_Frame=Frame(tree_frame,relief=RIDGE,bg="crimson")
        Table_Frame.place(x=10,y=70,width=515,height=300)
        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        
        self.billing_table=ttk.Treeview(Table_Frame,columns=("ProductID","Products","Quantity","MRP_Price","product_details","CGST","SGST","Purchase_price"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)

        self.billing_table.heading("ProductID",text="ProductID")
        self.billing_table.heading("Products",text="Products")
        self.billing_table.heading("Quantity",text="quantity")
        self.billing_table.heading("MRP_Price",text="MRP_Price")
        self.billing_table.heading("product_details",text="product_details")
        self.billing_table.heading("CGST",text="CGST")
        self.billing_table.heading("SGST",text="SGST")
        self.billing_table.heading("Purchase_price",text="Purchase_price")
        self.billing_table['show']='headings'
        self.billing_table.column("ProductID",width=2)
        self.billing_table.column("Products",width=100)
        self.billing_table.column("Quantity",width=10)
        self.billing_table.column("MRP_Price",width=20)
        self.billing_table.column("product_details",width=20)
        self.billing_table.column("CGST",width=10)
        self.billing_table.column("SGST",width=20)
        self.billing_table.column("Purchase_price",width=20)
        self.billing_table.pack(fill=BOTH,expand=1)
        self.billing_table.bind("<ButtonRelease-1>",self.getData)

        '''displaying bill area and dimenions'''
        '''Customer Details'''
        F1=LabelFrame(self.master, bd=10,relief=GROOVE, text="Customer Details",font=("times new roman", 10,"bold"),fg="black", bg="sky blue")
        F1.place(x=980,y=136, width=550)

        self.cphn_lbl=Label(F1,text="Phone No.",bg="sky blue",fg="black", font=("times new roman",15,"bold")).grid(row=0,column=2,padx=20,pady=5)
        self.txtPhone=Entry(F1,width=15,font="arial 15",bd=7,relief=SUNKEN,textvariable=self.c_phone).grid(row=0, column=3,pady=5,padx=10)

        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.master,bg="sky blue",bd=10,relief=GROOVE)
        self.billing_area.place(x=980, y=214, width=550, height=470)
        self.billing_tiltle=Label(self.billing_area,text="Bill Area",font="arial 15 bold",fg="black",bg="sky blue",bd=7,relief=GROOVE).pack(fill=X)

        scroll_y=Scrollbar(self.billing_area,orient=VERTICAL)
        self.billing_area=Text(self.billing_area,yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH,expand=1)
        self.welcome_default1()

        '''Bill Menu'''
        self.button_frame=LabelFrame(self.master,bg="sky blue",bd=10,relief=GROOVE)
        self.button_frame.place(x=980,y=685,width=550,height=100)

        '''Total Calculate Menue'''
        self.button_Total_frame=LabelFrame(self.master,bg="sky blue",bd=10,relief=GROOVE)
        self.button_Total_frame.place(x=0,y=630,width=975,height=157)

        self.cphn_lbl1=Label(self.button_Total_frame,text="Total",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=0,column=2,padx=20.0,pady=5)
        self.cphn_ibl1=Entry(self.button_Total_frame,textvariable=self.Total_price,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=0, column=3,pady=5,padx=10)

        self.cphn_lbl2=Label(self.button_Total_frame,text="Tax",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=1,column=2,padx=20,pady=5)
        self.cphn_ibl2=Entry(self.button_Total_frame,textvariable=self.tax2,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=1, column=3,pady=5,padx=10)

        self.cphn_lbl3=Label(self.button_Total_frame,text="Total Quantity",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=0,column=4,padx=20,pady=5)
        self.cphn_ibl3=Entry(self.button_Total_frame,textvariable=self.total_quantity,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=0, column=5,pady=5,padx=10)

        self.cphn_lbl3=Label(self.button_Total_frame,text="Total Amount",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=1,column=4,padx=20,pady=5)
        self.cphn_ibl3=Entry(self.button_Total_frame,textvariable=self.totalbill,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=1, column=5,pady=5,padx=10)

        self.lblcphn_Coupon=Label(self.button_Total_frame,text="Disscount%",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=0,column=6,padx=5,pady=5)
        self.txtcphn_coupon=Entry(self.button_Total_frame,textvariable=self.coupons,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=0, column=7,pady=5,padx=5)

        self.cphn_Coupon_Total=Label(self.button_Total_frame,text="Amount",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=1,column=6,padx=5,pady=5)
        self.cphn_coupon_total=Entry(self.button_Total_frame,textvariable=self.coupon_total_pay,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=1, column=7,pady=5,padx=5)
#========================================================
        self.cphn_pay_amount=Label(self.button_Total_frame,text="Paid Amount",bg="sky blue",fg="black", font=("times new roman",12,"bold")).grid(row=3,column=6,padx=5,pady=5)
        self.cphn_pay_amount=Entry(self.button_Total_frame,textvariable=self.pay_amount,width=15,font="arial 12",bd=7,relief=SUNKEN).grid(row=3, column=7,pady=5,padx=5)
#===================================================================
        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="Total",text_font=('Helvetica', 14),command=self.total).grid(row=0, column=0,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="Bill",text_font=('Helvetica', 14),command=lambda:[self.gbill(),self.add_income(),self.store_customer_data(),self.disable_text(),self.delete_edit_area()]).grid(row=0, column=1,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="Print",text_font=('Helvetica', 14),command=self.print_bill).grid(row=0, column=2,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="Clear",text_font=('Helvetica', 14),command=lambda:[self.clear_bill(),self.clear_bill_text()]).grid(row=0, column=3,padx=5,pady=5)

        self.button = customtkinter.CTkButton(self.button_frame,width=14,height=40,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="ApplyCoupon",text_font=('Helvetica', 14),command=lambda:[self.conform_coupon()]).grid(row=0, column=4,padx=5,pady=5)

        '''displaying data of edit area'''
        '''displaying edit area'''
        self.billing_edit = Frame(self.master,bg="sky blue")
        self.billing_edit.place(x=538, y=235, width=440, height=370)

        button = customtkinter.CTkButton(self.billing_edit,width=8,height=20,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="Add Cart",text_font=('Helvetica', 8),command=lambda:[self.update_items_quantity(),self.add_to_edit_area()]).grid(row=1, column=0,padx=2)

        # button = customtkinter.CTkButton(self.billing_edit,width=8,height=20,border_width=0,corner_radius=8,
        # text="Update Cart",text_font=('Helvetica', 8),command=self.update_edit_area).grid(row=1, column=1,padx=2)

        button = customtkinter.CTkButton(self.billing_edit,width=8,height=20,border_width=0,corner_radius=8,fg_color = "green",text_color = "White",
        text="Delete Cart",text_font=('Helvetica', 8),command=lambda:[self.update_items_quantity_after_delete_cart(),self.delete_oneitem_edit_area()]).grid(row=1, column=2,padx=2)

        self.lbl_edit=Label(self.billing_edit,text="Cart",bg="sky blue",fg="black",font=("times new roman",14,"bold"))
        self.lbl_edit.grid(row=0,column=0,pady=10,padx=20,sticky="w")
        
        self.combo_search=ttk.Combobox(self.billing_edit,textvariable=self.search_by1,width=7,font=("times new roman",11,"bold"),state='readonly')
        self.combo_search['values']=("bill_no")
        self.combo_search.grid(row=0,column=1,padx=5,pady=5)
        self.search_btn = Button(self.billing_edit,text="Search Customer Bill",bg="green", fg='white', width=17,pady=5,command=lambda:[self.user_bill(),self.disable_text()]).grid(row=0, column=3,padx=5,pady=5)
        self.txtBillSearch=Entry(self.billing_edit,width=9,font="arial 11",bd=7,relief=SUNKEN,textvariable=self.search_bill).grid(row=0, column=2,pady=5,padx=10)
        
        self.edit_Table_Frame=Frame(self.billing_edit,relief=RIDGE,bg="white")
        self.edit_Table_Frame.place(x=10,y=79,width=421,height=290)

        scroll_x=Scrollbar(self.edit_Table_Frame,orient=HORIZONTAL)

        self.edit_billing_table=ttk.Treeview(self.edit_Table_Frame,columns=("ProductID","Products","Quantity","MRP_Price","product_details","CGST","SGST","Purchase_price","total_price"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
       
        scroll_x.config(command=self.edit_billing_table.xview)

        self.edit_billing_table.heading("ProductID",text="ProductID")
        self.edit_billing_table.heading("Products",text="Products")
        self.edit_billing_table.heading("Quantity",text="quantity")
        self.edit_billing_table.heading("MRP_Price",text="MRP_Price")
        self.edit_billing_table.heading("product_details",text="product_details")
        self.edit_billing_table.heading("CGST",text="CGST")
        self.edit_billing_table.heading("SGST",text="SGST")
        self.edit_billing_table.heading("Purchase_price",text="Purchase_price")
        self.edit_billing_table.heading("total_price",text="total_price")
        self.edit_billing_table['show']='headings'
        self.edit_billing_table.column("ProductID",width=2)
        self.edit_billing_table.column("Products",width=100)
        self.edit_billing_table.column("Quantity",width=10)
        self.edit_billing_table.column("MRP_Price",width=20)
        self.edit_billing_table.column("product_details",width=20)
        self.edit_billing_table.column("CGST",width=10)
        self.edit_billing_table.column("SGST",width=20)
        self.edit_billing_table.column("Purchase_price",width=20)
        self.edit_billing_table.column("total_price",width=20)
        
        self.edit_billing_table.pack(fill=BOTH,expand=1)
        self.edit_billing_table.bind("<ButtonRelease-1>",self.edit_area_getData)
        self.dispalyAll_edit_area()

        self.style = ttk.Style()
        self.style.configure("Treeview",background='#7FFFD4', foreground='black', font=('Calibri', 12),rowheight=20)
        self.style.configure("Treeview.Heading",background='blue', foreground='black',relief='flat', font=('Calibri', 12))

    def welcome_default1(self):
        self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END,"\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END,"\t       Hyderabad 500084\n")
        self.billing_area.configure(font='arial 12 bold')

    def remove_edit_area(self):
        if  self.cur.execute("delete from products"):
            self.con.commit()
            logging.info('item removed successfully from cart')
        else:
            logging.error('item not removed from cart')

    def getData(self,event):
        '''It will get data from database and display it'''
        self.clearAll()
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]
        print(row)
        global quantity_set
        quantity_set = row[2]
        self.items.set(row[1])
        self.quantity.set(row[2])
        self.price.set(row[3])
        self.tablet_details.set(row[4])   
        self.SGST_Amount.set(row[5])           
        self.CGST_Amount.set(row[6])
        self.amount_purchased.set(row[7])

    def edit_area_getData(self,event):
        self.clearAll()
        selected_row = self.edit_billing_table.focus()
        data = self.edit_billing_table.item(selected_row)
        global row
        row = data["values"]
        print(row)

        self.items.set(row[1])
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.items.get())+"%'")
        quantity_rows1 = cur.fetchall()
        for quantity_row in quantity_rows1:
            self.quantity.set(quantity_row[2])
        
        self.price.set(row[3])
        self.tablet_details.set(row[4])   
        self.SGST_Amount.set(row[5])           
        self.CGST_Amount.set(row[6])
        self.amount_purchased.set(row[7])
        self.total_price.set(row[8])
        self.Sheet.set(row[2])

    def update_items_quantity(self):
        '''This method will update quantity'''
        quantity_reduce = int(self.txtQuantity.get()) - int(self.txtSheet.get())
        self.db.update(self.txtName.get(),quantity_reduce,self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),row[0])
    
    def update_items_quantity_after_delete_cart(self):
        '''This method will update quantity'''
        quantity_add = int(self.txtQuantity.get()) + int(self.txtSheet.get())
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.items.get())+"%'")
        quantity_rows = cur.fetchall()
        for quantity_row in quantity_rows:
            self.db.update(self.txtName.get(),quantity_add,self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),quantity_row[0])
    
    def dispalyAll(self):
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.fetch():
            self.billing_table.insert("", END, values=row)

    def dispalyAll_edit_area(self):
        self.edit_billing_table.delete(*self.edit_billing_table.get_children())
        for row in self.db.edit_fetch():
            self.edit_billing_table.insert("", END, values=row)

    def search_dispalyAll(self):
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.search_data():
            self.billing_table.insert("", END, values=row)

    def update_edit_area(self):
        if self.txtSheet.get()=="":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        self.db.update_to_edit_area(self.edit_items,self.txtSheet.get(),self.edit_price,row[0])
        messagebox.showinfo("Success", "Record Update")
        logging.info('Updated products from cart')
        self.clearAll()
        self.dispalyAll_edit_area()

    def delete_oneitem_edit_area(self):
        '''This method will delete perticular product from the cart'''
        self.db.remove_oneitem_edit_area(row[0])
        self.clearAll()
        self.dispalyAll_edit_area()

    def delete_edit_area(self):
        '''This method deletes all data from cart'''
        self.db.remove_edit_area()
        self.clearAll()
        self.dispalyAll_edit_area()

    def clearAll(self):
        self.items.set("")
        self.quantity.set("")
        self.price.set("")

    def exit(self):
        if messagebox.askyesno('Exit','Do you really want to exit'):
            self.master.destroy()
            logging.info('Exited Successfully')

    def add_to_edit_area(self):
        if self.txtSheet.get() == "":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        txt_mrp_price = float(self.txtMrp_Price.get())
        self.db.insert_to_edit_area(self.txtName.get(),self.txtSheet.get(),txt_mrp_price,self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get())
        self.clearAll()
        self.dispalyAll_edit_area()

    def total(self):
        '''This method will calculate Total Bill'''
        global sum1,sheet_price
        sum1=0
        global quantity1,CGST,SGST,Profit_Price
        quantity1=0
        Profit_Price = 0
        for row in self.db.edit_fetch():
            sum1=sum1+float(row[8])
            quantity1=quantity1+int(row[2])
            sheet_price = 0
            sheet_price = sheet_price+float(row[3])
            CGST = float(row[5])*0.01
            SGST = float(row[6])*0.01
            Profit_Price = Profit_Price + float(row[9])

        global tax, tax1, totalbill1
        tax=CGST + SGST
        tax1 = sum1*tax
        self.tax2.set(tax1)
        totalbill1=sum1+tax1
        self.Total_price.set(sum1)
        self.totalbill.set(totalbill1)
        self.total_quantity.set(quantity1)

    def gbill(self):
            '''This method will Generate Bill'''
            self.welcome()
            #rupee = u"\u20B9"
            for row in self.db.edit_fetch():
                self.billing_area.insert(END, f"\n{row[1]}\t\t{row[2]}\t\t{row[3]}\t{row[8]}\t\t\n")
            self.billing_area.insert(END, f"\n========================================================\n")
            #==================================Experiment==============================================
            # self.billing_area.insert(END, f"\nTotal\t\t{quantity1}\t\t{sheet_price}\t{sum1}\t\t\n")
            self.billing_area.insert(END, f"\nTotal\t\t{quantity1}\t\t\t{sum1}\t\t\n")
            self.billing_area.insert(END, f"\n=========================================================\n")
            #==========================================================================================
            self.billing_area.insert(END, f"\nTax:{round(tax,2)}% \tTotal Products Amount: Rs. {sum1}\n")
            self.billing_area.insert(END, f"\nCGST :  {CGST}% \t  SGST : {SGST}%\n")
            self.billing_area.insert(END, f"\nTotal Amount:\t\t Rs. {totalbill1}\n")
            self.billing_area.insert(END, f"\n==========================================================\n")
            self.billing_area.insert(END, f"\nCoupon Disscount :\t\t{matched_coupon}%\n")
            # self.billing_area.insert(END, f"\nCoupon Disscount :\t\t{coupon_disscount}%\n")
            self.billing_area.insert(END, f"\nTotal Paybill Amount:\t\t Rs. {Final_pay}\n")
            self.billing_area.insert(END, f"\n==========================================================\n")
            self.billing_area.insert(END, f"\n\tTHANK YOU\n")
            self.billing_area.insert(END, f"\n==========================================================\n")
            logging.info('Bill generated successfully')

            print(self.billing_area.get('1.0','end-1c'))

    def user_bill(self):
        '''This method will generate user bill histroy and display it'''
        self.user_bill_history()

        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from customer_datas where "+str(self.search_by1.get())+" LIKE '%"+self.search_bill.get()+"%'")
        rows1 = cur.fetchall()
        #rupee = u"\u20B9"
        for row in rows1:
            print(row[3])
            self.billing_area.insert(END, f"\n{row[3]}\t\t{row[4]}\t\t{row[5]}\t\t\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\nTax:{(row[7])}% \t Total Products Amount: Rs. {row[6]}\n")
        self.billing_area.insert(END, f"\nCGST :  {row[11]}% \t  SGST : {row[12]}%\n")
        self.billing_area.insert(END, f"\nTotal Amount :\t\t Rs. {row[8]}\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\nCoupon Disscount :\t\t{row[14]}%\n")
        self.billing_area.insert(END, f"\nTotal Paybill Amount :\t\t Rs. {row[15]}\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\n\tTHANK YOU\n")
        self.billing_area.insert(END, f"\n======================================\n")
        logging.info('Customer bill searched successfully')

    def user_bill_history(self):
        '''Method will display searched bill history'''
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from customer_datas where "+str(self.search_by1.get())+" LIKE '%"+self.search_bill.get()+"%'")
        rows1 = cur.fetchall()
        for row in rows1:

            self.billing_area.delete(1.0,END)
            self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
            self.billing_area.insert(END,"\t  Hitech City Anjaiya Nagar\n")
            self.billing_area.insert(END,"\t    Hyderabad 500084\n")
            self.billing_area.insert(END,f"\n\nBill Number:\t\t{row[2]}")
            self.billing_area.insert(END,f"\nPhone Number:\t\t{row[1]}")
            self.billing_area.insert(END,f"\nBill_Date:{row[9]}")
            self.billing_area.insert(END,f"\n\n======================================")
            self.billing_area.insert(END,"\nProduct\t\tQTY\t\tPrice Rs.")
            self.billing_area.insert(END,f"\n======================================\n")
            self.billing_area.configure(font='arial 12 bold')

    def store_customer_data(self):
        '''Save customer data and bill data to the database'''
        # for col in self.db.fetch_admin():
        #     print(col)
        for i in self.db.edit_fetch():
            #self.db.insert_to_customer_data(self.c_phone.get(),self.bill_no.get(),i[1],i[2],i[3],i[8],tax,totalbill1,date,user_name1.get(),CGST,SGST,coupon_disscount_total,matched_coupon,Final_pay,float_amount,self.pay_amount.get())
            self.db.insert_to_customer_data(self.c_phone.get(),self.bill_no.get(),i[1],i[2],i[3],i[8],tax,totalbill1,date,user_name1.get(),CGST,SGST,coupon_disscount_total,matched_coupon,Final_pay,self.pay_amount.get())

    def add_income(self):
        '''Stores revenue data'''
        convert_str = float(self.pay_amount.get())
        pay_amou = self.pay_amount.get()
        bill_amount = round((float(final_pay_bill_amount) - convert_str),2)
        if (pay_amou.isdigit()):
            # self.db.insert_income(date, day,self.bill_no.get(), quantity1, final_pay_bill_amount, tax_amount, tax_total_amount,coupon_disscount_total, Profit_Price,Total_Profit_Price,self.pay_amount.get(),bill_amount)
            self.db.insert_income(date, day,self.bill_no.get(), quantity1, final_pay_bill_amount, tax_amount, tax_total_amount,coupon_disscount_total, Profit_Price,Total_Profit_Price,convert_str,bill_amount)

    def print_bill(self):
        '''Save the bill in PC'''
        q=self.billing_area.get('1.0','end-1c')
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,'Print')
        logging.info('Printing generated bill')

    def clear_bill(self):
        self.c_phone.set('')
        self.items.set('')
        self.price.set('')
        self.tax2.set('')
        self.total_quantity.set('')
        self.totalbill.set('')
        self.Total_price.set('')
        self.coupon_total_pay.set('')
        self.coupons.set('')
        x=random.randint(1000,9999)
        self.bill_no.set(str(x))
        self.welcome()
        logging.info('Cleared bill area')

    def search(self,*args):
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            try:
                cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.search_txt.get())+"%'")
                row=cur.fetchall()
                if len(row)>0:
                    self.billing_table.delete(*self.billing_table.get_children())
                    for i in row:
                        self.billing_table.insert("",END,values=i)
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}")

    def conform_coupon(self,*args):
        '''Coupon Search'''
        global coupon_disscount
        coupon_disscount=0
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM coupons")
            row=cur.fetchall()
            for i in row:
            
                if i[1] == self.coupons.get():
                    coupon_disscount=coupon_disscount+int(i[2])*float(0.01)
                    global matched_coupon, coupon_disscount_total, final_pay_bill, final_pay_bill_amount,float_amount, Final_pay
                    matched_coupon = i[2]
                    coupon_disscount_total = totalbill1 * coupon_disscount
                    final_pay_bill = totalbill1 - coupon_disscount_total
                    final_pay_bill_amount = round(final_pay_bill, 2)
                    
                    '''Final pay amount with round up'''
                    # Final_pay = math.ceil(final_pay_bill_amount)
                    Final_pay = final_pay_bill_amount
                    float_amount = round((float(Final_pay)) - float(final_pay_bill_amount),2)
                    
                    self.coupon_total_pay.set(final_pay_bill_amount)
                    global tax_amount, tax_total_amount, disscount_amount, Total_Profit_Price
                    disscount_amount = sum1 * (float(matched_coupon)*0.01)

                    tax_amount = float(sum1)*float(tax)
                    tax_total_amount =  float(totalbill1)-float(tax_amount)
                    Total_Profit_Price = float(Profit_Price) - float(coupon_disscount_total)
                    logging.info('Coupon applied successfully')

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
            logging.error('Have an error, coupon not matched')

    def disable_text(self):
        self.billing_area.config(state= DISABLED)

    def clear_bill_text(self):
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0','end')

    def welcome_default(self):
        self.billing_area.insert(END,"\tWelcome Apollo Medical")
        self.billing_area.insert(END,"\t  Hitech City Anjaiya Nagar")
        self.billing_area.insert(END,"\t    Hyderabad 500084")

    def welcome(self):
        global date,month_word,day,month,year
        date = dt.datetime.now()
        month_word = date.strftime("%B")
        day = str(date.date())
        month = date.month
        year = date.year
        
        self.bill_no=StringVar()
        x=random.randint(1000,9999)
        self.bill_no.set(str(x))
        self.billing_area.delete(1.0,END)
        self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END,"\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END,"\t   Hyderabad 500084\n")
        #self.billing_area.insert(END,"\t  Welcome Apollo Medical")
        self.billing_area.insert(END,f"\n\nBill Number:\t\t{self.bill_no.get()}")
        self.billing_area.insert(END,f"\nPhone Number:\t\t{self.c_phone.get()}")
        self.billing_area.insert(END,f"\nBill_Date:{date}")
        self.billing_area.insert(END,f"\n\n======================================")
        self.billing_area.insert(END,"\nProduct\t\tQTY\t\tPrice\tTotal Price")
        self.billing_area.insert(END,f"\n======================================\n")
        self.billing_area.configure(font='arial 12 bold')


    def track_location(self):
        try:
            g = geocoder.ip('me')
            #print(g.state)
            logging.info(f'Success, {a} User location tracked:{g.latlng}{g.state},{g.city},{g.postal}')
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
            logging.error('Have an error, Location not detected')
        # try:
        #     g = geocoder.ip('me')
        #     loca = g.latlng
        #     lat = loca[0]
        #     lang = loca[1]
        #     #print(g.postal)
        #     geoLoc = Nominatim(user_agent="GetLoc")
        #     locname = geoLoc.reverse(f"{lat}, {lang}")
        #     print(locname.address)
        #     # logging.info(f'Success, User location tracked:{locname.address}')
        #     logging.info(f'Success, User location tracked:{g.latlng}')
        # except Exception as ex:
        #     messagebox.showerror("Error",f"Error due to {str(ex)}")
        #     logging.error('Have an error, Location not detected')

    def clockin(self):
        try:
            global clockin_timing
            date = dt.datetime.now()
            day_clockin = str(date.date())
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            cur.execute("SELECT salary from users where username LIKE '%"+str(a)+"%'")
            row=cur.fetchall()

            for sal_row in row:
                date = dt.datetime.now()
                clockin_timing = str(date.time())
                day_clockin = str(date.date())
                month_clockin = date.month
                year_clockin = date.year
                number_of_months = calendar.monthrange(year_clockin,month_clockin)[1]
                daily_sal = float(sal_row[0])/number_of_months

            cur.execute("SELECT username,clockin_date from users_sal")
            row_user_name=cur.fetchall()
            ab = (a,day_clockin)
            # print("abababab:",a)
            # print("user_name_display:",user_name_display)

            if ab in row_user_name:
                print("Today Already Clocked-in")
                messagebox.showinfo("Error", "Today Already Clocked-in")
            else:
                self.db.insert_User_sal(a, day_clockin, clockin_timing, daily_sal)
                messagebox.showinfo("Success", "Success Clockin")
                print("Clockin Success")
                logging.info(f'Success, Successfully clocked in')

        except Exception as ex:
            #messagebox.showerror("Error",f"Error due to {str(ex)}")
            logging.error(f'Have an error, Have an issue in clockin please check {a}')

        # self.lblAdmin = Label(self.entries_frame1, textvariable=clockin_timing, font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        # self.lblAdmin.grid(row=3, column=0,padx=1, sticky="w")
    
    
    def clockOut(self):
        try:
            global clockout_timing
            date = dt.datetime.now()
            day_clockin = str(date.date())
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            cur.execute("SELECT salary from users where username LIKE '%"+str(a)+"%'")
            row=cur.fetchall()

            for sal_row in row:
                                    
                date = dt.datetime.now()
                clockout_timing = str(date.time())
                day_clockout = str(date.date())
                month_clockout = date.month
                year_clockout = date.year
                number_of_months = calendar.monthrange(year_clockout,month_clockout)[1]
                daily_sal = float(sal_row[0])/number_of_months

            cur.execute("SELECT username,clockOut_date from users_clockOut")
            row_user_name=cur.fetchall()
            ab = (a,day_clockin)

            if ab in row_user_name:
                messagebox.showinfo("Error", "Today Already Clocked-Out")
            else:
                if messagebox.askyesno('Exit','Do you really want to exit') == 'yes':
                    self.db.insert_User_Clockout(a, day_clockout, clockout_timing, daily_sal)
                    messagebox.showinfo("Success", "Success Clock-Out")
                    print("Clockout Success")
                    logging.info(f'Success, Successfully clocked out by {a}')
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
            logging.error(f'Have an error, Have an issue in clock-out please check {a}')

        #==================================IMPPPPPPPPPPP============================================================================
        # ending_search = cur.execute('''
        # SELECT * FROM users_sal WHERE username LIKE ?
        # ''', (f'%{a.get()}',))
        # ending_search_results = ending_search.fetchall()

        # for row in ending_search_results:
        #     print(row)


        # ending_search = cur.execute('''
        # SELECT * FROM users_sal WHERE username LIKE ?''', (f'%{a.get()}',)) and '''clockin_date LIKE ?''', (f'%{a.get()}',)
        # ending_search_results = ending_search.fetchall()

        # for row in ending_search_results:
        #     print(row)

        #==========================IMPPPPPPPPPPPPPPPPPPPPPPPP=========================================
        # self.lblAdmin = Label(self.entries_frame1, textvariable=clockin_timing, font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        # self.lblAdmin.grid(row=3, column=0,padx=1, sticky="w")

        # self.lblAdmin = Label(self.entries_frame1, textvariable=clockout_timing, font=("Times new roman", 18,'bold'), bg="sky blue", fg="black")
        # self.lblAdmin.grid(row=3, column=1,padx=1, sticky="w")


class Window_user_register(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,register_window):
        self.register_window = register_window
        self.register_window.title("Register User")
        #self.register_window.geometry("1200x750")1920x1080
        self.register_window.geometry("1920x1080")
        self.register_window.config(bg = 'blue')
        self.username = StringVar()
        self.password = StringVar()
        self.email = StringVar()
        self.phone_no = StringVar()
        self.address = StringVar()
        self.active = StringVar()
        self.usersal = StringVar()
        self.is_admin = StringVar()
        self.is_user = StringVar()
        self.user_conform_password = StringVar()

        self.basic = StringVar()
        self.hra = StringVar()
        self.conveyance_allowance = StringVar()
        self.medical_allowance = StringVar()
        self.performance_bonus =StringVar()
        self.pf = StringVar()
        self.esi = StringVar()
        self.tax = StringVar()
        global t_sal
        t_sal = 0

        img = Image.open('images/medical.webp')
        logo = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.register_window,image=logo)
        logo_label.image = logo
        logo_label.place(width=1920, height=1080)

        self.user_frame = Frame(self.register_window,bg="light green")
        self.user_frame.place(x=40, y=50, width=800, height=650)
       
        self.lbluserName = Label(self.user_frame, text="User Name", font=("Calibri", 14), bg="light green", fg="black") #bg="#535c68"
        self.lbluserName.grid(row=0, column=0,padx=10,pady=10)
        self.txtuserName = Entry(self.user_frame, textvariable=self.username, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        self.txtuserName.grid(row=0, column=1,padx=10,pady=10, sticky="w")
        #self.txtName.config(state=DISABLED)

        self.lblPassword = Label(self.user_frame, text="Password", font=("Calibri", 14), bg="light green", fg="black")
        self.lblPassword.grid(row=1, column=0,padx=10,pady=10, sticky="w")
        self.txtpassword = Entry(self.user_frame, textvariable=self.password, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        self.txtpassword.grid(row=1, column=1,padx=10,pady=10, sticky="w")
        self.txtpassword.config(state=DISABLED)
        
        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,fg_color='yellow',corner_radius=8,
        text="Generate Password",text_font=('Helvetica', 10),command=lambda:[self.enable(),self.new_rand(),self.disable()]).grid(row=7, column=1,padx=50,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,fg_color='yellow',corner_radius=8,
        text="Copy password",text_font=('Helvetica', 10),command=lambda:[self.clipper_admin()]).grid(row=7, column=0,padx=5,pady=10, sticky="w")


        self.lblEmail = Label(self.user_frame, text="Email Id", font=("Calibri", 14), bg="light green", fg="black")
        self.lblEmail.grid(row=2, column=0,padx=10,pady=10, sticky="w")
        self.txtEmail = Entry(self.user_frame, textvariable=self.email, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        self.txtEmail.grid(row=2, column=1,padx=10,pady=10, sticky="w")

        self.lblPhone_no = Label(self.user_frame, text="Phone No", font=("Calibri", 14), bg="light green", fg="black")
        self.lblPhone_no.grid(row=3, column=0,padx=10,pady=10, sticky="w")
        self.txtPhone_no = Entry(self.user_frame, textvariable=self.phone_no, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        self.txtPhone_no.grid(row=3, column=1,padx=10,pady=10, sticky="w")

        self.lblAdress = Label(self.user_frame, text="Adress", font=("Calibri", 14), bg="light green", fg="black")
        self.lblAdress.grid(row=4, column=0,padx=10,pady=10, sticky="w")
        self.txtAdress = Entry(self.user_frame, textvariable=self.address, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        self.txtAdress.grid(row=4, column=1,padx=10,pady=10, sticky="w")

        self.lbl_edit=Label(self.user_frame,text="Is Active",bg="light green",fg="black",font=("times new roman",14,"bold"))
        self.lbl_edit.grid(row=6,column=0,pady=10,padx=10,sticky="w")

        self.user_search=ttk.Combobox(self.user_frame,textvariable=self.active,width=7,font=("times new roman",11,"bold"),state='readonly')
        self.user_search['values']=("Yes","No")
        self.user_search.grid(row=6, column=1,padx=10,pady=10, sticky="w")
        #=================================================================================
        self.lbl_edit=Label(self.user_frame,text="Is Admin",bg="light green",fg="black",font=("times new roman",14,"bold"))
        self.lbl_edit.grid(row=0,column=2,pady=10,padx=10,sticky="w")

        self.user_search=ttk.Combobox(self.user_frame,textvariable=self.is_admin,width=7,font=("times new roman",11,"bold"),state='readonly')
        self.user_search['values']=("Yes","No")
        self.user_search.grid(row=0, column=3,padx=10,pady=10, sticky="w")

        self.lbl_edit=Label(self.user_frame,text="Is User",bg="light green",fg="black",font=("times new roman",14,"bold"))
        self.lbl_edit.grid(row=1,column=2,pady=10,padx=10,sticky="w")

        self.user_search=ttk.Combobox(self.user_frame,textvariable=self.is_user,width=7,font=("times new roman",11,"bold"),state='readonly')
        self.user_search['values']=("Yes","No")
        self.user_search.grid(row=1, column=3,padx=10,pady=10, sticky="w")
        #========================================================================

        self.lbluserSal = Label(self.user_frame, text="User Sal", font=("Calibri", 14), bg="light green", fg="black") #bg="#535c68"
        self.lbluserSal.grid(row=5, column=0,padx=10,pady=10, sticky="w")
        self.txtuserSal = Entry(self.user_frame, textvariable=self.usersal, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        #self.usersal.trace('w', self.fetch_doc_pateint_number_details())
        self.txtuserSal.grid(row=5, column=1,padx=10,pady=10, sticky="w")
        #t_sal = t_sal + float(self.txtuserSal.get())
#==================================================================Salary=======================================
#         self.lblBasic = Label(self.user_frame, text="Basic", font=("Calibri", 14), bg="light green", fg="black") #bg="#535c68"
#         self.lblBasic.grid(row=0, column=2,padx=10,pady=10, sticky="w")
#         self.txtBasic = Entry(self.user_frame, textvariable=self.basic, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtBasic.grid(row=0, column=3,padx=10,pady=10, sticky="w")
#         #self.txtName.config(state=DISABLED)
# # self.txtBasic.get(),self.txtHRA.get(),self.txtCon_alow.get(),self.txtMed_alow.get(),self.txtBonus.get(),self.txtPF.get(),self.txtESI.get(),self.txtTax.get()
#         self.lblHRA = Label(self.user_frame, text="HRA", font=("Calibri", 14), bg="light green", fg="black")
#         self.lblHRA.grid(row=1, column=2,padx=10,pady=10, sticky="w")
#         self.txtHRA = Entry(self.user_frame, textvariable=self.hra, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtHRA.grid(row=1, column=3,padx=10,pady=10, sticky="w")
#         #self.txtHRA.config(state=DISABLED)

#         self.lblCon_alow = Label(self.user_frame, text="Conveyance Allowance", font=("Calibri", 14), bg="light green", fg="black")
#         self.lblCon_alow.grid(row=2, column=2,padx=10,pady=10, sticky="w")
#         self.txtCon_alow = Entry(self.user_frame, textvariable=self.conveyance_allowance, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtCon_alow.grid(row=2, column=3,padx=10,pady=10, sticky="w")

#         self.lblMed_alow = Label(self.user_frame, text="Medical Allowance", font=("Calibri", 14), bg="light green", fg="black")
#         self.lblMed_alow.grid(row=3, column=2,padx=10,pady=10, sticky="w")
#         self.txtMed_alow = Entry(self.user_frame, textvariable=self.medical_allowance, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtMed_alow.grid(row=3, column=3,padx=10,pady=10, sticky="w")

#         self.lblBonus = Label(self.user_frame, text="Performance Bonus", font=("Calibri", 14), bg="light green", fg="black")
#         self.lblBonus.grid(row=4, column=2,padx=10,pady=10, sticky="w")
#         self.txtBonus = Entry(self.user_frame, textvariable=self.performance_bonus, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtBonus.grid(row=4, column=3,padx=10,pady=10, sticky="w")

#         self.lblPF = Label(self.user_frame, text="PF", font=("Calibri", 14), bg="light green", fg="black") #bg="#535c68"
#         self.lblPF.grid(row=5, column=2,padx=10,pady=10, sticky="w")
#         self.txtPF = Entry(self.user_frame, textvariable=self.pf, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtPF.grid(row=5, column=3,padx=10,pady=10, sticky="w")

#         self.lblESI = Label(self.user_frame, text="ESI", font=("Calibri", 14), bg="light green", fg="black")
#         self.lblESI.grid(row=6, column=2,padx=10,pady=10, sticky="w")
#         self.txtESI = Entry(self.user_frame, textvariable=self.esi, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtESI.grid(row=6, column=3,padx=10,pady=10, sticky="w")

#         self.lblTax = Label(self.user_frame, text="Tax", font=("Calibri", 14), bg="light green", fg="black")
#         self.lblTax.grid(row=7, column=2,padx=10,pady=10, sticky="w")
#         self.txtTax = Entry(self.user_frame, textvariable=self.tax, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
#         self.txtTax.grid(row=7, column=3,padx=10,pady=10, sticky="w")

#         self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
#         text="Submit",text_font=('Helvetica', 12),command=lambda:[self.add_to_User_register()]).grid(row=8, pady = 10, column=1)

        # self.lbluserSal = Label(self.user_frame, text="User Sal", font=("Calibri", 14), bg="light green", fg="black") #bg="#535c68"
        # self.lbluserSal.grid(row=8, column=2,padx=10,pady=10, sticky="w")
        # self.txtuserSal = Entry(self.user_frame, textvariable=self.usersal, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        # self.txtuserSal.grid(row=8, column=3,padx=10,pady=10, sticky="w")
#============================================================================Salary==================================================

        self.btn_user = Frame(self.user_frame, bg="#535c68")
        self.btn_user.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")

       
        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Register User",text_font=('Helvetica', 12),command=lambda:[self.add_to_User_register(),self.exit_register()]).grid(row=8, pady = 10, column=1)

        
        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Registr Admin",text_font=('Helvetica', 12),command=lambda:[self.add_to_Admin_register(),self.exit_register()]).grid(row=8, pady = 10, column=0)


        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Update User",text_font=('Helvetica', 12),command=lambda:[self.update_user_area(),self.exit_register()]).grid(row=9, pady = 10, column=1)


        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Update Admin",text_font=('Helvetica', 12),command=lambda:[self.update_admin_area(),self.exit_register()]).grid(row=9, pady = 10, column=0)

        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Delete User",text_font=('Helvetica', 12),command=lambda:[self.delete_users(),self.exit_register()]).grid(row=10, pady = 10, column=1)


        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Delete Admin",text_font=('Helvetica', 12),command=lambda:[self.delete_admins(),self.exit_register()]).grid(row=10, pady = 10, column=0)
        
        
        user_tree_frame = Frame(self.register_window,bg="gold")
        user_tree_frame.place(x=900, y=50, width=615, height=295)

        '''Table Show Data'''
        User_Frame=Frame(user_tree_frame,relief=RIDGE,bg="crimson")
        User_Frame.place(x=10,y=26,width=595,height=255)

        self.lbl_edit1=Label(user_tree_frame,text="Users",bg="gold",fg="Black",font=("times new roman",10,"bold"))
        self.lbl_edit1.grid(row=0,column=0,pady=5,padx=5,sticky="w")

        scroll_x=Scrollbar(User_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(User_Frame,orient=VERTICAL)
        self.user_table=ttk.Treeview(User_Frame,columns=("UserId","UserName", "Email", "PhoneNo", "Address", "Active"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        self.user_table.heading("UserId",text="UserId")
        self.user_table.heading("UserName",text="UserName")
        self.user_table.heading("Email",text="Email")
        self.user_table.heading("PhoneNo",text="PhoneNo")
        self.user_table.heading("Address",text="Address")
        self.user_table.heading("Active",text="Active")
        self.user_table['show']='headings'
        self.user_table.column("UserId",width=10)
        self.user_table.column("UserName",width=10)
        self.user_table.column("Email",width=10)
        self.user_table.column("PhoneNo",width=10)
        self.user_table.column("Address",width=10)
        self.user_table.column("Active",width=10)
        self.user_table.pack(fill=BOTH,expand=1)
        self.user_table.bind("<ButtonRelease-1>",self.get_user_Data)
        self.dispalyUser()
        '''Admin Tree View'''
        admin_tree_frame = Frame(self.register_window,bg="gold")
        admin_tree_frame.place(x=900, y=350, width=615, height=350)

        admin_Frame=Frame(admin_tree_frame,relief=RIDGE,bg="crimson")
        admin_Frame.place(x=10,y=26,width=595,height=285)

        self.lbl_edit1=Label(admin_tree_frame,text="Admins",bg="gold",fg="Black",font=("times new roman",10,"bold"))
        self.lbl_edit1.grid(row=0,column=0,pady=5,padx=5,sticky="w")

        scroll_x=Scrollbar(admin_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(admin_Frame,orient=VERTICAL)
        self.admin_table=ttk.Treeview(admin_Frame,columns=("UserId","UserName", "Email", "PhoneNo", "Address", "Active"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.admin_table.xview)
        scroll_y.config(command=self.admin_table.yview)

        self.admin_table.heading("UserId",text="UserId")
        self.admin_table.heading("UserName",text="UserName")
        self.admin_table.heading("Email",text="Email")
        self.admin_table.heading("PhoneNo",text="PhoneNo")
        self.admin_table.heading("Address",text="Address")
        self.admin_table.heading("Active",text="Active")
        self.admin_table['show']='headings'
        self.admin_table.column("UserId",width=10)
        self.admin_table.column("UserName",width=10)
        self.admin_table.column("Email",width=10)
        self.admin_table.column("PhoneNo",width=10)
        self.admin_table.column("Address",width=10)
        self.admin_table.column("Active",width=10)
        self.admin_table.pack(fill=BOTH,expand=1)
        self.admin_table.bind("<ButtonRelease-1>",self.get_admin_Data)
        self.dispalyAdmin()
        

    # def fetch_doc_pateint_number_details(self):
    #     con=sqlite3.connect(database="apollo.db")
    #     cur=con.cursor()
    #     cur.execute("SELECT * from sal_structure")
    #     row_sal=cur.fetchall()
    #     for sal_structure in row_sal:
    #         sal_basic =  (float(sal_structure[1]))*0.01
    #         sal_hra = (float(sal_structure[2]))*0.01 
    #         print("sal_hra:",sal_hra)
    #         sal_coveyance_allowance = (float(sal_structure[3]))*0.01 
    #         print("sal_coveyance_allowance:",sal_coveyance_allowance)
    #         sal_performence_bonus = (float(sal_structure[5]))*0.01 
    #         print("sal_performence_bonus:",sal_performence_bonus)
    #         sal_pf = (float(sal_structure[6]))*0.01 
    #         print("sal_pf:",sal_pf)
    #         sal_esi = (float(sal_structure[7]))*0.01 
    #         print("sal_esi:",sal_esi)
    #         sal_tax = (float(sal_structure[8]))*0.01 
    #         print("sal_tax:",sal_tax)
    #         sal_medical_allowance = (float(sal_structure[4]))*0.01

    #     # cur.execute("SELECT * from users where username LIKE '%"+str(self.search_user_sal.get())+"%'")
    #     # row=cur.fetchall()
        
    #     # for rows in row:
    #     #     emp_name = rows[1]
    #     #     emp_email = rows[3]
    #     #     emp_salary = rows[7]
    #         #print(self.txtuserSal.get())
    #         # emp_salary = float(self.txtuserSal.get())
    #         emp_salary = t_sal
    #         #emp_salary = float(self.usersal)
            
    #         performance_fee = float(emp_salary)*sal_performence_bonus
    #         basic1 =float(emp_salary)*sal_basic
    #         basic =float(emp_salary)
    #         convey_fee = (float(emp_salary))*sal_coveyance_allowance
    #         pf = (float(emp_salary))*sal_pf
    #         ESI = (float(emp_salary))*sal_esi

    #         contribution = (float(emp_salary))*0.13
    #         tax = (float(emp_salary))*sal_tax
    #         HRA = (float(emp_salary))*sal_hra
    #         medical_allowance = (float(emp_salary))*sal_hra

    #         self.basic.set(basic1)
    #         self.hra.set(HRA)
    #         self.conveyance_allowance.set(convey_fee)
    #         self.medical_allowance.set(0.0)
    #         self.performance_bonus.set(performance_fee)
    #         self.pf.set(pf)
    #         self.esi.set(ESI)
    #         self.tax.set(tax)

    def enable(self):
        self.txtpassword.config(state=NORMAL)

    def disable(self):
        self.txtpassword.config(state=DISABLED)

    def enable(self):
        self.txtpassword.config(state=NORMAL)
       
    def new_rand(self):
        self.txtpassword.delete(0, END)
        pw_length = int(8)
        my_password = ''
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        my_password = ''.join(random.choice(chars) for i in range(pw_length))
        self.txtpassword.insert(0, my_password)
        
    def clipper_admin(self):
        self.register_window.clipboard_clear()
        self.register_window.clipboard_append(self.txtpassword.get())

    def add_to_User_register(self):
        '''Validation'''
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from users where username LIKE '%"+str(self.txtuserName.get())+"%'")
        row=cur.fetchall()
        txt_Ph =self.txtPhone_no.get()
        #===============================================
        txt_mail = self.txtEmail.get()
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        re.search(regex,txt_mail)
        #==========================================
        if row == [] and (txt_Ph.isdigit()) and re.search(regex,txt_mail) and (self.usersal.get()).isdigit(): 
            #self.txtBasic.get(),self.txtHRA.get(),self.txtCon_alow.get(),self.txtMed_alow.get(),self.txtBonus.get(),self.txtPF.get(),self.txtESI.get(),self.txtTax.get()
            self.db.insert_User_register(self.txtuserName.get(), self.txtpassword.get(), txt_mail, txt_Ph, self.txtAdress.get(),self.user_search.get(),self.usersal.get())
            #self.txtBasic.get(),self.txtHRA.get(),self.txtCon_alow.get(),self.txtMed_alow.get(),self.txtBonus.get(),self.txtPF.get(),self.txtESI.get(),self.txtTax.get())
            messagebox.showinfo("Success", "Record Inserted")
            logging.info('Registered user successfully')

        else:
            messagebox.showinfo("Failure", "User name already exits or give valid input")
    
    def exit_register(self):
            self.register_window.destroy()
            logging.info('Exited from user register Window Successfully')

    '''Validation'''
    def add_to_Admin_register(self):
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from admins where username LIKE '%"+str(self.txtuserName.get())+"%'")
        row=cur.fetchall()
        #===============================================
        txt_Ph =self.txtPhone_no.get()
        txt_mail = self.txtEmail.get()
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        re.search(regex,txt_mail)
        #==========================================
        if row == [] and (txt_Ph.isdigit()) and re.search(regex,txt_mail) and (self.usersal.get()).isdigit(): 
            self.db.insert_admin_register(self.txtuserName.get(), self.txtpassword.get(), self.txtEmail.get(), self.txtPhone_no.get(), self.txtAdress.get(),self.user_search.get())
            messagebox.showinfo("Success", "Record Inserted")
            logging.info('Registered user successfully')
        else:
            messagebox.showinfo("Failure", "User name already exits or give valid input")
    
    def get_user_Data(self,event):
        self.clearAllUser()
        selected_row = self.user_table.focus()
        data = self.user_table.item(selected_row)
        global row_user
        row_user = data["values"]
        print(row_user)
        self.username.set(row_user[1])
        self.email.set(row_user[2])
        self.phone_no.set(row_user[3])
        self.address.set(row_user[4])
        self.active.set(row_user[5])

    def get_admin_Data(self,event):
        self.clearAllUser()
        selected_row = self.admin_table.focus()
        data = self.admin_table.item(selected_row)
        global row_admin
        row_admin = data["values"]
        self.username.set(row_admin[1])
        self.email.set(row_admin[2])
        self.phone_no.set(row_admin[3])
        self.address.set(row_admin[4])
        self.active.set(row_admin[5])

    def clearAllUser(self):
        self.username.set("")
        self.password.set("")
        self.email.set("")
        self.phone_no.set("")
        self.address.set("")
        self.active.set("")

    def dispalyUser(self,*args):
        self.user_table.delete(*self.user_table.get_children())
        for row in self.db.fetch_user():
            self.user_table.insert("", END, values=row)

    def dispalyAdmin(self,*args):
        self.admin_table.delete(*self.admin_table.get_children())
        for row in self.db.fetch_admin():
            self.admin_table.insert("", END, values=row)

    def update_admin_area(self):
        if self.txtuserName.get() == "" and self.txtpassword.get() == "" and self.user_search.get() =="":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        self.db.update_admin(self.txtuserName.get(), self.txtpassword.get(), self.txtEmail.get(), self.txtPhone_no.get(), self.txtAdress.get(),self.user_search.get(),row_admin[0])
        messagebox.showinfo("Success", "Admin Record Updated")

    def update_user_area(self):
        if self.txtuserName.get() == "" and self.txtpassword.get() == "" and self.user_search.get() =="":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        self.db.update_user(self.txtuserName.get(), self.txtpassword.get(), self.txtEmail.get(), self.txtPhone_no.get(), self.txtAdress.get(),self.user_search.get(),row_user[0])
        messagebox.showinfo("Success", "User Record Updated")

    def delete_users(self):
        self.db.remove_user(row_user[0])
        self.clearAllUser()

    def delete_admins(self):
        self.db.remove_admin(row_admin[0])
        self.clearAllUser()

class Window_user_edit(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,master):
        self.master = master
        self.master.title("Edit User")
        self.master.geometry("1100x650")
        self.master.config(bg = 'grey')
        self.username = StringVar()
        self.password = StringVar()
        self.email = StringVar()
        self.phone_no = StringVar()
        self.address = StringVar()
        self.active = StringVar()
        self.user_name = StringVar()
        self.user_conform_password = StringVar()

        img = Image.open('images/tablet.jpg')
        logo = img.resize((1100, 650), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.master,image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=650)

        self.user_frame = Frame(self.master,bg="light green")
        self.user_frame.place(x=20, y=100, width=400, height=400)
        self.user_frame1 = Frame(self.master,bg="light green")
        self.user_frame1.place(x=240, y=10, width=600, height=77)
        space=(10 * ' ')
        self.lbluserName = Label(self.user_frame1, text=f"{space} EDIT USER PROFILE", font=("times new roman", 30, "bold"), bg="light green", fg="black") ##535c68
        self.lbluserName.grid(row=0, column=1)

        self.lbluserName = Label(self.user_frame, text="User Name", font=("Calibri", 14), bg="light green", fg="black") ##535c68
        self.lbluserName.grid(row=0, column=0,padx=10,pady=10, sticky="w")
        self.txtuserName = Entry(self.user_frame, textvariable=self.username, font=("Calibri", 14), width=20)
        self.txtuserName.grid(row=0, column=1,padx=10,pady=10, sticky="w")
        self.txtuserName.config(state=DISABLED)

        self.conform_password = Label(self.user_frame, text="Old Password", font=("Calibri", 14), bg="light green", fg="black")
        self.conform_password.grid(row=1,column=0,pady=10,padx=10,sticky="w")
        self.conform_password = Entry(self.user_frame,show = "*", textvariable=self.user_conform_password, font=("Calibri", 14), width=20)
        self.conform_password.grid(row=1, column=1,padx=10,pady=10, sticky="w")

        self.lblPassword = Label(self.user_frame, text="New Password", font=("Calibri", 14), bg="light green", fg="black")
        self.lblPassword.grid(row=2, column=0,padx=10,pady=10, sticky="w")
        self.txtpassword = Entry(self.user_frame,show = "*", textvariable=self.password, font=("Calibri", 14), width=20)
        self.txtpassword.grid(row=2, column=1,padx=10,pady=10, sticky="w")
        self.txtpassword.config(state=DISABLED)

        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,fg_color='yellow',corner_radius=8,
        text="Generate Password",text_font=('Helvetica', 12),command=lambda:[self.enable(),self.new_rand(),self.disable()]).grid(row=6, column=1,padx=50,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,fg_color='yellow',corner_radius=8,
        text="Copy password",text_font=('Helvetica', 12),command=lambda:[self.clipper()]).grid(row=6, column=0,padx=5,pady=10, sticky="w")

        self.lblEmail = Label(self.user_frame, text="Email Id", font=("Calibri", 14), bg="light green", fg="black")
        self.lblEmail.grid(row=3, column=0,padx=10,pady=10, sticky="w")
        self.txtEmail = Entry(self.user_frame, textvariable=self.email, font=("Calibri", 14), width=20)
        self.txtEmail.grid(row=3, column=1,padx=10,pady=10, sticky="w")

        self.lblPhone_no = Label(self.user_frame, text="Phone No", font=("Calibri", 14), bg="light green", fg="black")
        self.lblPhone_no.grid(row=4, column=0,padx=10,pady=10, sticky="w")
        self.txtPhone_no = Entry(self.user_frame, textvariable=self.phone_no, font=("Calibri", 14), width=20)
        self.txtPhone_no.grid(row=4, column=1,padx=10,pady=10, sticky="w")

        self.lblAdress = Label(self.user_frame, text="Adress", font=("Calibri", 14), bg="light green", fg="black")
        self.lblAdress.grid(row=5, column=0,padx=10,pady=10, sticky="w")
        self.txtAdress = Entry(self.user_frame, textvariable=self.address, font=("Calibri", 14), width=20)
        self.txtAdress.grid(row=5, column=1,padx=10,pady=10, sticky="w")

        self.btnAdd = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,fg_color='green',text_color='white', corner_radius=8,
        text="Update User",text_font=('Calibri', 14),command=lambda:[self.conform_pass()]).grid(row=8, pady = 10, column=1)

        '''Admin Tree View'''
        admin_tree_frame = Frame(self.master,bg="light green")
        admin_tree_frame.place(x=500, y=100, width=505, height=400)

        admin_Frame=Frame(admin_tree_frame,relief=RIDGE,bg="crimson")
        admin_Frame.place(x=10,y=20,width=485,height=285)
        scroll_x=Scrollbar(admin_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(admin_Frame,orient=VERTICAL)
        self.admin_table=ttk.Treeview(admin_Frame,columns=("UserId","UserName", "Email", "PhoneNo", "Address"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.admin_table.xview)
        scroll_y.config(command=self.admin_table.yview)

        self.admin_table.heading("UserId",text="UserId")
        self.admin_table.heading("UserName",text="UserName")
        self.admin_table.heading("Email",text="Email")
        self.admin_table.heading("PhoneNo",text="PhoneNo")
        self.admin_table.heading("Address",text="Address")
        self.admin_table['show']='headings'
        self.admin_table.column("UserId",width=10)
        self.admin_table.column("UserName",width=10)
        self.admin_table.column("Email",width=10)
        self.admin_table.column("PhoneNo",width=10)
        self.admin_table.column("Address",width=10)
        self.admin_table.pack(fill=BOTH,expand=1)
        self.admin_table.bind("<ButtonRelease-1>",self.get_user_edit)
        result =ai, user_name_edit, user_email_edit, user_ph_no, user_address_edit, user_admin_edit
        self.admin_table.insert("",END, values=result)
        self.clearAllUser()
        self.button_event()

    def disable(self):
        self.txtpassword.config(state=DISABLED)

    def enable(self):
        self.txtpassword.config(state=NORMAL)
       
    def new_rand(self):
        self.txtpassword.delete(0, END)
        pw_length = int(8)
        my_password = ''
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        my_password = ''.join(random.choice(chars) for i in range(pw_length))
        self.txtpassword.insert(0, my_password)
        
    def clipper(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.txtpassword.get())
    
    def clearAllUser(self):
        self.username.set("")
        self.password.set("")
        self.email.set("")
        self.phone_no.set("")
        self.address.set("")
        self.active.set("")

    def get_user_edit(self,event):
        self.clearAllUser()
        selected_row = self.admin_table.focus()
        data = self.admin_table.item(selected_row)
        global row_admin
        row_admin = data["values"]
        self.username.set(user_name_edit)
        self.email.set(user_email_edit)
        self.phone_no.set(user_ph_no)
        self.address.set(user_address_edit)

    def conform_pass(self,*args):
            '''This ethod will conform old password and changes new password in user edit profile'''
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            try:
                cur.execute("SELECT * FROM users")
                row=cur.fetchall()
                for i in row:
                    if i[2] == self.user_conform_password.get() and self.txtuserName.get() == i[1]:
                        self.update_user_area()
                        logging.info('User password updated successfully')
                    else:
                        #messagebox.showerror("Error","Give correct old password")
                        logging.error('User password not updated')
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}")
                logging.error('Have an error, user data not updated')

    def update_user_area(self):
        self.db.update_user_edit(self.txtpassword.get(), self.txtEmail.get(), self.txtPhone_no.get(), self.txtAdress.get(), ai)
        messagebox.showinfo("Success", "User Record Updated")


class Window_coupon_edit(Super_Admin_Window,Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,cupon_window):
        self.cupon_window = cupon_window
        self.cupon_window.title("Edit User")
        self.cupon_window.geometry("1100x550")
        self.cupon_window.config(bg = 'grey')

        self.coupon_code_data = StringVar()
        self.coupon_amount = StringVar()
       
        img = Image.open('images/tablet.jpg')
        logo = img.resize((1100, 550), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.cupon_window,image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=550)

        self.coupon_frame = Frame(self.cupon_window,bg="light green")
        self.coupon_frame.place(x=20, y=100, width=420, height=300)

        self.coupon_frame1 = Frame(self.cupon_window,bg="light green")
        self.coupon_frame1.place(x=200, y=10, width=620, height=70)
        space = (10*' ')
        self.lblcoupon = Label(self.coupon_frame1, text=f"{space} CREATE DISSCOUNT", font=("Times new roman", 34,'bold'), bg="light green", fg="black") ##535c68
        self.lblcoupon.grid(row=0, column=0)

        self.lblcoupon = Label(self.coupon_frame, text="Disscount Name :", font=("Calibri", 14), bg="light green", fg="black") ##535c68
        self.lblcoupon.grid(row=1, column=0,padx=10,pady=10, sticky="w")
        self.txtcoupon = Entry(self.coupon_frame, textvariable=self.coupon_code_data, bd=7,relief=SUNKEN, font=("Calibri", 14), width=20)
        self.txtcoupon.grid(row=1, column=1,padx=10,pady=10, sticky="w")

        self.lblcoupon_disscount_amount = Label(self.coupon_frame, text="Discount % :", font=("Calibri", 14), bg="light green", fg="black")
        self.lblcoupon_disscount_amount.grid(row=2,column=0,pady=10,padx=10,sticky="w")
        self.txtcoupon_disscount_amount = Entry(self.coupon_frame, textvariable=self.coupon_amount, bd=7,relief=SUNKEN, font=("Calibri", 14), width=20)
        self.txtcoupon_disscount_amount.grid(row=2, column=1,padx=10,pady=10, sticky="w")

        self.btnAdd=Button(self.coupon_frame,command=lambda:[self.add_coupon(),self.exit_cupon()], text='Generate Disscount',font='arial 14 bold',bg='green',fg='white',padx=5,pady=5,width=14)
        self.btnAdd.grid(row=3,column=1,pady=10)

        self.btnAdd=Button(self.coupon_frame,command=lambda:[self.delete_coupons(),self.exit_cupon()], text='Delete Disscount',font='arial 16 bold',bg='green',fg='white',padx=5,pady=5,width=14)
        self.btnAdd.grid(row=4,column=1,pady=10)

        '''Admin Tree View'''
        coupon_tree_frame = Frame(self.cupon_window,bg="light green")
        coupon_tree_frame.place(x=500, y=100, width=505, height=300)

        coupon_Frame=Frame(coupon_tree_frame,relief=RIDGE,bg="crimson")
        coupon_Frame.place(x=10,y=20,width=485,height=255)
        scroll_x=Scrollbar(coupon_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(coupon_Frame,orient=VERTICAL)
        self.coupons_table=ttk.Treeview(coupon_Frame,columns=("DisscountId","DisscountCode", "Disscount%"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.coupons_table.xview)
        scroll_y.config(command=self.coupons_table.yview)

        self.coupons_table.heading("DisscountId",text="DisscountId")
        self.coupons_table.heading("DisscountCode",text="DisscountCode")
        self.coupons_table.heading("Disscount%",text="Disscount%")
        self.coupons_table['show']='headings'
        self.coupons_table.column("DisscountId",width=10)
        self.coupons_table.column("DisscountCode",width=10)
        self.coupons_table.column("Disscount%",width=10)
        self.coupons_table.pack(fill=BOTH,expand=1)
        self.coupons_table.bind("<ButtonRelease-1>",self.get_coupon_edit)
        self.dispalyAll_coupons()
        # self.clearAllUser()
        
    def get_coupon_edit(self,event):
        self.clearAllCoupon()
        selected_row = self.coupons_table.focus()
        data = self.coupons_table.item(selected_row)
        global row_cupon
        row_cupon = data["values"]
        self.coupon_code_data.set(row_cupon[1])
        self.coupon_amount.set(row_cupon[2])

    def dispalyAll_coupons(self):
        self.coupons_table.delete(*self.coupons_table.get_children())
        for row in self.db.fetch_cupon():
            self.coupons_table.insert("", END, values=row)

    def clearAllCoupon(self):
        self.coupon_code_data.set("")
        self.coupon_amount.set("")

    def exit_cupon(self):
            self.cupon_window.destroy()
            logging.info('Exited from cupon generate Window Successfully')
    
    def add_coupon(self):
        if self.txtcoupon.get() == "":
            messagebox.showerror("Erorr in Input", "Please fill all the valid details")
            #return
        else:
            self.db.insert_coupon(self.txtcoupon.get(),self.txtcoupon_disscount_amount.get())
            messagebox.showinfo("Success", "Cupon Inserted")

    def delete_coupons(self):
        '''This method will delete perticular product from the cart'''
        self.db.remove_coupons(row_cupon[0])


class Window_income(User_Window,Super_Admin_Window,Window_admin,Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,cupon_window):
        self.cupon_window = cupon_window
        self.cupon_window.title("Edit User")
        self.cupon_window.geometry("1100x750")
        self.cupon_window.config(bg = 'grey')

        self.income_amounts = StringVar()
        self.search_day = StringVar()
        self.from_date =StringVar()
        self.to_date = StringVar()

        img = Image.open('images/a3.webp')
        logo = img.resize((1100, 750), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.cupon_window,image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=750)

        self.revenue_frame = Frame(self.cupon_window,bg="sky blue")
        self.revenue_frame.place(x=20, y=100, width=1020, height=550)

        self.revenue_frame1 = Frame(self.cupon_window,bg="light green")
        self.revenue_frame1.place(x=200, y=10, width=620, height=50)
        space = (10*' ')
        self.lblcoupon = Label(self.revenue_frame1, text=f"{space} FIND OUT INCOME/REVENUE", font=("Times new roman", 26,'bold'), bg="sky blue", fg="black")
        self.lblcoupon.grid(row=0, column=0)
        
        '''Empty'''
        self.lblincome = Label(self.revenue_frame, text="", font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=0,padx=10,pady=10, sticky="w")

        self.lblincome = Label(self.revenue_frame, text="From Date:", font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=1,padx=10,pady=10, sticky="w")
        
        self.txtincome = DateEntry(self.revenue_frame, textvariable=self.from_date, date_pattern='y-mm-dd', bd=7,relief=SUNKEN, font=("Calibri", 12), width=20)
        self.txtincome.grid(row=1, column=2,padx=10,pady=10, sticky="w")

        self.lblincome = Label(self.revenue_frame, text="To Date:", font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=3,padx=10,pady=10, sticky="w")
        self.txtincome = DateEntry(self.revenue_frame, textvariable=self.to_date, date_pattern='y-mm-dd', bd=7,relief=SUNKEN, font=("Calibri", 12), width=20)
        self.txtincome.grid(row=1, column=4,padx=10,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.revenue_frame,width=14,height=30,border_width=0,text_color='white',fg_color='dark blue',corner_radius=8,
        text="Find Income",text_font=('Times new roman', 14),command=lambda:[self.search_datas11(),self.search_bt1(),self.delete_edit_income()])
        self.button.grid(row=1, column=5,padx=10,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.revenue_frame,width=14,height=30,border_width=0,text_color='white',fg_color='dark blue',corner_radius=8,
        text="Clear",text_font=('Times new roman', 14),command=lambda:[self.clear_income_text()])
        self.button.grid(row=1, column=6,padx=10,pady=10, sticky="w")

        # self.button = customtkinter.CTkButton(self.revenue_frame,width=14,height=30,border_width=0,text_color='white',fg_color='dark blue',corner_radius=8,
        # text="Emp sal",text_font=('Times new roman', 14),command=lambda:[self.search_emp_sal()])
        # self.button.grid(row=1, column=8,padx=10,pady=10, sticky="w")

        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.cupon_window,bg="sky blue",bd=10,relief=GROOVE)
        self.billing_area.place(x=70, y=170, width=870, height=470)
        self.billing_tiltle=Label(self.billing_area,text="Income",font="arial 15 bold",fg="black",bg="sky blue",bd=7,relief=GROOVE).pack(fill=X)

        scroll_y=Scrollbar(self.billing_area,orient=VERTICAL)
        self.billing_area=Text(self.billing_area,yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH,expand=1)

    def search_datas11(self,*args):
            '''This method will search products from database'''
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            self.search_month = StringVar()
            self.search_month_name = StringVar()
            
            global to_date_window3
            to_date_window3 = self.to_date
            try:
                cur.execute(f"select * from revenue where day_date >= \'{self.from_date.get()}\' AND day_date <= \'{self.to_date.get()}\'")
                rows=cur.fetchall()
                for row  in rows:
                    
                    self.db.insert_income_edit(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],row[11],row[12])
                    logging.info("Record inserted to revenue_edit table")

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}")
                logging.error("Record not inserted to revenue_edit table")

    def search_bt1(self):
        #global sum_amount, sum_quantity, tax_amount, net_profit_amount, final_profit_amount, float_income_amount, with_float_income,total_price, income_after_deduction_emp_sal, emp_sal, mrp_amount,Tax_total1, tax_mrp_total,final_profit_amount,final_profit_paid_amount, final_profit_price
        sum_amount = 0
        sum_quantity = 0
        tax_amount = 0
        net_profit_amount = 0
        final_profit_amount = 0
        final_profit_paid_amount = 0
        # float_income_amount = 0
        # with_float_income = 0
        income_after_deduction_emp_sal = 0
        emp_sal = 0
        
        mrp_amount = 0
        Tax_total1 = 0
        final_profit_price = 0

        for row in self.db.edit_fetch_income():
            mrp_amount = mrp_amount + float(row[7])
            Tax_total1 = Tax_total1+float(row[6])
            print("Tax_total1:",Tax_total1)
            tax_mrp_total = Tax_total1 + mrp_amount

            sum_amount=sum_amount+float(row[9])
            sum_quantity=sum_quantity+float(row[6])
            tax_amount=tax_amount+float(row[8])

            net_profit_amount=net_profit_amount+float(row[7])
            final_profit_amount = (final_profit_amount+float(row[10]))
            #=======================================================================
            final_profit_paid_amount = (final_profit_paid_amount+float(row[12]))
            final_profit_price = final_profit_amount - final_profit_paid_amount
            #===============================================================

            # float_income_amount = float_income_amount + float(row[11])
            # with_float_income = float_income_amount + final_profit_amount
            # total_price = sum_amount + tax_amount
         
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            cur.execute(f"select salary_per_day from users_sal where clockin_date >= \'{self.from_date.get()}\' AND clockin_date <= \'{self.to_date.get()}\'")
            rows=cur.fetchall()
            sum_sal=0
            for r1  in rows:
                sum_sal=sum_sal+float(r1[0])
            income_profit = final_profit_price - sum_sal
            income_after_deduction_emp_sal = income_after_deduction_emp_sal + (final_profit_price - emp_sal)

        self.billing_area.insert(END,"\tAPOLLO MEDICAL\n")
        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END,"\tYOUR INCOME\n")
        self.billing_area.configure(font='arial 14 bold')
        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END, f"\n======================================================================================================================\n")
        self.billing_area.insert(END,f"\t{'MRP_PRICE':<20}\t{'TAX_APPLIED':<20}\t{'TOTAL_PRICE':<20}\t{'PROFIT_PRICE':>30}\t\n")
        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END,f"\t{round(mrp_amount,2):<20}\t{round(Tax_total1,2):>20}\t{round(tax_mrp_total,2):>20}\t{round(final_profit_price,2):>50}\t\n")
        self.billing_area.insert(END, f"\n======================================================================================================================\n")

        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END, f"\n======================================================================================================================\n")
        self.billing_area.insert(END, f"\tAFTER DEDUCTION OF EMPLOYEE SAL THE TOTAL PROFIT\n")
        self.billing_area.configure(font='arial 14 bold')
        self.billing_area.insert(END, f"\n======================================================================================================================\n")
        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END,f"\t{'PROFIT_WITH_FLOAT_PRICE':<20}\t{'EMP_SAL':>30}\t{'PROFI_AFTER_DEDUCTION_OF_EMP_SAL':>50}\n")
        self.billing_area.insert(END, f"\n")
        self.billing_area.insert(END,f"\t{round(final_profit_price,2):<20}\t\t{round(sum_sal,2):>50}\t\t{round(income_profit,2):>50}\t\n")
        self.billing_area.insert(END, f"\n======================================================================================================================\n")
        self.billing_area.configure(font='arial 9 bold')

    def delete_edit_income(self):
        '''This method deletes all data from revenue_edit table'''
        self.db.remove_edit_income()

    def add_income_edit(self):
        self.db.insert_income_edit(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        messagebox.showinfo("Success", "Cupon Inserted")

    def clear_income_text(self):
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0','end')
        logging.info('income area cleared')
        

class Window_add_products(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,add_product):
        self.add_product = add_product
        self.add_product.title("Medical billing")
        self.add_product.geometry("1100x700+0+0")
        self.add_product.config(bg = '#2c3e50')

        img = Image.open('images/tablet.jpg')
        logo = img.resize((1100, 700), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.add_product,image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=700)

        self.items = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        
        self.search_by1 = StringVar()
        self.Total_price=StringVar()
        self.total_price=StringVar()
        self.tablet_details=StringVar()
        
        self.Sheet=StringVar()
        self.amount_purchased = StringVar()
        self.CGST_Amount = StringVar()
        self.SGST_Amount = StringVar()
        
        self.entries_frame = Frame(self.add_product,bg="light green")
        self.entries_frame.place(x=100, y=10, width=875, height=225)
        
        title = Label(self.entries_frame, text="BILLING SYSTEM", font=("Calibri", 14, "bold"), bg="light green", fg="white")
        title.grid(row=0, columnspan=2, sticky="w")
        
        self.lblName = Label(self.entries_frame, text="Product_Name", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblName.grid(row=1, column=0,padx=10,pady = 5, sticky="w")
        self.txtName = Entry(self.entries_frame, textvariable=self.items, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtName.grid(row=1, column=1,padx=10,pady = 5, sticky="w")

        self.lblMrp_Price = Label(self.entries_frame, text="Product_MRP_Price", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblMrp_Price.grid(row=2, column=0,padx=10,pady = 5, sticky="w")
        self.txtMrp_Price = Entry(self.entries_frame, textvariable=self.price, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtMrp_Price.grid(row=2, column=1,padx=10,pady = 5, sticky="w")

        self.lblQuantity = Label(self.entries_frame, text="Product_Quantity", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblQuantity.grid(row=3, column=0,padx=10,pady = 5, sticky="w")
        self.txtQuantity = Entry(self.entries_frame, textvariable=self.quantity, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtQuantity.grid(row=3, column=1,padx=10,pady = 5, sticky="w")
 
        self.lblamount_purchased = Label(self.entries_frame, text="Purchased_disscount%", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblamount_purchased.grid(row=1, column=2,padx=10,pady = 5, sticky="w")
        self.txtamount_purchased = Entry(self.entries_frame, textvariable=self.amount_purchased, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtamount_purchased.grid(row=1, column=3,padx=10,pady = 5, sticky="w")

        self.lblCGST = Label(self.entries_frame, text="CGST%", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblCGST.grid(row=2, column=2,padx=10,pady = 5, sticky="w")
        self.txtCGST = Entry(self.entries_frame, textvariable=self.CGST_Amount, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtCGST.grid(row=2, column=3,padx=10,pady = 5, sticky="w")

        self.lblSGST = Label(self.entries_frame, text="SGST%", font=("Calibri", 12), bg="#535c68", fg="white")
        self.lblSGST.grid(row=3, column=2,padx=10,pady = 5, sticky="w")
        self.txtSGST = Entry(self.entries_frame, textvariable=self.SGST_Amount, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtSGST.grid(row=3, column=3,padx=10,pady = 5, sticky="w")
        
        self.lblTablet_details = Label(self.entries_frame, text="Tablet_details", font=("Calibri", 10), bg="#535c68", fg="white")
        self.lblTablet_details.grid(row=4, padx=10,column=0, sticky="w")
        self.txtTablet_deatails = Entry(self.entries_frame, textvariable=self.tablet_details, font=("Calibri", 12),bd=7,relief=SUNKEN, width=15)
        self.txtTablet_deatails.grid(row=4, padx=10,column=1, sticky="w")
        

        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Add Product",text_font=('Helvetica', 8,'bold'),command=self.add_items).grid(row=1, column=6,padx=10)

        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Update Product",text_font=('Helvetica', 8,'bold'),command=self.update_items).grid(row=2, column=6,padx=10)
        
        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Delete Product",text_font=('Helvetica', 8,'bold'),command=self.delete_items).grid(row=3, column=6,padx=10)

        self.button = customtkinter.CTkButton(self.entries_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Clear Product",text_font=('Helvetica', 8,'bold'),command=self.clearAll).grid(row=4, column=6,padx=10)
        

        '''Table Frame (displaying data from data base)'''
        tree_frame = Frame(self.add_product,bg="light green")
        tree_frame.place(x=100, y=275, width=875, height=390)

        lbl_search=Label(tree_frame,text="Search Products",bg="green",fg="white",font=("times new roman",14,"bold"))
        lbl_search.grid(row=0,column=0,pady=5,padx=5,sticky="w")

        txt_Search= Entry(tree_frame,textvariable=self.search_txt,width=20,font=("times new roman",10,"bold") ,bd=5,relief=GROOVE)
        txt_Search.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        txt_Search.bind("<Key>",self.search)

        '''Table Show Data'''
        Table_Frame=Frame(tree_frame,relief=RIDGE,bg="crimson")
        Table_Frame.place(x=10,y=70,width=855,height=300)
        #Table_Frame.place(x=10,y=150,width=475,height=300)
        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
        self.billing_table=ttk.Treeview(Table_Frame,columns=("ProductID","Products","Quantity","MRP_Price","product_details","CGST","SGST","Purchase_price"),xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)

        self.billing_table.heading("ProductID",text="ProductID")
        self.billing_table.heading("Products",text="Products")
        self.billing_table.heading("Quantity",text="quantity")
        self.billing_table.heading("MRP_Price",text="MRP_Price")
        self.billing_table.heading("product_details",text="product_details")
        self.billing_table.heading("CGST",text="CGST")
        self.billing_table.heading("SGST",text="SGST")
        self.billing_table.heading("Purchase_price",text="Purchase_price")
        self.billing_table['show']='headings'
        self.billing_table.column("ProductID",width=2)
        self.billing_table.column("Products",width=100)
        self.billing_table.column("Quantity",width=10)
        self.billing_table.column("MRP_Price",width=20)
        self.billing_table.column("product_details",width=20)
        self.billing_table.column("CGST",width=10)
        self.billing_table.column("SGST",width=20)
        self.billing_table.column("Purchase_price",width=20)
        self.billing_table.pack(fill=BOTH,expand=1)
        self.billing_table.bind("<ButtonRelease-1>",self.getData)

    def getData(self,event):
        '''It will get data from database and display it'''
        self.clearAll()
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]
        print(row)
        global quantity_set
        quantity_set = row[2]
        self.items.set(row[1])
        self.quantity.set(row[2])
        self.price.set(row[3])
        self.tablet_details.set(row[4])   
        self.SGST_Amount.set(row[5])           
        self.CGST_Amount.set(row[6])
        self.amount_purchased.set(row[7])

    def dispalyAll(self):
        ''' This method will display all aitems from database'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.fetch():
            self.billing_table.insert("", END, values=row)

    def search_dispalyAll(self):
        '''It will search the products from database according to there alphabets'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.search_data():
            self.billing_table.insert("", END, values=row)

    def add_items(self):
        '''This method will add products'''
        if self.txtName.get() == "":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        txt_Name = float(self.txtMrp_Price.get())
        self.db.insert(self.txtName.get(),self.txtQuantity.get(),txt_Name,self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get())
        self.clearAll()
        self.dispalyAll()

    def update_items(self):
        '''This method will update products'''
        self.db.update(self.txtName.get(),self.txtQuantity.get(),self.txtMrp_Price.get(),self.txtTablet_deatails.get(),self.txtCGST.get(),self.txtSGST.get(),self.txtamount_purchased.get(),row[0])
        messagebox.showinfo("Success", "Record Update")
        logging.info('Updated products successfully')
        self.clearAll()
        self.dispalyAll()

    def delete_items(self):
        self.db.remove(row[0])
        self.clearAll()
        self.dispalyAll()

    def clearAll(self):
        self.items.set("")
        self.quantity.set("")
        self.price.set("")
        self.Sheet.set("")
        self.tablet_details.set("")
        self.amount_purchased.set("")
        self.CGST_Amount.set("")
        self.SGST_Amount.set("")

    def search(self,*args):
            con=sqlite3.connect(database="apollo.db")
            cur=con.cursor()
            try:
                cur.execute("SELECT * FROM products where product_name LIKE '%"+str(self.search_txt.get())+"%'")
                row=cur.fetchall()
                if len(row)>0:
                    self.billing_table.delete(*self.billing_table.get_children())
                    for i in row:
                        self.billing_table.insert("",END,values=i)
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}")

class Window_Bill_Search(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("900x780+0+0")
        self.master.config(bg = 'sky blue')

        self.search_bill = StringVar()
        self.search_by1 = StringVar()
       
        '''displaying bill area and dimenions'''
        '''Customer Details'''
        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.master,bg="#535c68",bd=10,relief=GROOVE)
        self.billing_area.place(x=100, y=100, width=550, height=570)
        self.billing_tiltle=Label(self.billing_area,text="Bill Area",font="arial 15 bold",fg="white",bg="#535c68",bd=7,relief=GROOVE).pack(fill=X)

        scroll_y=Scrollbar(self.billing_area,orient=VERTICAL)
        self.billing_area=Text(self.billing_area,yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH,expand=1)
        self.welcome_default()

        self.billing_edit = Frame(self.master,bg="#535c68")
        self.billing_edit.place(x=100, y=20, width=550, height=80) #490

        self.lbl_edit=Label(self.billing_edit,text="Cart",bg="#535c68",fg="white",font=("times new roman",14,"bold"))
        self.lbl_edit.grid(row=0,column=0,pady=10,padx=20,sticky="w")

        self.combo_search=ttk.Combobox(self.billing_edit,textvariable=self.search_by1,width=7,font=("times new roman",11,"bold"),state='readonly')
        self.combo_search['values']=("bill_no")
        self.combo_search.grid(row=0,column=1,padx=5,pady=5)

        self.search_btn = Button(self.billing_edit,text="Search_Customer_Bill",bg="skyblue", width=17,pady=5,command=lambda:[self.user_bill()]).grid(row=0, column=3,padx=5,pady=5)
        self.search_btn = Button(self.billing_edit,text="Clear",bg="skyblue", width=12,pady=5,command=lambda:[self.clear_bill_text()]).grid(row=0, column=4,padx=5,pady=5)

        self.txtBillSearch=Entry(self.billing_edit,width=9,font="arial 11",bd=7,relief=SUNKEN,textvariable=self.search_bill).grid(row=0, column=2,pady=5,padx=10)

    def user_bill(self):
        '''This method will generate user bill histroy and display it'''
        self.user_bill_history()

        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from customer_datas where "+str(self.search_by1.get())+" LIKE '%"+self.search_bill.get()+"%'")
        rows1 = cur.fetchall()
        #rupee = u"\u20B9"
        for row in rows1:
            print(row[3])
            self.billing_area.insert(END, f"\n{row[3]}\t\t{row[4]}\t\t{row[5]}\t\t\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\nTax:{(row[7])}% \t Total Products Amount: Rs. {row[6]}\n")
        self.billing_area.insert(END, f"\nCGST :  {row[11]}% \t  SGST : {row[12]}%\n")
        self.billing_area.insert(END, f"\nTotal Amount :\t\t Rs. {row[8]}\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\nCoupon Disscount :\t\t{row[14]}%\n")
        self.billing_area.insert(END, f"\nTotal Paybill Amount :\t\t Rs. {row[15]}\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.billing_area.insert(END, f"\n\tTHANK YOU\n")
        self.billing_area.insert(END, f"\n======================================\n")
        self.disable_text()
        logging.info('Customer bill searched successfully')

    def user_bill_history(self):
        '''Method will display searched bill history'''
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from customer_datas where "+str(self.search_by1.get())+" LIKE '%"+self.search_bill.get()+"%'")
        rows1 = cur.fetchall()
        for row in rows1:
            self.billing_area.delete(1.0,END)
            self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
            self.billing_area.insert(END,"\t  Hitech City Anjaiya Nagar\n")
            self.billing_area.insert(END,"\t    Hyderabad 500084\n")
            self.billing_area.insert(END,f"\n\nBill Number:\t\t{row[2]}")
            self.billing_area.insert(END,f"\nPhone Number:\t\t{row[1]}")
            self.billing_area.insert(END,f"\nBill_Date:{row[9]}")
            self.billing_area.insert(END,f"\n\n======================================")
            self.billing_area.insert(END,"\nProduct\t\tQTY\t\tPrice Rs.")
            self.billing_area.insert(END,f"\n======================================\n")
            self.billing_area.configure(font='arial 12 bold')

    def disable_text(self):
        self.billing_area.config(state= DISABLED)

    def clear_bill_text(self):
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0','end')
        logging.info('Bill area cleared')

    def welcome_default(self):
        self.billing_area.insert(END,"\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END,"\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END,"\t       Hyderabad 500084\n")
        self.billing_area.configure(font='arial 12 bold')

class Window_emp(Database,Login_Window):
    db=Database("apollo.db")
    def __init__(self,cupon_window):
        self.cupon_window = cupon_window
        self.cupon_window.title("Edit User")
        self.cupon_window.geometry("1920x1080")        
        self.cupon_window.config(bg = 'grey')

        self.search_user_sal = StringVar()

        self.basic = StringVar()
        self.hra = StringVar()
        self.conveyance_allowance = StringVar()
        self.medical_allowance = StringVar()
        self.performance_bonus =StringVar()
        self.pf = StringVar()
        self.esi = StringVar()
        self.tax = StringVar()
        # img = Image.open('a3.webp')
        # logo = img.resize((1100, 750), Image.Resampling.LANCZOS)
        # logo = ImageTk.PhotoImage(logo)
        # logo_label = tk.Label(self.cupon_window,image=logo)
        # logo_label.image = logo
        # logo_label.place(width=1100, height=750)

        self.revenue_frame_main = Frame(self.cupon_window,bg="grey")
        self.revenue_frame_main.place(x=20, y=100, width=1120, height=550)

        self.revenue_frame = Frame(self.cupon_window,bg="sky blue")
        self.revenue_frame.place(x=20, y=100, width=980, height=650)

        self.user_frame = Frame(self.cupon_window,bg="light green")
        self.user_frame.place(x=1020, y=100, width=470, height=650)

        self.revenue_frame1 = Frame(self.cupon_window,bg="light green")
        self.revenue_frame1.place(x=200, y=10, width=620, height=50)
        space = (10*' ')
        self.lblcoupon = Label(self.revenue_frame1, text=f"{space} FIND OUT EMPLOYEE SAL", font=("Times new roman", 26,'bold'), bg="sky blue", fg="black")
        self.lblcoupon.grid(row=0, column=0)
        
        '''Empty'''
        self.lblincome = Label(self.revenue_frame, text="", font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=0,padx=10,pady=10, sticky="w")

        self.lblincome = Label(self.revenue_frame, text="Search User:", font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=1,padx=10,pady=10, sticky="w")
        
        self.txtincome = Entry(self.revenue_frame, textvariable=self.search_user_sal, bd=7,relief=SUNKEN, font=("Calibri", 12), width=20)
        self.txtincome.grid(row=1, column=2,padx=10,pady=10, sticky="w")

        #============================================
        self.lblBasic = Label(self.user_frame, text="Basic", font=("Calibri", 12), bg="light green", fg="black") #bg="#535c68"
        self.lblBasic.grid(row=0, column=2,padx=10,pady=10, sticky="w")
        self.txtBasic = Entry(self.user_frame, textvariable=self.basic, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtBasic.grid(row=0, column=3,padx=10,pady=10, sticky="w")
        #self.txtName.config(state=DISABLED)
# self.txtBasic.get(),self.txtHRA.get(),self.txtCon_alow.get(),self.txtMed_alow.get(),self.txtBonus.get(),self.txtPF.get(),self.txtESI.get(),self.txtTax.get()
        self.lblHRA = Label(self.user_frame, text="HRA", font=("Calibri", 12), bg="light green", fg="black")
        self.lblHRA.grid(row=1, column=2,padx=10,pady=10, sticky="w")
        self.txtHRA = Entry(self.user_frame, textvariable=self.hra, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtHRA.grid(row=1, column=3,padx=10,pady=10, sticky="w")
        #self.txtHRA.config(state=DISABLED)

        self.lblCon_alow = Label(self.user_frame, text="Conveyance Allowance", font=("Calibri", 12), bg="light green", fg="black")
        self.lblCon_alow.grid(row=2, column=2,padx=10,pady=10, sticky="w")
        self.txtCon_alow = Entry(self.user_frame, textvariable=self.conveyance_allowance, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtCon_alow.grid(row=2, column=3,padx=10,pady=10, sticky="w")

        self.lblMed_alow = Label(self.user_frame, text="Medical Allowance", font=("Calibri", 12), bg="light green", fg="black")
        self.lblMed_alow.grid(row=3, column=2,padx=10,pady=10, sticky="w")
        self.txtMed_alow = Entry(self.user_frame, textvariable=self.medical_allowance, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtMed_alow.grid(row=3, column=3,padx=10,pady=10, sticky="w")

        self.lblBonus = Label(self.user_frame, text="Performance Bonus", font=("Calibri", 12), bg="light green", fg="black")
        self.lblBonus.grid(row=4, column=2,padx=10,pady=10, sticky="w")
        self.txtBonus = Entry(self.user_frame, textvariable=self.performance_bonus, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtBonus.grid(row=4, column=3,padx=10,pady=10, sticky="w")

        self.lblPF = Label(self.user_frame, text="PF", font=("Calibri", 12), bg="light green", fg="black") #bg="#535c68"
        self.lblPF.grid(row=5, column=2,padx=10,pady=10, sticky="w")
        self.txtPF = Entry(self.user_frame, textvariable=self.pf, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtPF.grid(row=5, column=3,padx=10,pady=10, sticky="w")

        self.lblESI = Label(self.user_frame, text="ESI", font=("Calibri", 12), bg="light green", fg="black")
        self.lblESI.grid(row=6, column=2,padx=10,pady=10, sticky="w")
        self.txtESI = Entry(self.user_frame, textvariable=self.esi, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtESI.grid(row=6, column=3,padx=10,pady=10, sticky="w")

        self.lblTax = Label(self.user_frame, text="Tax", font=("Calibri", 12), bg="light green", fg="black")
        self.lblTax.grid(row=7, column=2,padx=10,pady=10, sticky="w")
        self.txtTax = Entry(self.user_frame, textvariable=self.tax, font=("Calibri", 12),bd=7,relief=SUNKEN, width=20)
        self.txtTax.grid(row=7, column=3,padx=10,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Submit",text_font=('Helvetica', 12),command=lambda:[self.add_to_sal_structure()]).grid(row=8, column=2,padx=10,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.user_frame,width=8,height=20,border_width=0,corner_radius=8,
        text="Update",text_font=('Helvetica', 12),command=lambda:[self.update_sal_struct()]).grid(row=8, column=3,padx=10,pady=10, sticky="w")

        # self.lbluserSal = Label(self.user_frame, text="User Sal", font=("Calibri", 14), bg="light green", fg="black") #bg="#535c68"
        # self.lbluserSal.grid(row=8, column=2,padx=10,pady=10, sticky="w")
        # self.txtuserSal = Entry(self.user_frame, textvariable=self.usersal, font=("Calibri", 14),bd=7,relief=SUNKEN, width=20)
        # self.txtuserSal.grid(row=8, column=3,padx=10,pady=10, sticky="w")
        #=================================================================================

        self.button = customtkinter.CTkButton(self.revenue_frame,width=14,height=30,border_width=0,text_color='white',fg_color='dark blue',corner_radius=8,
        text="Find Income",text_font=('Times new roman', 14),command=lambda:[self.emp_sal()])
        self.button.grid(row=1, column=3,padx=10,pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.revenue_frame,width=14,height=30,border_width=0,text_color='white',fg_color='dark blue',corner_radius=8,
        text="Find Sal",text_font=('Times new roman', 14),command=lambda:[self.emp_sal()])
        self.button.grid(row=1, column=4,padx=10,pady=10, sticky="w")

        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.cupon_window,bg="sky blue") #,bd=10,relief=GROOVE)
        self.billing_area.place(x=50, y=170, width=920, height=570)
        #self.billing_tiltle=Label(self.billing_area,text="Income",font="arial 15 bold",fg="black",bg="sky blue",bd=7,relief=GROOVE).pack(fill=X)

        scroll_y=Scrollbar(self.billing_area,orient=VERTICAL)
        self.billing_area=Text(self.billing_area,yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH,expand=1)

    
    def add_to_sal_structure(self):
            self.db.insert_sal_structure(self.txtBasic.get(),self.txtHRA.get(),self.txtCon_alow.get(),self.txtMed_alow.get(),
            self.txtBonus.get(),self.txtPF.get(),self.txtESI.get(),self.txtTax.get())

    def update_sal_struct(self):
        if self.txtBasic.get() == "" and self.txtHRA.get() == "" and self.txtCon_alow.get() =="" and self.txtMed_alow.get() == "" and self.txtBonus.get() == "" and self.txtPF.get() =="" and self.txtESI.get() == "" and self.txtTax.get() =="":
            messagebox.showerror("Erorr in Input", "Please Fill All the Details")
            return
        self.db.update_sal_structure(self.txtBasic.get(),self.txtHRA.get(),self.txtCon_alow.get(),self.txtMed_alow.get(),
            self.txtBonus.get(),self.txtPF.get(),self.txtESI.get(),self.txtTax.get(),row_user[0])
        messagebox.showinfo("Success", "Salary structure Record Updated")


    def fetch_doc_pateint_number_details(*args):
        print("entered in sal")
        # print("entering")
        # db = mysql.connector.connect(host="localhost", user="root", password="root", database="hospital")
        # mycursor = db.cursor()
        # mycursor_second = db.cursor()
        # try:
        #     """fetching next patient id"""mycursor_second.execute("select patient_id from admission")
        #     doc_det_second = mycursor_second.fetchall()
        #     for n in doc_det_second:
        #         lastpatid = n[0]
        #     lastpatid += 1            var_pat_no.set(lastpatid)
        #     """fetching doctor details auto"""mycursor.execute("select first_name from register where user_name='Doctor'")
        #     doc_det = mycursor.fetchall()
        #     doc_detail = [j[0] for j in doc_det]
        #     doc_detail.insert(0, "Select")
        #     pdoc_entry["values"] = doc_detail pdoc_entry.place(x=770, y=190, width=250)
        #     pdoc_entry.current(0)
        #     # log_logger.info("list of doctors fetched")        except EXCEPTION as e:
        #     print(e)
        #     # log_logger.info("Failed to fetch list of doctors", e)        finally:
        #     db.commit()
        #     db.close()

    # def emp_sal(self):
    #     con=sqlite3.connect(database="apollo.db")
    #     cur=con.cursor()
    #     cur.execute("SELECT * from users where username LIKE '%"+str(self.search_user_sal.get())+"%'")
    #     row=cur.fetchall()
    #     print("user_name:row:,",row)

    #     for rows in row:
    #         #global emp_name,emp_email,emp_number,emp_salary,convey_fee, HRA, basic, performance_fee, pf, tax, ESI, contribution, basic1
    #         emp_name = rows[1]
    #         emp_email = rows[3]
    #         #emp_number = rows[4]
    #         emp_salary = rows[7]
    #         emp_basicss = (float(rows[8]))*0.01
    #         #print("emp_basicss:",emp_basicss)
    #         emp_per = (float(rows[12]))*0.01
    #         #print("emp_per:",emp_per)
    #         basic1 =float(rows[7])*emp_basicss
    #         basic =float(rows[7])
    #         performance_fee = float(rows[7])*emp_per

    #         emp_con = (float(rows[10]))*0.01
    #         #print("emp_con:",emp_con)
    #         convey_fee = (float(emp_salary))*emp_con
    #         emp_pf = (float(rows[13]))*0.01
    #         pf = (float(emp_salary))*emp_pf
    #         emp_esi = (float(rows[14]))*0.01
    #         ESI = (float(emp_salary))*emp_esi
    #         contribution = (float(emp_salary))*0.13
    #         #tax = (float(emp_salary))*0.75
    #         emp_tax = (float(rows[15]))*0.01
    #         tax = (float(emp_salary))*emp_tax
    #         emp_hra = (float(rows[9]))*0.01
    #         HRA = (float(emp_salary))*emp_hra
            
    #     self.billing_area.insert(END, "PAYSLIP")
    #     self.billing_area.insert(END, "\n\nAPOLLO MEDICAL ANJAIAH NAGAR HYDERBAD")
    #     self.billing_area.insert(END, f"\nName: {emp_name}")
    #     self.billing_area.insert(END, f"\nEmail: {emp_email}")
    #     self.billing_area.insert(END, "\n\nSALARY DETAILS")
    #     self.billing_area.insert(END, "\n\n========================================================================================================")
    #     # self.billing_area.insert(END, "\nACTUAL PAYABLE DAYS\t\t\t\t\tTOTAL WORKING DAYS\t\t\t\t\tLOSS OF PAY DAYS\t\t\t\t\tDAYS PAYABLE")
    #     # self.billing_area.insert(END, "\n28.0\t\t\t\t\t28.0\t\t\t\t\t0.0\t\t\t\t\t28")
    #     # self.billing_area.insert(END, "\n\n=======================================================================================================================================================")
    #     self.billing_area.insert(END, "\n\nEARNINGS")
    #     self.billing_area.insert(END, "\nBasic\t\t\tConveyance Allowance\t\t\tHRA\t\t\tPerformance Bonus\t\t\tTotal Earnings(A)")
    #     self.billing_area.insert(END,f"\n{basic1}\t\t\t{convey_fee}\t\t\t{HRA}\t\t\t{performance_fee}\t\t\t{basic1+convey_fee+HRA+performance_fee}#")
    #     self.billing_area.insert(END, "\n\nCONTRIBUTIONS")
    #     self.billing_area.insert(END, "\nPF Employee\t\t\tESI Employee\t\t\tTotal Contributions(B)")
    #     self.billing_area.insert(END, f"\n{pf}\t\t\t{ESI}\t\t\t{pf+ESI}")
    #     self.billing_area.insert(END, "\n\nTAXES & DEDUCTIONS")
    #     self.billing_area.insert(END, "\nProfessional Tax\t\t\tTotal Deductions(C)")
    #     self.billing_area.insert(END, f"\n{tax}\t\t\t{tax}")
    #     self.billing_area.insert(END, "\n\n========================================================================================================")
    #     self.billing_area.insert(END, f"\n\nNet Salary Payable \t\t\t\t\t\t\t{basic-pf-tax-ESI}")
    #     self.billing_area.insert(END, "\n\n========================================================================================================")
    #     self.billing_area.configure(font='arial 10 bold')
    #     self.billing_area.configure(state=DISABLED)


    def emp_sal(self):
        con=sqlite3.connect(database="apollo.db")
        cur=con.cursor()
        cur.execute("SELECT * from sal_structure")
        row_sal=cur.fetchall()
        for sal_structure in row_sal:
            sal_basic =  (float(sal_structure[1]))*0.01
            print("sal_basic:",sal_basic)
            sal_hra = (float(sal_structure[2]))*0.01 
            print("sal_hra:",sal_hra)
            sal_coveyance_allowance = (float(sal_structure[3]))*0.01 
            print("sal_coveyance_allowance:",sal_coveyance_allowance)
            sal_performence_bonus = (float(sal_structure[5]))*0.01 
            print("sal_performence_bonus:",sal_performence_bonus)
            sal_pf = (float(sal_structure[6]))*0.01 
            print("sal_pf:",sal_pf)
            sal_esi = (float(sal_structure[7]))*0.01 
            print("sal_esi:",sal_esi)
            sal_tax = (float(sal_structure[8]))*0.01 
            print("sal_tax:",sal_tax)
            sal_medical_allowance = (float(sal_structure[4]))*0.01

        cur.execute("SELECT * from users where username LIKE '%"+str(self.search_user_sal.get())+"%'")
        row=cur.fetchall()
        
        for rows in row:
            emp_name = rows[1]
            emp_email = rows[3]
            emp_salary = rows[7]
            
            performance_fee = float(rows[7])*sal_performence_bonus
            basic1 =float(rows[7])*sal_basic
            basic =float(rows[7])
            convey_fee = (float(emp_salary))*sal_coveyance_allowance
            pf = (float(emp_salary))*sal_pf
            ESI = (float(emp_salary))*sal_esi

            contribution = (float(emp_salary))*0.13
            tax = (float(emp_salary))*sal_tax
            HRA = (float(emp_salary))*sal_hra
            
        self.billing_area.insert(END, "PAYSLIP")
        self.billing_area.insert(END, "\n\nAPOLLO MEDICAL ANJAIAH NAGAR HYDERBAD")
        self.billing_area.insert(END, f"\nName: {emp_name}")
        self.billing_area.insert(END, f"\nEmail: {emp_email}")
        self.billing_area.insert(END, "\n\nSALARY DETAILS")
        self.billing_area.insert(END, "\n\n========================================================================================================")
        # self.billing_area.insert(END, "\nACTUAL PAYABLE DAYS\t\t\t\t\tTOTAL WORKING DAYS\t\t\t\t\tLOSS OF PAY DAYS\t\t\t\t\tDAYS PAYABLE")
        # self.billing_area.insert(END, "\n28.0\t\t\t\t\t28.0\t\t\t\t\t0.0\t\t\t\t\t28")
        # self.billing_area.insert(END, "\n\n=======================================================================================================================================================")
        self.billing_area.insert(END, "\n\nEARNINGS")
        self.billing_area.insert(END, "\nBasic\t\t\tConveyance Allowance\t\t\tHRA\t\t\tPerformance Bonus\t\t\tTotal Earnings(A)")
        self.billing_area.insert(END,f"\n{basic1}\t\t\t{convey_fee}\t\t\t{HRA}\t\t\t{performance_fee}\t\t\t{basic1+convey_fee+HRA+performance_fee}#")
        self.billing_area.insert(END, "\n\nCONTRIBUTIONS")
        self.billing_area.insert(END, "\nPF Employee\t\t\tESI Employee\t\t\tTotal Contributions(B)")
        self.billing_area.insert(END, f"\n{pf}\t\t\t{ESI}\t\t\t{pf+ESI}")
        self.billing_area.insert(END, "\n\nTAXES & DEDUCTIONS")
        self.billing_area.insert(END, "\nProfessional Tax\t\t\tTotal Deductions(C)")
        self.billing_area.insert(END, f"\n{tax}\t\t\t{tax}")
        self.billing_area.insert(END, "\n\n========================================================================================================")
        self.billing_area.insert(END, f"\n\nNet Salary Payable \t\t\t\t\t\t\t{basic-pf-tax-ESI}")
        self.billing_area.insert(END, "\n\n========================================================================================================")
        self.billing_area.configure(font='arial 10 bold')
        self.billing_area.configure(state=DISABLED)


if __name__=='__main__':
    main()
    
