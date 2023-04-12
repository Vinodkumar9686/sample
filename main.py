from tkinter import *
from tkinter import END, BOTH, X, Y, BOTTOM, RIGHT
from tkinter import Entry, Text, LabelFrame, Toplevel, PhotoImage
from tkinter import VERTICAL, HORIZONTAL, Scrollbar, RIDGE, Frame, Canvas
from tkinter import DISABLED, Label, NORMAL, SUNKEN, GROOVE, Button, StringVar
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
import threading
import time

import ctypes
from ctypes import Structure, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, UINT, DWORD
import io
from tkinter.filedialog import askopenfilename

import smtplib
from email.message import EmailMessage
from configparser import ConfigParser

'''Read config file'''
parser = ConfigParser()
parser.read("configure.ini")
saved_database = parser.get('database', 'db')
saved_username = parser.get('admin', 'username')
saved_admin_name = parser.get('admin', 'admin_name')
saved_password = parser.get('admin', 'password')
saved_email = parser.get('admin', 'email')

logging.basicConfig(filename='apollo_log.log',
                    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


def main():
    root = Tk()
    app = Login_Window(root)
    root.mainloop()


class Database():
    try:
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
                active text,
                photo BLOB
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
            sql_queries = [sql_products, sql_edit_products,
                           sql_customer_datas,
                           sql_users, sql_users_sal,
                           sql_users_clockout, sql_admins,
                           sql_coupons, sql_revenue,
                           sql_revenue_edit, sql_sal_structure]
            for i in sql_queries:
                self.cur.execute(i)
                self.con.commit()

        def insert_income(self, date_time, day_date,
                          bill_number, total_sheet,
                          total_amount, tax, mrp_amount,
                          given_disscount_amount,
                          got_disscount_amount, profit_amount,
                          paid_amount, float_price):
            '''Inserts revenue data in Revenue table'''
            db_table = '''insert into Revenue values
                          (NULL,?,?,?,?,?,?,?,?,?,?,?,?)'''
            if self.cur.execute(db_table,
                                (date_time, day_date, bill_number,
                                 total_sheet,
                                 total_amount, tax, mrp_amount,
                                 given_disscount_amount,
                                 got_disscount_amount, profit_amount,
                                 paid_amount, float_price)):
                self.con.commit()
                logging.info('income history inserted successfully')

        def insert_income_edit(self, date_time, day_date,
                               bill_number, total_sheet,
                               total_amount, tax, mrp_amount,
                               given_disscount_amount,
                               got_disscount_amount, profit_amount,
                               paid_amount, float_price):
            '''Inserts data of finding revenue in revenue_edit table'''
            sql = '''insert into revenue_edit values
              (NULL,?,?,?,?,?,?,?,?,?,?,?,?)'''
            if self.cur.execute(sql,
                                (date_time, day_date, bill_number,
                                 total_sheet, total_amount, tax, mrp_amount,
                                 given_disscount_amount, got_disscount_amount,
                                 profit_amount, paid_amount, float_price)):
                self.con.commit()
                logging.info('income history inserted successfully')

        def insert_coupon(self, coupon_code, coupon_amount):
            '''Inserts coupons/disscounts in coupon table'''
            if self.cur.execute("insert into coupons values (NULL,?,?)",
                                (coupon_code, coupon_amount)):
                self.con.commit()
                logging.info('Coupon generated successfully')
            else:
                logging.error('Coupon not generated by admin')

        def insert_User_register(self, username, password,
                                 email, phone_no, address,
                                 active, salary):
            '''Inserts users data into users table'''
            if self.cur.execute('''insert into USERS values
                                (NULL,?,?,?,?,?,?,?)''',
                                (username, password, email, phone_no, address,
                                 active, salary)):
                self.con.commit()
                logging.info('User added successfully to the database')
            else:
                logging.error('User not added')

        def insert_sal_structure(self, basic_sal, hra,
                                 conveyance_allowance,
                                 medical_allowance,
                                 performance_bonus, PF,
                                 Esi, Tax):
            '''Inserts salary structure like basics,
                ESI etc into sal_structure table'''
            if self.cur.execute('''insert into sal_structure values
                                (NULL,?,?,?,?,?,?,?,?)''',
                                (basic_sal, hra, conveyance_allowance,
                                 medical_allowance,
                                 performance_bonus, PF, Esi, Tax)):
                self.con.commit()
                logging.info('Sal Structure added successfully')
            else:
                logging.error('Sal Structure not added')

        def insert_User_sal(self, username, clockin_date,
                            clockin_time, salary_per_day):
            '''Inserts users salary in users_sal table'''
            if self.cur.execute("insert into users_sal values (NULL,?,?,?,?)",
                                (username, clockin_date, clockin_time,
                                 salary_per_day)):
                self.con.commit()
                logging.info('User clocked in successfully')
            else:
                logging.error('User not clocked-in')

        def insert_User_Clockout(self, username, clockin_date,
                                 clockin_time, salary_per_day):
            '''Inserts users clock-out date and time in users_clockOut table'''
            if self.cur.execute('''insert into users_clockOut values
                                (NULL,?,?,?,?)''',
                                (username, clockin_date, clockin_time,
                                 salary_per_day)):
                self.con.commit()
            else:
                logging.error('User not clock-out')

        def insert_admin_register(self, username, password,
                                  email, phone_no, address,
                                  active):
            '''Inserts admins data in damins table'''
            filename = "images/a1.jpg"
            with open(filename, 'rb') as file:
                blobData = file.read()
            if self.cur.execute('''insert into admins values
                                (NULL,?,?,?,?,?,?,?)''',
                                (username, password, email,
                                 phone_no, address,
                                 active, blobData)):
                self.con.commit()
                logging.info('product added successfully to the database')
            else:
                logging.error('item not added')

        def insert(self, product_name, product_quantity,
                   product_mrp_price, product_details,
                   product_cgst, product_sgst,
                   product_purchase_price):
            '''Inserts products into products table'''
            if self.cur.execute('''insert into products values
                                (NULL,?,?,?,?,?,?,?)''',
                                (product_name, product_quantity,
                                 product_mrp_price,
                                 product_details, product_cgst,
                                 product_sgst,
                                 product_purchase_price)):
                self.con.commit()
                logging.info('product added successfully to the database')
            else:
                logging.error('item not added')

        def insert_to_edit_billing_area(self, items, quantity, price, Sheet):
            '''inserting into cart edit area'''
            sheet_no = 0
            sheet_no = sheet_no+(int(Sheet))
            total_price = 0
            total_price = total_price+(int(price)*int(Sheet))
            total_price = str(total_price)
            if self.cur.execute('''insert into edit_products values
                                (NULL,?,?,?,?)''',
                                (items, sheet_no, price, total_price)):
                self.con.commit()
                logging.info('item added successfully to the cart')
            else:
                logging.error('item not added to the cart')

        def insert_to_edit_area(self, items, Sheet, price,
                                tablet_details, CGST_Amount,
                                SGST_Amount, amount_purchased):
            '''inserting into cart edit area'''
            sheet_no = 0
            sheet_no = sheet_no+(int(Sheet))
            total_price = 0
            total_price = total_price+(float(price)*int(Sheet))
            total_price = str(total_price)
            disscount_price = 0
            abc = float(amount_purchased) * 0.01
            disscount_price = float(total_price) * float(abc)
            '''profit_price = float(total_price) - float(disscount_price)'''

            if self.cur.execute('''insert into edit_products values
                                (NULL,?,?,?,?,?,?,?,?,?)''',
                                (items, sheet_no, price, tablet_details,
                                 CGST_Amount, SGST_Amount,
                                 amount_purchased, total_price,
                                 disscount_price)):
                self.con.commit()
                logging.info('item added to the cart')
            else:
                logging.error('item not added to the cart')

        def insert_to_customer_data(self, phone, bill_no,
                                    items, quantity, price,
                                    total_price, tax, totalbill1,
                                    bill_date, username, CGST, SGST,
                                    coupon_disscount_total,
                                    matched_coupon, final_pay_bill_amount,
                                    float_price):
            '''Customer bill data stores'''
            cus_d = '''insert into customer_datas values
                    (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
            if self.cur.execute(cus_d,
                                (phone, bill_no, items, quantity,
                                 price, total_price, tax, totalbill1,
                                 bill_date, username, CGST, SGST,
                                 coupon_disscount_total, matched_coupon,
                                 final_pay_bill_amount, float_price)):
                self.con.commit()
                logging.info('Customer data and bill added successfully')
            else:
                logging.error('Customer data and bill not added')

        def fetch(self):
            ''' Fetch All Data from products'''
            self.cur.execute("SELECT * from products")
            rows = self.cur.fetchall()
            return rows

        def fetch_sal_structure(self):
            ''' Fetch All Data from sal_structure'''
            self.cur.execute("SELECT * from sal_structure")
            rows = self.cur.fetchall()
            return rows

        def fetch_cupon(self):
            ''' Fetch All Data from coupons table'''
            self.cur.execute("SELECT * from coupons")
            rows = self.cur.fetchall()
            return rows

        def fetch_user(self):
            ''' Fetch All Data from users table'''
            us_da = '''SELECT id, username, email, phone_no,
                    address, active, salary from users'''
            self.cur.execute(us_da)
            rows = self.cur.fetchall()
            return rows

        def fetch_admin(self):
            ''' Fetch All Data from admins table'''
            ad_da = '''SELECT id, username, email, phone_no,
                    address, active from admins'''
            self.cur.execute(ad_da)
            rows = self.cur.fetchall()
            return rows

        def edit_fetch(self):
            '''This method fetches data from cart'''
            self.cur.execute("SELECT * from edit_products")
            rows = self.cur.fetchall()
            return rows

        def edit_fetch_income(self):
            '''This method searches revenue from edit_revenue table'''
            self.cur.execute("SELECT * from revenue_edit")
            rows = self.cur.fetchall()
            return rows

        def find_income(self):
            '''This method searches revenue data from revenue table'''
            self.cur.execute("SELECT * from Revenue")
            rows = self.cur.fetchall()
            return rows

        def search_data(self):
            '''This method will search products from products table'''
            self.search_by = StringVar()
            self.search_txt = StringVar()
            if self.cur.execute("SELECT * from products where "
                                + str(self.search_by.get())
                                + " LIKE '%"
                                + str(self.search_txt.get()) + "%'"):
                rows = self.cur.fetchall()
                logging.info('Searched items successfully from database')
                return rows
            else:
                logging.error('Cannot searched items')

        def search_income(self, *args):
            '''This method will searches revenue from
                one date to another'''
            self.search_day = StringVar()
            self.income_amounts = StringVar()
            self.cur.execute("SELECT * from Revenue where "
                             + str(self.search_day.get())
                             + " LIKE '%"
                             + self.income_amounts.get() + "%'")
            rows = self.cur.fetchall()
            return rows

        def remove(self, id):
            '''Deletes products from products table'''
            if self.cur.execute("delete from products where id = ?",
                                (id,)):
                self.con.commit()
                logging.info('Product removed successfully from database')
            else:
                logging.error('item not removed from database')

        def remove_oneitem_edit_area(self, id):
            '''Deletes selected products data from cart'''
            if self.cur.execute("delete from edit_products where id = ?",
                                (id,)):
                self.con.commit()
                logging.info('item removed successfully from cart')
            else:
                logging.error('item not removed from cart')

        def remove_edit_area(self):
            '''Deletes all products data from cart after genrating bill'''
            if self.cur.execute("delete from edit_products"):
                self.con.commit()
                logging.info('item removed successfully from cart')
            else:
                logging.error('item not removed from cart')

        def remove_edit_income(self):
            '''Deletes revenue data after finding revenue'''
            if self.cur.execute("delete from revenue_edit"):
                self.con.commit()
                logging.info('item removed successfully from revenue_edit')
            else:
                logging.error('item not removed from revenue_edit')

        def remove_user(self, id):
            '''Delete a perticular users from users table'''
            if self.cur.execute("delete from users where id = ?", (id,)):
                self.con.commit()
                logging.info('Product removed successfully from database')
            else:
                logging.error('item not removed from database')

        def remove_admin(self, id):
            '''Delete a perticular admin from admins table'''
            if self.cur.execute("delete from admins where id = ?", (id,)):
                self.con.commit()
                logging.info('Product removed successfully from database')
            else:
                logging.error('item not removed from database')

        def remove_coupons(self, id):
            '''Delete a perticular coupons from coupons table'''
            if self.cur.execute("delete from coupons where id = ?", (id,)):
                self.con.commit()
                logging.info('Product removed successfully from database')
            else:
                logging.error('item not removed from database')

        def remove_sal_structure(self, id):
            '''Delete a perticular remove_salStructure from
                remove_sal_structure table'''
            if self.cur.execute("delete from sal_structure where id = ?",
                                (id,)):
                self.con.commit()
                logging.info('sal_tructure removed successfully from database')
            else:
                logging.error('sal_tructure not removed from database')

        def update(self, product_name, product_quantity,
                   product_mrp_price, product_details,
                   product_cgst, product_sgst,
                   product_purchase_price, id):
            '''Update a perticular products from products table'''
            if self.cur.execute('''update products set product_name = ?,
                                product_quantity = ?, product_mrp_price = ?,
                                product_details = ?, product_cgst = ?,
                                product_sgst = ?,
                                product_purchase_price = ? where id = ?''',
                                (product_name, product_quantity,
                                 product_mrp_price,
                                 product_details, product_cgst, product_sgst,
                                 product_purchase_price, id)):
                self.con.commit()
                logging.info('Product updated successfully from database')
            else:
                logging.error('Product not updated from database')

        def update_quantity(self, product_quantity, id):
            '''Updates products details'''
            if self.cur.execute('''update products set  product_quantity = ?
                                where id = ?''',
                                (product_quantity, id)):
                self.con.commit()

        def update_user(self, username, password, email,
                        phone_no, address, active, salary, id):
            '''Updates users records'''
            if self.cur.execute('''update users set username = ?,
                                password = ?, mail = ?, phone_no = ?,
                                address = ?, active = ?,
                                salary = ? where id = ?''',
                                (username, password, email, phone_no,
                                 address, active, salary, id)):
                self.con.commit()
                logging.info('User updated successfully')
            else:
                logging.error('User not updated from database')

        def update_sal_structure(self, basic_sal, hra,
                                 conveyance_allowance, medical_allowance,
                                 performance_bonus, PF, Esi, Tax, id):
            '''Updates users salary structure like basics, ESI etc'''
            if self.cur.execute('''update sal_structure set basic_sal = ?,
                                hra = ?,
                                conveyance_allowance = ?,
                                medical_allowance = ?,
                                performance_bonus = ?, PF = ?, Esi = ?,
                                Tax = ? where id = ?''',
                                (basic_sal, hra, conveyance_allowance,
                                 medical_allowance, performance_bonus,
                                 PF, Esi, Tax, id)):
                self.con.commit()
                logging.info('Updated sal structure successfully')
            else:
                logging.error('Sal structure not updated')

        def update_user_edit(self, password, email, phone_no,
                             address, salary, id):
            '''Updates users data'''
            if self.cur.execute('''update users set password = ?,
                                email = ?, phone_no = ?,
                                address = ?, salary = ? where id = ?''',
                                (password, email, phone_no, address,
                                 salary, id)):
                self.con.commit()
                logging.info('User updated successfully from database')
            else:
                logging.error('User not updated from database')

        def update_admin(self, username, password, email,
                         phone_no, address, active, id):
            '''Updates admins data'''
            self.cur.execute("SELECT * from admins where username LIKE '%"
                             + str(b.get()) + "%'") ## noqa
            record = self.cur.fetchall()
            for row in record:
                photo = row[7]
            if self.cur.execute('''update admins set username = ?,
                                password = ?, email = ?,
                                phone_no = ?, address = ?,
                                active = ?, photo = ? where id = ?''',
                                (username, password, email, phone_no,
                                 address, active, photo, id)):
                self.con.commit()
                logging.info('Admin updated successfully from database')
            else:
                logging.error('Admin not updated from database')

        def update_to_edit_area(self, items, number_of_sheets,
                                per_sheet_price, id):
            '''This method wil updates cart product details'''
            total_price = 0
            total_price = (total_price + (int(number_of_sheets) *
                                          int(per_sheet_price)))
            total_price = str(total_price)

            if self.cur.execute('''update edit_products set items = ?,
                                number_of_sheets = ?,
                                per_sheet_price = ?, total_price = ?
                                where id = ?''',
                                (items, number_of_sheets,
                                 per_sheet_price, total_price, id)):
                self.con.commit()
                logging.info('item updated successfully from cart')
            else:
                logging.error('item not updated from cart')
    except Exception as e:
        logging.error("Error handled by database class:", e)


db = Database(saved_database)


class Login_Window():
    '''This class is for login page'''
    def __init__(self, master):
        self.master = master
        self.master.title("Medical billing login page")
        self.master.geometry("1820x750")
        self.master.config(bg='#202A44')
        self.user_name = StringVar()
        self.password = StringVar()
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        cursor.execute("SELECT username from admins")
        user_name = cursor.fetchall()
        usr_na = (saved_admin_name,)

        cursor.execute("SELECT username from users")
        user_name12 = cursor.fetchall()
        usr_na1 = (saved_username,)

        if usr_na in user_name and usr_na1 in user_name12:
            logging.error(" Default user already exist")
        else:
            with open('images/a1.jpg', 'rb') as file:
                blobData = file.read()
            cursor.execute("insert into admins values (NULL,?,?,?,?,?,?,?)",
                           (saved_admin_name, saved_password, saved_email,
                            '7529527927', 'Bangalore HSR Layout', 'Yes',
                            blobData))
            cursor.execute("insert into users values (NULL,?,?,?,?,?,?,?)",
                           (saved_username, saved_password, saved_email,
                            '7529527927', 'Bangalore HSR Layout', 'Yes', 0))
            cursor.execute("insert into coupons values (NULL,?,?)",
                           ('disscount', 0))
            connection.commit()
            logging.info('Default user added')

        img = Image.open('images/medical.webp')
        logo = img.resize((1100, 750), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.master, image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=750)

        self.frame1 = tkinter.Frame(self.master, bg='light blue')
        self.frame1.place(x=130, y=20, width=790, height=80)
        space = (9 * " ")
        lblName = Label(master=self.frame1,
                        text=f"{space} WELCOME TO APOLLO MEDICAL",
                        font=("Calibri", 34), bg="powder blue",
                        fg="black")
        lblName.grid(row=0, column=0, padx=10, pady=10)

        self.frame = tkinter.Frame(self.master, bg='powder blue')
        self.frame.place(x=1111, y=0, width=720, height=750)

        lblName = Label(master=self.frame, text="",
                        font=("Calibri", 10),
                        bg="powder blue", fg="black")
        lblName.grid(row=0, column=0, padx=10, pady=10)
        lblName = Label(master=self.frame, text="LOGIN",
                        font=("Calibri", 32, 'bold'),
                        bg="powder blue", fg="black")
        lblName.grid(row=1, column=0, padx=10, pady=10)
        lblName = Label(master=self.frame, text="",
                        font=("Calibri", 10),
                        bg="powder blue", fg="black")
        lblName.grid(row=2, column=0, padx=10, pady=10)
        space1 = (18*'_')
        lblName = Label(master=self.frame,
                        text=f"{space1}User Name{space1}",
                        font=("Calibri", 10), bg="powder blue",
                        fg="black")
        lblName.grid(row=3, column=0, padx=10, pady=10)

        global user_name1
        user_name1 = customtkinter.CTkEntry(master=self.frame,
                                            placeholder_text="Username",
                                            border_color="black",
                                            textvariable=self.user_name,
                                            text_font=('Helvetica', 18),
                                            width=300, height=50,
                                            border_width=2, corner_radius=10)
        user_name1.grid(row=4, column=0)

        lblName = Label(master=self.frame, text=f"{space1}Password{space1}",
                        font=("Calibri", 10), bg="powder blue", fg="black")
        lblName.grid(row=5, column=0, padx=10, pady=10)

        password1 = customtkinter.CTkEntry(master=self.frame,
                                           placeholder_text="Password",
                                           border_color="black",
                                           textvariable=self.password,
                                           text_font=('Helvetica', 18),
                                           width=300, height=50, show="*",
                                           border_width=2, corner_radius=10)
        password1.grid(row=6, column=0, padx=10, pady=10)

        lblName = Label(master=self.frame, text="", font=("Calibri", 10),
                        bg="powder blue", fg="black")
        lblName.grid(row=7, column=0, padx=10, pady=10)

        button = customtkinter.CTkButton(master=self.frame, width=300,
                                         height=50, border_width=0,
                                         fg_color="Blue",
                                         text_color='white',
                                         corner_radius=8,
                                         text="Log In",
                                         text_font=('Helvetica', 14),
                                         command=lambda: [self.button_event()])
        button.grid(row=8, column=0, padx=10, pady=10)

        self.frame_auto_text = tkinter.Frame(self.master, bg='powder blue')
        self.frame_auto_text.place(x=1111, y=500, width=400, height=25)

        self.canvas = Canvas(self.frame_auto_text, bg='powder blue')
        self.canvas.pack(fill=BOTH, expand=1)
        text_var = "Please provide your user name and password"
        self.text = self.canvas.create_text(0, -2000, text=text_var,
                                            font=('Times New Roman',
                                                  14, 'bold'),
                                            fill='Red',
                                            tags=("marquee",),
                                            anchor='w')
        x1, y1, x2, y2 = self.canvas.bbox("marquee")
        width = x2 - x1
        height = y2 - y1
        self.canvas['width'] = width
        self.canvas['height'] = height
        self.fps = 70
        self.animation_text()

        t1 = threading.Thread(target=self.timer_set)
        t1.start()

    def timer_set(self):
        '''This method helps to automatic logout if application
            is inactive till 30 minutes'''
        try:
            class LastInputInfo(Structure, Login_Window):
                _fields_ = [("cbSize", UINT), ("dwTime", DWORD)]

            def _getLastInputTick() -> int:
                prototype = WINFUNCTYPE(BOOL, POINTER(LastInputInfo))
                paramflags = ((1, "lastinputinfo"), )
                c_GetLastInputInfo = prototype(("GetLastInputInfo",
                                                ctypes.windll.user32),
                                               paramflags)

                last_in = LastInputInfo()
                last_in.cbSize = ctypes.sizeof(LastInputInfo)
                assert 0 != c_GetLastInputInfo(last_in)
                return last_in.dwTime

            def _getTickCount() -> int:
                prototype = WINFUNCTYPE(DWORD)
                paramflags = ()
                c_GetTickCount = prototype(("GetTickCount",
                                            ctypes.windll.kernel32),
                                           paramflags)
                return c_GetTickCount()

            def seconds_since_last_input():
                seconds_since_input = ((_getTickCount() -
                                        _getLastInputTick()) / 1000)
                return seconds_since_input

            def autologoutdetection():
                while True:
                    time.sleep(1)
                    last_input = seconds_since_last_input()
                    if last_input > 5:
                        logging.info("Automatic close due to away from system")
                        self.exit_login()
            autologoutdetection()

        except Exception as ex:
            logging.debug(f"Error handled by timer_set method:{ex}")

    def animation_text(self):
        '''This method helps to display animation text'''
        x1, y1, x2, y2 = self.canvas.bbox("marquee")
        if (x2 < 0 or y1 < 0):
            x1 = self.canvas.winfo_width()
            y1 = self.canvas.winfo_height()//2
            self.canvas.coords("marquee", x1, y1)
        else:
            self.canvas.move("marquee", -2, 0)
        self.canvas.after(1000//self.fps, self.animation_text)

    def exit_login(self):
        '''Destroys login window'''
        logging.info('Destroyed Main Window Successfully')
        self.master.destroy()

    def button_event(self):
        '''This method validates login credentials and according
            to credentials opens pages like user and admin pages'''
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        cursor.execute("SELECT * from users")
        results = cursor.fetchall()
        self.a = StringVar()

        for result in results:
            if (self.user_name.get() == result[1]
                    and self.password.get() == result[2]
                    and result[6] == 'Yes'):
                global a, ai, user_pass_edit, user_email_edit
                global user_ph_no, user_address_edit, user_admin_edit
                global user_name_edit, user_password_edit, user_salary_edit

                a = self.user_name
                user_pass_edit = self.password
                user_name_edit = result[1]
                user_password_edit = result[2]
                user_email_edit = result[3]
                user_ph_no = result[4]
                user_address_edit = result[5]
                user_admin_edit = result[6]
                user_salary_edit = result[7]
                ai = result[0]
                logging.info('Login done by users successfully')
                User_Window(self.master)
            else:
                connection = sqlite3.connect(saved_database)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM admins where username LIKE '%"
                               + str(self.user_name.get()) + "%'")
                results = cursor.fetchall()
                for result in results:
                    global b, admin_id
                    b = self.user_name
                    admin_id = result[0]
                    if (self.user_name.get() == result[1]
                            and self.password.get() == result[2]
                            and result[6] == 'Yes'):
                        logging.info('Login done by admins successfully')
                        Super_Admin_Window(self.master)

    def new_window(self):
        '''This method redirects super admin page'''
        self.newWindow = Toplevel(self.master)
        self.app = Super_Admin_Window(self.newWindow)

    def new_user_window(self):
        '''This method will redirects users page'''
        self.newWindow = Toplevel(self.master)
        self.app = User_Window(self.newWindow)

    def new_usr_data(self):
        '''This method will redirects user register page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_user_register(self.newWindow)

    def edit_user_d(self):
        '''This method will redirects user edit page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_user_edit(self.newWindow)

    def coupon_data(self):
        '''This method will redirects coupons page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_coupon_edit(self.newWindow)

    def income_windw(self):
        '''This method will redirects income/revenue page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_income(self.newWindow)

    def add_pro_win(self):
        '''This methods redirects add products page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_add_products(self.newWindow)

    def adm_bill_ser(self):
        '''This method redirects bill search page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_Bill_Search(self.newWindow)

    def emp_salary(self):
        '''This method redirects employee salary slip'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_emp(self.newWindow)

    def emp_activity(self):
        '''This method redirects user activity page'''
        self.newWindow = Toplevel(self.master)
        self.app = Window_User_Activity(self.newWindow)


class Super_Admin_Window(Database, Login_Window):
    '''This class redirect super admin page'''
    db = Database(saved_database)

    def __init__(self, master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("1920x1080+0+0")
        self.master.config(bg='#2c3e50')

        self.entries_frame_color = Frame(self.master, bg="#202A44")
        self.entries_frame_color.place(x=0, y=0, width=1920, height=1080)

        img = Image.open('images/a2.webp')
        logo = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.master, image=logo)
        logo_label.image = logo
        logo_label.place(width=1920, height=1080)

        date_timing = dt.datetime.now()
        date_time_login = date_timing.strftime("%H:%M:%S:%p:%A")
        self.entries_frame1 = Frame(self.master, bg="#535c68")
        self.entries_frame1.place(x=0, y=0, width=457, height=935)

        self.add_image()

        '''Empty'''
        self.lblAdmin = Label(self.entries_frame1, text="",
                              font=("Times new roman", 18, 'bold'),
                              bg="#535c68", fg="white")
        self.lblAdmin.grid(row=0, column=0, padx=10, pady=100, sticky="w")

        self.bt = customtkinter.CTkButton(self.entries_frame1,
                                          width=18, height=30,
                                          border_width=0,
                                          fg_color="Sky blue",
                                          text_color="black",
                                          corner_radius=18,
                                          text="Edit Pic",
                                          text_font=('Times new roman',
                                                     18, 'bold'),
                                          command=lambda: [self.e_u_p()])
        self.bt.grid(row=1, column=0, padx=2)

        self.lblAdmin = Label(self.entries_frame1, textvariable=b,
                              font=("Times new roman", 22, 'bold'),
                              bg="#535c68", fg="white")
        self.lblAdmin.grid(row=2, column=0, padx=10)

        label = Label(self.entries_frame1, text=f"{date_time_login}",
                      font=("Times new roman", 18,
                            'bold'), bg="white", fg="black")
        label.grid(row=3, column=0, padx=10, pady=10)

        self.lblAdmin = Label(self.entries_frame1, text="",
                              font=("Times new roman", 18, 'bold'),
                              bg="#535c68", fg="white")
        self.lblAdmin.grid(row=4, column=1, padx=10, pady=150, sticky="w")

        self.bt = customtkinter.CTkButton(self.entries_frame1,
                                          width=18, height=30,
                                          border_width=0,
                                          fg_color="red",
                                          text_color="white",
                                          corner_radius=18,
                                          text="Logout",
                                          text_font=('Times new roman',
                                                     18, 'bold'),
                                          command=lambda: [self.exit()])
        self.bt.grid(row=5, column=0, padx=2, sticky="w")

        self.entries_frame_label = Frame(self.master, bg="sky blue")
        self.entries_frame_label.place(x=470, y=10, width=1075, height=70)
        title = Label(self.entries_frame_label,
                      text="APOLLO MEDICAL HITECH-CITY GACHIBOWLI HYDERABAD",
                      font=("Times new roman", 24, "bold"),
                      bg="sky blue", fg="black")
        title.grid(row=0, columnspan=2, sticky="w")

        self.entries_frame = Frame(self.master, bg="sky blue")
        self.entries_frame.place(x=600, y=150, width=820, height=460)

        photo_add_cart = PhotoImage(file=r"images/cart.png").subsample(4, 4)
        self.bt = customtkinter.CTkButton(self.entries_frame,
                                          width=18, height=30,
                                          border_width=0,
                                          corner_radius=0,
                                          fg_color="green",
                                          text_color="white",
                                          image=photo_add_cart,
                                          text="Add Product",
                                          text_font=('times new roman',
                                                     14, 'bold'),
                                          command=lambda: [self.add_pro_win()])
        self.bt.grid(row=0, column=0, padx=20, pady=30, sticky="w")
        photoimage_user = PhotoImage(file=r"images/user.png").subsample(4, 4)
        self.b = customtkinter.CTkButton(self.entries_frame,
                                         width=18, height=30,
                                         border_width=0,
                                         corner_radius=0,
                                         fg_color="green",
                                         text_color="white",
                                         image=photoimage_user,
                                         text="Add User",
                                         text_font=('times new roman',
                                                    14, 'bold'),
                                         command=lambda: [self.new_usr_data()])
        self.b.grid(row=0, column=1, padx=20, pady=30, sticky="w")

        photo_coupon = PhotoImage(file=r"images/coupons.png").subsample(4, 4)
        self.bu = customtkinter.CTkButton(self.entries_frame, width=18,
                                          height=30, border_width=0,
                                          corner_radius=0,
                                          fg_color="green",
                                          text_color="white",
                                          image=photo_coupon,
                                          text="Disscount%",
                                          text_font=('times new roman',
                                                     14, 'bold'),
                                          command=lambda: [self.coupon_data()])
        self.bu.grid(row=0, column=2, padx=20, pady=30, sticky="w")
        '''income'''
        photoimage = PhotoImage(file=r"images/revenuee.png").subsample(4, 4)
        self.b = customtkinter.CTkButton(self.entries_frame,
                                         width=18, height=30,
                                         border_width=0,
                                         corner_radius=0,
                                         fg_color="green",
                                         text_color="white",
                                         image=photoimage,
                                         text="Revenue ",
                                         text_font=('Times new roman',
                                                    14, 'bold'),
                                         command=lambda: [self.income_windw()])
        self.b.grid(row=1, column=1, padx=20, pady=30, sticky="w")
        photo_search = PhotoImage(file=r"images/search.png").subsample(4, 4)
        self.b = customtkinter.CTkButton(self.entries_frame, width=18,
                                         height=30, border_width=0,
                                         corner_radius=0,
                                         fg_color="green",
                                         text_color="white",
                                         image=photo_search,
                                         text="Bill History ",
                                         text_font=('Times new roman',
                                                    14, 'bold'),
                                         command=lambda: [self.adm_bill_ser()])
        self.b.grid(row=1, column=0, padx=30, pady=20, sticky="w")
        photo_sal = PhotoImage(file=r"images/emp sal.png").subsample(4, 4)
        self.bu = customtkinter.CTkButton(self.entries_frame, width=18,
                                          height=30, border_width=0,
                                          corner_radius=0,
                                          fg_color="green",
                                          text_color="white",
                                          image=photo_sal,
                                          text="Emp Salary",
                                          text_font=('Times new roman',
                                                     14, 'bold'),
                                          command=lambda: [self.emp_salary()])
        self.bu.grid(row=1, column=2, padx=20, pady=30, sticky="w")

        photo_sal = PhotoImage(file=r"images/emp sal.png").subsample(4, 4)
        self.b = customtkinter.CTkButton(self.entries_frame, width=18,
                                         height=30, border_width=0,
                                         corner_radius=0,
                                         fg_color="green",
                                         text_color="white",
                                         image=photo_sal,
                                         text="Emp Activity",
                                         text_font=('Times new roman',
                                                    14, 'bold'),
                                         command=lambda: [self.emp_activity()])
        self.b.grid(row=2, column=1, padx=20, pady=30, sticky="w")

    def add_image(self):
        '''This method adds profile pic'''
        try:
            connection = sqlite3.connect(saved_database)
            cursor = connection.cursor()
            cursor.execute("SELECT * from admins where username LIKE '%"
                           + str(b.get()) + "%'")
            record = cursor.fetchall()
            for row in record:
                photo = row[7]
                fp = io.BytesIO(photo)
                img = Image.open(fp)
            logo = img.resize((150, 150), Image.Resampling.LANCZOS)
            logo = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.entries_frame1, imag=logo)
            logo_label.image = logo
            logo_label.place(x=50, y=50, width=150, height=150)
        except Exception as e:
            logging.info(f"Error: add image: {e}")

    def e_u_p(self):
        '''This method will edit profile pic'''
        def convertToBinaryData(filename):
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData

        def insertBLOB(photo):
            '''This method inserts blob data to admins table'''
            try:
                sqliteConnection = sqlite3.connect(saved_database)
                cursor = sqliteConnection.cursor()
                sqlite_insert_blob_query = """Update admins set
                                            photo=? where id = ?"""
                empPhoto = convertToBinaryData(photo)
                data_tuple = (empPhoto, admin_id)
                cursor.execute(sqlite_insert_blob_query, data_tuple)
                sqliteConnection.commit()
                logging.info("Image updated as a BLOB into a table")
                cursor.close()
                messagebox.showinfo("Success", "Profile Image Updated")

            except sqlite3.Error as error:
                logging.error("Failed to insert blob data", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()

        filename = askopenfilename()
        insertBLOB(filename)

    def exit(self):
        '''This method exit from admin page'''
        if messagebox.askyesno('Exit', 'Do you really want to exit'):
            self.master.destroy()
            logging.info('Exited Successfully')


class User_Window(Database, Login_Window):
    '''This class redirects user page'''
    db = Database(saved_database)

    def __init__(self, master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("1920x1080+0+0")
        self.master.config(bg='#2c3e50')
        self.items = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.search_bill = StringVar()
        self.search_by1 = StringVar()
        self.Total_price = StringVar()
        self.total_price = StringVar()
        self.user_change_pass = StringVar()
        self.c_phone = StringVar()
        self.bill_no = StringVar()
        self.coupons = StringVar()
        self.coupon_total_pay = StringVar()
        self.tax2 = StringVar()
        self.totalbill = StringVar()
        self.total_quantity = StringVar()
        self.Sheet = StringVar()
        self.tablet_details = StringVar()
        self.user_name = StringVar()
        self.password = StringVar()
        self.SGST_Amount = StringVar()
        self.CGST_Amount = StringVar()
        self.amount_purchased = StringVar()
        self.pay_amount = StringVar()

        self.entries_frame_main = Frame(self.master, bg="black")
        self.entries_frame_main.place(x=0, y=0, width=1920, height=1080)

        self.entries_frame = Frame(self.master, bg="sky blue")
        self.entries_frame.place(x=0, y=0, width=975, height=225)

        '''login display'''
        self.entries_frame1 = Frame(self.master, bg="sky blue")
        self.entries_frame1.place(x=986, y=0, width=557, height=135)

        self.lblAdmin = Label(self.entries_frame1, text="Welcome",
                              font=("Times new roman", 18, 'bold'),
                              bg="sky blue", fg="black")
        self.lblAdmin.grid(row=0, column=0, padx=1, sticky="w")

        self.lblAdmin = Label(self.entries_frame1,
                              textvariable=a,
                              font=("Times new roman", 18, 'bold'),
                              bg="sky blue", fg="black")
        self.lblAdmin.grid(row=0, column=1, padx=1, sticky="w")
        '''Empty'''
        self.lblAdmin = Label(self.entries_frame1, text="",
                              font=("Times new roman", 18, 'bold'),
                              bg="sky blue", fg="black")
        self.lblAdmin.grid(row=1, column=0, padx=1, sticky="w")
        self.btn = customtkinter.CTkButton(self.entries_frame1,
                                           width=12,
                                           height=30,
                                           border_width=0,
                                           fg_color="red",
                                           text_color="White",
                                           corner_radius=8,
                                           text="Logout",
                                           text_font=('Helvetica', 12),
                                           command=lambda: [self.exit()])
        self.btn.grid(row=2, column=1, padx=10)

        self.b = customtkinter.CTkButton(self.entries_frame1,
                                         width=12,
                                         height=30,
                                         border_width=0,
                                         fg_color="red",
                                         text_color="White",
                                         corner_radius=8,
                                         text="Clockin",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.track_loc(),
                                                          self.clockin()])
        self.b.grid(row=2, column=2, padx=10)

        self.b = customtkinter.CTkButton(self.entries_frame1,
                                         width=12,
                                         height=30,
                                         border_width=0,
                                         fg_color="red",
                                         text_color="White",
                                         corner_radius=8,
                                         text="ClockOut",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.clockOut()])
        self.b.grid(row=2, column=3, padx=10)

        self.b = customtkinter.CTkButton(self.entries_frame1,
                                         width=12,
                                         height=30,
                                         border_width=0,
                                         fg_color="green",
                                         text_color="White",
                                         corner_radius=8,
                                         text="Edit profile",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.edit_user_d()])
        self.b.grid(row=2, column=0, padx=10)
        self.title = Label(self.entries_frame, text="BILLING SYSTEM",
                           font=("times new roman", 14, "bold"),
                           bg="sky blue", fg="black")
        self.title.grid(row=0, columnspan=2, padx=5,
                        pady=5, sticky="w")

        self.lblName = Label(self.entries_frame, text="Product_Name",
                             font=("times new roman", 12, 'bold'),
                             bg="sky blue", fg="black")
        self.lblName.grid(row=1, column=0, pady=5, sticky="w")
        self.txtName = Entry(self.entries_frame, textvariable=self.items,
                             font=("times new roman", 12, 'bold'), bd=7,
                             bg="sky blue",
                             relief=SUNKEN, width=15)
        self.txtName.grid(row=1, column=1, pady=5, sticky="w")
        self.txtName.config(state=DISABLED)

        self.lblMrp_Price = Label(self.entries_frame, text="Product_MRP_Price",
                                  font=("times new roman", 12, 'bold'),
                                  bg="sky blue", fg="black")
        self.lblMrp_Price.grid(row=2, column=0, pady=5, sticky="w")
        self.txtMrp_Price = Entry(self.entries_frame, textvariable=self.price,
                                  fon=("times new roman", 12, 'bold'), bd=7,
                                  relief=SUNKEN, width=15)
        self.txtMrp_Price.grid(row=2, column=1, pady=5, sticky="w")
        self.txtMrp_Price.config(state=DISABLED)

        self.lblQuantity = Label(self.entries_frame, text="Product_Quantity",
                                 font=("times new roman", 12, 'bold'),
                                 bg="sky blue", fg="black")
        self.lblQuantity.grid(row=3, column=0, pady=5, sticky="w")
        self.txtQuantity = Entry(self.entries_frame,
                                 textvariable=self.quantity,
                                 font=("times new roman", 12, 'bold'),
                                 bd=7, relief=SUNKEN, width=15)
        self.txtQuantity.grid(row=3, column=1, pady=5, sticky="w")
        self.txtQuantity.config(state=DISABLED)

        self.lblamount_purchased = Label(self.entries_frame,
                                         text="Purchased_disscount%",
                                         font=("times new roman", 12, 'bold'),
                                         bg="sky blue", fg="black")
        self.lblamount_purchased.grid(row=1, column=2, pady=5, sticky="w")
        self.txtamount_purchased = Entry(self.entries_frame,
                                         textvariable=self.amount_purchased,
                                         font=("times new roman", 12, 'bold'),
                                         bd=7,
                                         relief=SUNKEN, width=15)
        self.txtamount_purchased.grid(row=1, column=3, pady=5, sticky="w")
        self.txtamount_purchased.config(state=DISABLED)

        self.lblCGST = Label(self.entries_frame, text="CGST%",
                             font=("times new roman", 12, 'bold'),
                             bg="sky blue", fg="black")
        self.lblCGST.grid(row=2, column=2, pady=5, sticky="w")
        self.txtCGST = Entry(self.entries_frame, textvariable=self.CGST_Amount,
                             font=("times new roman", 12, 'bold'), bd=7,
                             relief=SUNKEN, width=15)
        self.txtCGST.grid(row=2, column=3, pady=5, sticky="w")
        self.txtCGST.config(state=DISABLED)

        self.lblSGST = Label(self.entries_frame, text="SGST%",
                             font=("times new roman", 12, 'bold'),
                             bg="sky blue", fg="black")
        self.lblSGST.grid(row=3, column=2, pady=5, sticky="w")
        self.txtSGST = Entry(self.entries_frame,
                             textvariable=self.SGST_Amount,
                             font=("times new roman", 12, 'bold'),
                             bd=7, relief=SUNKEN, width=15)
        self.txtSGST.grid(row=3, column=3, pady=5, sticky="w")
        self.txtSGST.config(state=DISABLED)
        '''Sheet'''
        self.lblSheet = Label(self.entries_frame,
                              text="Strip/Sheet",
                              font=("times new roman", 12, 'bold'),
                              bg="sky blue", fg="black")
        self.lblSheet.grid(row=4, column=2, padx=1, sticky="w")

        self.txtSheet = Entry(self.entries_frame,
                              textvariable=self.Sheet,
                              font=("times new roman", 12, 'bold'),
                              bd=7, relief=SUNKEN, width=15)
        self.txtSheet.grid(row=4, column=3, sticky="w")

        self.lblTablet_details = Label(self.entries_frame,
                                       text="Tablet_details",
                                       font=("times new roman", 12, 'bold'),
                                       bg="sky blue", fg="black")
        self.lblTablet_details.grid(row=4, column=0, sticky="w")
        self.txtTablet_deatails = Entry(self.entries_frame,
                                        textvariable=self.tablet_details,
                                        font=("Calibri", 12, 'bold'),
                                        bd=7, relief=SUNKEN, width=15)
        self.txtTablet_deatails.grid(row=4, column=1, sticky="w")
        self.txtTablet_deatails.config(state=DISABLED)

        '''Table Frame (displaying data from data base)'''
        tree_frame = Frame(self.master, bg="sky blue")
        tree_frame.place(x=0, y=235, width=535, height=370)
        lbl_search = Label(tree_frame, text="Search Products", bg="green",
                           fg="white", font=("times new roman", 14, "bold"))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        txt_Search = Entry(tree_frame, textvariable=self.search_txt,
                           width=20,
                           font=("times new roman", 10, "bold"),
                           bd=5, relief=GROOVE)
        txt_Search.grid(row=0, column=2, padx=20, pady=10, sticky="w")
        txt_Search.bind("<Key>", self.search)

        '''Table Show Data'''
        Table_Frame = Frame(tree_frame, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=70, width=515, height=300)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table = ttk.Treeview(Table_Frame,
                                          columns=("ProductID",
                                                   "Products",
                                                   "Quantity",
                                                   "MRP_Price",
                                                   "product_details",
                                                   "CGST",
                                                   "SGST",
                                                   "Purchase_price"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)

        self.billing_table.heading("ProductID", text="ProductID")
        self.billing_table.heading("Products", text="Products")
        self.billing_table.heading("Quantity", text="quantity")
        self.billing_table.heading("MRP_Price", text="MRP_Price")
        self.billing_table.heading("product_details", text="product_details")
        self.billing_table.heading("CGST", text="CGST")
        self.billing_table.heading("SGST", text="SGST")
        self.billing_table.heading("Purchase_price", text="Purchase_price")
        self.billing_table['show'] = 'headings'
        self.billing_table.column("ProductID", width=2)
        self.billing_table.column("Products", width=100)
        self.billing_table.column("Quantity", width=10)
        self.billing_table.column("MRP_Price", width=20)
        self.billing_table.column("product_details", width=20)
        self.billing_table.column("CGST", width=10)
        self.billing_table.column("SGST", width=20)
        self.billing_table.column("Purchase_price", width=20)
        self.billing_table.pack(fill=BOTH, expand=1)
        self.billing_table.bind("<ButtonRelease-1>", self.getData)

        '''displaying bill area and dimenions'''
        '''Customer Details'''
        F1 = LabelFrame(self.master, bd=10, relief=GROOVE,
                        text="Customer Details",
                        font=("times new roman", 10, "bold"),
                        fg="black", bg="sky blue")
        F1.place(x=980, y=136, width=550)

        self.cphn_lbl = Label(F1, text="Phone No.", bg="sky blue",
                              fg="black",
                              font=("times new roman",
                                    15, "bold")).grid(row=0,
                                                      column=2,
                                                      padx=20,
                                                      pady=5)
        self.txtPhone = Entry(F1, width=15, font="arial 15", bd=7,
                              relief=SUNKEN,
                              textvariable=self.c_phone).grid(row=0,
                                                              column=3,
                                                              pady=5,
                                                              padx=10)

        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.master, bg="sky blue",
                                  bd=10, relief=GROOVE)
        self.billing_area.place(x=980, y=214, width=550, height=470)
        self.billing_tiltle = Label(self.billing_area, text="Bill Area",
                                    font="arial 15 bold",
                                    fg="black", bg="sky blue",
                                    bd=7,
                                    relief=GROOVE).pack(fill=X)

        scroll_y = Scrollbar(self.billing_area, orient=VERTICAL)
        self.billing_area = Text(self.billing_area,
                                 yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH, expand=1)
        self.welcome_default1()

        '''Bill Menu'''
        self.button_frame = LabelFrame(self.master, bg="sky blue",
                                       bd=10, relief=GROOVE)
        self.button_frame.place(x=980, y=685, width=550, height=100)

        '''Total Calculate Menue'''
        self.button_Total_frame = LabelFrame(self.master, bg="sky blue",
                                             bd=10, relief=GROOVE)
        self.button_Total_frame.place(x=0, y=630, width=975, height=157)

        self.cphn_lbl1 = Label(self.button_Total_frame,
                               text="Total", bg="sky blue", fg="black",
                               font=("times new roman",
                                     12, "bold")).grid(row=0,
                                                       column=2,
                                                       padx=20.0,
                                                       pady=5)
        self.cphn_ibl1 = Entry(self.button_Total_frame,
                               textvariable=self.Total_price, width=15,
                               font="arial 12", bd=7, relief=SUNKEN)
        self.cphn_ibl1.grid(row=0, column=3, pady=5, padx=10)
        self.cphn_ibl1.config(state=DISABLED)

        self.cphn_lbl2 = Label(self.button_Total_frame,
                               text="Tax", bg="sky blue", fg="black",
                               font=("times new roman",
                                     12, "bold")).grid(row=1,
                                                       column=2,
                                                       padx=20,
                                                       pady=5)
        self.cphn_ibl2 = Entry(self.button_Total_frame,
                               textvariable=self.tax2, width=15,
                               font="arial 12", bd=7, relief=SUNKEN)
        self.cphn_ibl2.grid(row=1, column=3, pady=5, padx=10)
        self.cphn_ibl2.config(state=DISABLED)

        self.cphn_lbl3 = Label(self.button_Total_frame,
                               text="Total Quantity", bg="sky blue",
                               fg="black",
                               font=("times new roman",
                                     12, "bold")).grid(row=0,
                                                       column=4,
                                                       padx=20,
                                                       pady=5)
        self.cphn_ibl3 = Entry(self.button_Total_frame,
                               textvariable=self.total_quantity, width=15,
                               font="arial 12", bd=7, relief=SUNKEN)
        self.cphn_ibl3.grid(row=0, column=5, pady=5, padx=10)
        self.cphn_ibl3.config(state=DISABLED)

        self.cphn_lbl3 = Label(self.button_Total_frame,
                               text="Total Amount", bg="sky blue", fg="black",
                               font=("times new roman",
                                     12, "bold")).grid(row=1,
                                                       column=4,
                                                       padx=20,
                                                       pady=5)
        self.cphn_ibl3 = Entry(self.button_Total_frame,
                               textvariable=self.totalbill, width=15,
                               font="arial 12", bd=7, relief=SUNKEN)
        self.cphn_ibl3.grid(row=1, column=5, pady=5, padx=10)
        self.cphn_ibl3.config(state=DISABLED)

        self.lblcphn_Coupon = Label(self.button_Total_frame,
                                    text="Disscount%",
                                    bg="sky blue", fg="black",
                                    font=("times new roman",
                                          12, "bold")).grid(row=0,
                                                            column=6,
                                                            padx=5,
                                                            pady=5)
        self.txtcphn_coupon = Entry(self.button_Total_frame,
                                    textvariable=self.coupons, width=15,
                                    font="arial 12", bd=7, relief=SUNKEN)
        self.txtcphn_coupon.grid(row=0, column=7, pady=5, padx=5)

        self.cphn_Coupon_Total = Label(self.button_Total_frame, text="Amount",
                                       bg="sky blue", fg="black",
                                       font=("times new roman",
                                             12, "bold")).grid(row=1,
                                                               column=6,
                                                               padx=5,
                                                               pady=5)
        self.cphn_coupon_total = Entry(self.button_Total_frame,
                                       textvariable=self.coupon_total_pay,
                                       width=15,
                                       font="arial 12",
                                       bd=7, relief=SUNKEN)
        self.cphn_coupon_total.grid(row=1, column=7,
                                    pady=5, padx=5)
        self.cphn_coupon_total.config(state=DISABLED)

        self.cphn_pay_amount = Label(self.button_Total_frame,
                                     text="Paid Amount",
                                     bg="sky blue", fg="black",
                                     font=("times new roman",
                                           12, "bold")).grid(row=3,
                                                             column=6,
                                                             padx=5,
                                                             pady=5)
        self.cphn_pay_amount = Entry(self.button_Total_frame,
                                     textvariable=self.pay_amount,
                                     width=15, font="arial 12", bd=7,
                                     relief=SUNKEN).grid(row=3,
                                                         column=7,
                                                         pady=5,
                                                         padx=5)

        self.button = customtkinter.CTkButton(self.button_frame,
                                              width=14, height=40,
                                              border_width=0,
                                              corner_radius=8,
                                              fg_color="green",
                                              text_color="White",
                                              text="Total",
                                              text_font=('Helvetica', 14),
                                              command=lambda: [self.total()])
        self.button.grid(row=0, column=0, padx=5, pady=5)

        self.b = customtkinter.CTkButton(self.button_frame,
                                         width=14,
                                         height=40,
                                         border_width=0,
                                         corner_radius=8,
                                         fg_color="green",
                                         text_color="White",
                                         text="Bill",
                                         text_font=('Helvetica', 14),
                                         command=lambda: [self.gbill(),
                                                          self.disable_text(),
                                                          self.delete_edit()])
        self.b.grid(row=0, column=1, padx=5, pady=5)

        self.bu = customtkinter.CTkButton(self.button_frame, width=14,
                                          height=40, border_width=0,
                                          corner_radius=8,
                                          fg_color="green",
                                          text_color="White",
                                          text="Print",
                                          text_font=('Helvetica', 14),
                                          command=lambda: [self.print_bill()])
        self.bu.grid(row=0, column=2, padx=5, pady=5)

        self.b = customtkinter.CTkButton(self.button_frame, width=14,
                                         height=40, border_width=0,
                                         corner_radius=8,
                                         fg_color="green",
                                         text_color="White",
                                         text="Clear",
                                         text_font=('Helvetica', 14),
                                         command=lambda: [self.clear_bill(),
                                                          self.clear_bill_text()])
        self.b.grid(row=0, column=3, padx=5, pady=5)

        self.b = customtkinter.CTkButton(self.button_frame,
                                         width=14, height=0,
                                         border_width=0,
                                         corner_radius=8,
                                         fg_color="green",
                                         text_color="White",
                                         text="ApplyCoupon",
                                         text_font=('Helvetica', 14),
                                         command=lambda: [self.conf_coupon()])
        self.b.grid(row=0, column=4, padx=5, pady=5)

        '''displaying data of edit area'''
        '''displaying edit area'''
        self.billing_edit = Frame(self.master, bg="sky blue")
        self.billing_edit.place(x=538, y=235, width=440, height=370)

        self.b = customtkinter.CTkButton(self.billing_edit, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         fg_color="green",
                                         text_color="White",
                                         text="Add Cart",
                                         text_font=('Helvetica', 8),
                                         command=lambda: [self.upda_itm_quan(),
                                                          self.add_edit_ara()])
        self.b.grid(row=1, column=0, padx=2)

        self.bt = customtkinter.CTkButton(self.billing_edit, width=8,
                                          height=20, border_width=0,
                                          corner_radius=8,
                                          fg_color="green",
                                          text_color="White",
                                          text="Delete Cart",
                                          text_font=('Helvetica', 8),
                                          command=lambda: [self.updt_a_d_crt(),
                                                           self.del_itm_e_a()])
        self.bt.grid(row=1, column=2, padx=2)

        self.lbl_edit = Label(self.billing_edit, text="Cart", bg="sky blue",
                              fg="black", font=("times new roman", 14, "bold"))
        self.lbl_edit.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.combo_search = ttk.Combobox(self.billing_edit,
                                         textvariable=self.search_by1,
                                         width=7,
                                         font=("times new roman", 11, "bold"),
                                         state='readonly')
        self.combo_search['values'] = ("bill_no", "phone")
        self.combo_search.grid(row=0, column=1, padx=5, pady=5)
        self.ser = Button(self.billing_edit,
                          text="Search Customer Bill", bg="green",
                          fg='white', width=17, pady=5,
                          command=lambda: [self.user_bill(),
                                           self.disable_text()]).grid(row=0,
                                                                      column=3,
                                                                      padx=5,
                                                                      pady=5)
        self.txtBill = Entry(self.billing_edit,
                             width=9, font="arial 11", bd=7,
                             relief=SUNKEN,
                             textvariable=self.search_bill).grid(row=0,
                                                                 column=2,
                                                                 pady=5,
                                                                 padx=10)
        self.edit_Table_Frame = Frame(self.billing_edit,
                                      relief=RIDGE, bg="white")
        self.edit_Table_Frame.place(x=10, y=79, width=421, height=290)

        scroll_x = Scrollbar(self.edit_Table_Frame, orient=HORIZONTAL)

        s_x = scroll_x.set
        self.edit_billing_table = ttk.Treeview(self.edit_Table_Frame,
                                               columns=("ProductID",
                                                        "Products",
                                                        "Quantity",
                                                        "MRP_Price",
                                                        "product_details",
                                                        "CGST",
                                                        "SGST",
                                                        "Purchase_price",
                                                        "total_price"),
                                               xscrollcommand=s_x)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_x.config(command=self.edit_billing_table.xview)

        self.edit_billing_table.heading("ProductID", text="ProductID")
        self.edit_billing_table.heading("Products", text="Products")
        self.edit_billing_table.heading("Quantity", text="quantity")
        self.edit_billing_table.heading("MRP_Price", text="MRP_Price")
        self.edit_billing_table.heading("product_details",
                                        text="product_details")
        self.edit_billing_table.heading("CGST", text="CGST")
        self.edit_billing_table.heading("SGST", text="SGST")
        self.edit_billing_table.heading("Purchase_price",
                                        text="Purchase_price")
        self.edit_billing_table.heading("total_price", text="total_price")
        self.edit_billing_table['show'] = 'headings'
        self.edit_billing_table.column("ProductID", width=2)
        self.edit_billing_table.column("Products", width=100)
        self.edit_billing_table.column("Quantity", width=10)
        self.edit_billing_table.column("MRP_Price", width=20)
        self.edit_billing_table.column("product_details", width=20)
        self.edit_billing_table.column("CGST", width=10)
        self.edit_billing_table.column("SGST", width=20)
        self.edit_billing_table.column("Purchase_price", width=20)
        self.edit_billing_table.column("total_price", width=20)
        self.edit_billing_table.pack(fill=BOTH, expand=1)
        self.edit_billing_table.bind("<ButtonRelease-1>",
                                     self.edit_area_getData)
        self.dispalyAll_edit_area()

        self.style = ttk.Style()
        self.style.configure("Treeview", background='#7FFFD4',
                             foreground='black', font=('Calibri', 12),
                             rowheight=20)
        self.style.configure("Treeview.Heading", background='blue',
                             foreground='black', relief='flat',
                             font=('Calibri', 12))

    def welcome_default1(self):
        '''Billing area default text'''
        self.billing_area.insert(END, "\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END, "\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END, "\t       Hyderabad 500084\n")
        self.billing_area.configure(font='arial 12 bold')

    def remove_edit_area(self):
        '''Deletes products from cart area'''
        if self.cur.execute("delete from products"):
            self.con.commit()
            logging.info('item removed successfully from cart')
        else:
            logging.error('item not removed from cart')

    def getData(self, event):
        '''It will get products data from database and display it'''
        self.clearAll()
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]
        global quantity_set
        quantity_set = row[2]
        self.items.set(row[1])
        self.quantity.set(row[2])
        self.price.set(row[3])
        self.tablet_details.set(row[4])
        self.SGST_Amount.set(row[5])
        self.CGST_Amount.set(row[6])
        self.amount_purchased.set(row[7])

    def edit_area_getData(self, event):
        '''It will get products data from database and display it in cart'''
        try:
            self.clearAll()
            selected_row = self.edit_billing_table.focus()
            data = self.edit_billing_table.item(selected_row)
            global row
            row = data["values"]
            self.items.set(row[1])
            con = sqlite3.connect(database=saved_database)
            cur = con.cursor()
            cur.execute("SELECT * FROM products where product_name LIKE '%"
                        + str(self.items.get()) + "%'")
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
        except Exception as e:
            logging.error('Error handled by edit_area_getData method:', e)

    def upda_itm_quan(self):
        '''Updates product quantity'''
        if self.txtSheet.get() == '':
            messagebox.showerror("Please Select How many Sheets Required")
            return
        '''This method will update quantity cart'''
        quantity_reduce = (int(self.txtQuantity.get()) -
                           int(self.txtSheet.get()))
        self.db.update(self.txtName.get(), quantity_reduce,
                       self.txtMrp_Price.get(),
                       self.txtTablet_deatails.get(),
                       self.txtCGST.get(),
                       self.txtSGST.get(),
                       self.txtamount_purchased.get(), row[0])

    def updt_a_d_crt(self):
        '''This method will update quantity
            in cart after deleting product from cart'''
        quantity_add = int(self.txtQuantity.get()) + int(self.txtSheet.get())
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT * FROM products where product_name LIKE '%"
                    + str(self.items.get()) + "%'")
        quantity_rows = cur.fetchall()
        for quantity_row in quantity_rows:
            self.db.update(self.txtName.get(), quantity_add,
                           self.txtMrp_Price.get(),
                           self.txtTablet_deatails.get(),
                           self.txtCGST.get(),
                           self.txtSGST.get(),
                           self.txtamount_purchased.get(),
                           quantity_row[0])

    def dispalyAll(self):
        '''displays products in search products'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.fetch():
            self.billing_table.insert("", END, values=row)

    def dispalyAll_edit_area(self):
        '''Displays products in cart'''
        self.edit_billing_table.delete(*self.edit_billing_table.get_children())
        for row in self.db.edit_fetch():
            self.edit_billing_table.insert("", END, values=row)

    def search_dispalyAll(self):
        '''displays products data'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.search_data():
            self.billing_table.insert("", END, values=row)

    def update_edit_area(self):
        '''Updates cart products'''
        if self.txtSheet.get() == "":
            messagebox.showerror("Please Fill All the Details")
            return
        self.db.update_to_edit_area(self.edit_items, self.txtSheet.get(),
                                    self.edit_price, row[0])
        messagebox.showinfo("Success", "Record Update")
        logging.info('Updated products from cart')
        self.clearAll()
        self.dispalyAll_edit_area()

    def del_itm_e_a(self):
        '''This method will delete perticular product from the cart'''
        self.db.remove_oneitem_edit_area(row[0])
        self.clearAll()
        self.dispalyAll_edit_area()

    def delete_edit(self):
        '''This method deletes all data from cart'''
        self.db.remove_edit_area()
        self.clearAll()
        self.dispalyAll_edit_area()

    def clearAll(self):
        '''Clears all cart data'''
        self.items.set("")
        self.quantity.set("")
        self.price.set("")
        self.Sheet.set("")
        self.tablet_details.set("")
        self.SGST_Amount.set("")
        self.CGST_Amount.set("")
        self.amount_purchased.set("")

    def exit(self):
        if messagebox.askyesno('Exit', 'Do you really want to exit'):
            self.master.destroy()
            logging.info('Exited Successfully')

    def add_edit_ara(self):
        '''Adds product to cart'''
        if self.txtSheet.get() == "":
            return
        txt_mrp_price = float(self.txtMrp_Price.get())
        self.db.insert_to_edit_area(self.txtName.get(), self.txtSheet.get(),
                                    txt_mrp_price,
                                    self.txtTablet_deatails.get(),
                                    self.txtCGST.get(), self.txtSGST.get(),
                                    self.txtamount_purchased.get())
        self.clearAll()
        self.dispalyAll_edit_area()

    def total(self):
        '''This method will calculate Total Bill'''
        global sum1, sheet_price
        sum1 = 0
        global quantity1, CGST, SGST, Profit_Price
        quantity1 = 0
        Profit_Price = 0
        for row in self.db.edit_fetch():
            sum1 = sum1 + float(row[8])
            quantity1 = quantity1 + int(row[2])
            sheet_price = 0
            sheet_price = sheet_price + float(row[3])
            CGST = float(row[5]) * 0.01
            SGST = float(row[6]) * 0.01
            Profit_Price = Profit_Price + float(row[9])

        global tax, tax1, totalbill1
        tax = CGST + SGST
        tax1 = sum1 * tax
        self.tax2.set(tax1)
        totalbill1 = sum1 + tax1
        self.Total_price.set(sum1)
        self.totalbill.set(totalbill1)
        self.total_quantity.set(quantity1)

    def gbill(self):
        '''This method will Generate Bill'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT coupon_code from coupons where coupon_code LIKE '%"
                    + self.coupons.get() + "%'")
        rows1 = cur.fetchall()
        row_coupon = rows1[0][0]
        space = (57 * '=')

        if self.coupons.get() == row_coupon:
            self.welcome()
            for row in self.db.edit_fetch():
                a_ = row[1]
                b_ = row[2]
                c_ = row[3]
                d_ = row[8]
                t_x = "Total Products Amount"
                r_ = round(tax, 2)
                t_ = totalbill1
                q_ = quantity1
                m_ = matched_coupon
                f_ = Final_pay
                self.billing_area.insert(END,
                                         f"\n{a_}\t\t{b_}\t\t{c_}\t{d_}\t\t\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END,
                                     f"\nTotal\t\t{q_}\t\t\t{sum1}\t\t\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END, f"\nTax:{r_}% \t{t_x}: Rs. {sum1}\n")
            self.billing_area.insert(END,
                                     f"\nCGST : {CGST}% \t SGST : {SGST}%\n")
            self.billing_area.insert(END, f"\nTotal Amount:\t\t Rs. {t_}\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END,
                                     f"\nCoupon Disscount :\t\t{m_}%\n")
            self.billing_area.insert(END,
                                     f"\nTotal Pay Amount:\t\t Rs. {f_}\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END, "\n\tTHANK YOU\n")
            self.billing_area.insert(END, f"\n{space}\n")
            logging.info('Bill generated successfully')
            self.add_income()
            self.store_customer_data()
        else:
            self.welcome()
            for row in self.db.edit_fetch():
                r1 = row[1]
                r2 = row[2]
                r3 = row[3]
                r8 = row[8]
                ta = round(tax, 2)
                q1 = quantity1
                t_t = self.totalbill.get()
                self.billing_area.insert(END,
                                         f"\n{r1}\t\t{r2}\t\t{r3}\t{r8}\t\t\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END, f"\nTotal\t\t{q1}\t\t\t{sum1}\t\t\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END,
                                     f"\nTax:{ta}%\tTotal Amount:Rs. {sum1}\n")
            self.billing_area.insert(END,
                                     f"\nCGST :  {CGST}% \t  SGST : {SGST}%\n")
            self.billing_area.insert(END,
                                     f"\nTotal Amount:\t\t Rs. {totalbill1}\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END,
                                     f"\nTotal Pay Amount:\t\t Rs. {t_t}\n")
            self.billing_area.insert(END, f"\n{space}\n")
            self.billing_area.insert(END, "\n\tTHANK YOU\n")
            self.billing_area.insert(END, f"\n{space}\n")
            logging.info('Bill generated successfully')
            self.add_revenue_bill()
            self.add_cus_bill_data()

    def add_revenue_bill(self):
        '''This method will adds revenue data to revenue table'''
        convert_str = float(self.pay_amount.get())
        bill_amount = round(convert_str - (float(totalbill1)), 2)
        tax_price = round((float(self.tax2.get())), 2)
        self.db.insert_income(date, day, self.bill_no.get(),
                              quantity1,
                              totalbill1, tax_price, sum1, '0',
                              Profit_Price,
                              Profit_Price, self.pay_amount.get(),
                              bill_amount)

    def add_cus_bill_data(self):
        '''This method adds customer bill data'''
        for i in self.db.edit_fetch():
            self.db.insert_to_customer_data(self.c_phone.get(),
                                            self.bill_no.get(),
                                            i[1], i[2], i[3], i[8],
                                            tax, totalbill1,
                                            date, user_name1.get(),
                                            CGST, SGST, '0',
                                            '0', totalbill1,
                                            self.pay_amount.get())

    def user_bill(self):
        '''This method will search user bill histroy and display it'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT * from customer_datas where "
                    + str(self.search_by1.get()) + " LIKE '%"
                    + self.search_bill.get() + "%'")
        rows1 = cur.fetchall()
        bill_all = ''
        space = (37 * '=')
        for row in rows1:
            r_w = row[3]
            r7 = (row[7])
            r6 = (row[6])
            r11 = (row[11])
            r15 = (row[15])
            self.billing_area.delete(1.0, END)
            self.billing_area.insert(END, "\tWELCOME APOLLO MEDICAL\n")
            self.billing_area.insert(END, "\t  Hitech City Anjaiya Nagar\n")
            self.billing_area.insert(END, "\t    Hyderabad 500084\n")
            self.billing_area.insert(END, f"\n\nBill Number: \t\t{row[2]}")
            self.billing_area.insert(END, f"\nPhone Number: \t\t{row[1]}")
            self.billing_area.insert(END, "\nBill_Date: {row[9]}")
            self.billing_area.insert(END, f"\n\n{space}")
            self.billing_area.insert(END, "\nProduct\t\tQTY\t\tPrice Rs.")
            self.billing_area.insert(END, f"\n\n{space}")
            self.billing_area.insert(END,
                                     f"\n{r_w}\t\t{row[4]}\t\t{row[5]}\t\t\n")
            self.billing_area.insert(END, f"\n\n{space}")
            self.billing_area.insert(END,
                                     f"\nTax:{r7}%\t Total Amount: Rs. {r6}\n")
            self.billing_area.insert(END,
                                     f"\nCGST : {r11}%\t SGST : {row[12]}%\n")
            self.billing_area.insert(END,
                                     f"\nTotal Amount :\t\t Rs. {row[8]}\n")
            self.billing_area.insert(END, f"\n\n{space}")
            self.billing_area.insert(END,
                                     f"\nCoupon Disscount :\t\t{row[14]}%\n")
            self.billing_area.insert(END,
                                     f"\nTotal Pay Amount:\t\t Rs. {r15}\n")
            self.billing_area.insert(END, f"\n\n{space}")
            self.billing_area.insert(END, "\n\tTHANK YOU\n")
            self.billing_area.insert(END, f"\n\n{space}")
            self.billing_area.configure(font='arial 12 bold')
            logging.info('Customer bill searched successfully')
            bill_all = bill_all + self.billing_area.get('1.0', 'end-1c')
            self.billing_area.delete('1.0', 'end')
            self.billing_area.insert(END, bill_all)

    def store_customer_data(self):
        '''Save customer data and bill data to the database'''
        for i in self.db.edit_fetch():
            self.db.insert_to_customer_data(self.c_phone.get(),
                                            self.bill_no.get(),
                                            i[1], i[2], i[3], i[8], tax,
                                            totalbill1,
                                            date, user_name1.get(),
                                            CGST, SGST,
                                            coupon_disscount_total,
                                            matched_coupon,
                                            Final_pay, self.pay_amount.get())

    def add_income(self):
        '''Stores revenue data'''
        convert_str = float(self.pay_amount.get())
        bill_amount = round(convert_str - (float(final_pay_bill_amount)), 2)
        self.db.insert_income(date, day, self.bill_no.get(),
                              quantity1, final_pay_bill_amount, tax_amount,
                              tax_total_amount, coupon_disscount_total,
                              Profit_Price, Total_Profit_Price,
                              self.pay_amount.get(), bill_amount)

    def print_bill(self):
        '''Save the bill in PC'''
        q = self.billing_area.get('1.0', 'end-1c')
        filename = tempfile.mktemp('.txt')
        open(filename, 'w').write(q)
        os.startfile(filename, 'Print')
        logging.info('Printing generated bill')

    def clear_bill(self):
        '''Clears entry data'''
        self.c_phone.set('')
        self.items.set('')
        self.price.set('')
        self.tax2.set('')
        self.total_quantity.set('')
        self.totalbill.set('')
        self.Total_price.set('')
        self.coupon_total_pay.set('')
        self.coupons.set('')
        x = random.randint(1000, 9999)
        self.bill_no.set(str(x))
        self.welcome()
        logging.info('Cleared bill area')

    def search(self, *args):
        '''searches products according to there alphabets'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM products where product_name LIKE '%"
                        + str(self.search_txt.get()) + "%'")
            row = cur.fetchall()
            if len(row) > 0:
                self.billing_table.delete(*self.billing_table.get_children())
                for i in row:
                    self.billing_table.insert("", END, values=i)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def conf_coupon(self, *args):
        '''Coupon Search and conforms'''
        global coupon_disscount
        coupon_disscount = 0
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM coupons")
            row = cur.fetchall()
            for i in row:
                if i[1] == self.coupons.get():
                    coupon_disscount = coupon_disscount+int(i[2]) * float(0.01)
                    global matched_coupon, coupon_disscount_total
                    global final_pay_bill
                    global final_pay_bill_amount, float_amount, Final_pay
                    matched_coupon = i[2]
                    coupon_disscount_total = totalbill1 * coupon_disscount
                    final_pay_bill = totalbill1 - coupon_disscount_total
                    final_pay_bill_amount = round(final_pay_bill, 2)
                    '''Final pay amount with round up'''
                    Final_pay = final_pay_bill_amount
                    f_p_b_a = final_pay_bill_amount
                    f_p = Final_pay
                    float_amount = round((float(f_p)) - float(f_p_b_a), 2)
                    self.coupon_total_pay.set(final_pay_bill_amount)
                    global tax_amount, tax_total_amount
                    global disscount_amount, Total_Profit_Price
                    disscount_amount = sum1 * (float(matched_coupon) * 0.01)

                    tax_amount = float(sum1) * float(tax)
                    tax_total_amount = float(totalbill1) - float(tax_amount)
                    Total_Profit_Price = (float(Profit_Price) -
                                          float(coupon_disscount_total))
                    logging.info('Coupon applied successfully')

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
            logging.error('Have an error, coupon not matched')

    def disable_text(self):
        '''Disables the bill area'''
        self.billing_area.config(state=DISABLED)

    def clear_bill_text(self):
        '''Clears bill area'''
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0', 'end')

    def welcome_default(self):
        '''Default bill area textdisplays'''
        self.billing_area.insert(END, "\tWelcome Apollo Medical")
        self.billing_area.insert(END, "\t Hitech City Anjaiya Nagar")
        self.billing_area.insert(END, "\t Hyderabad 500084")

    def welcome(self):
        '''displays date, bill number medicall details in bill'''
        global date, month_word, day, month, year
        date = dt.datetime.now()
        month_word = date.strftime("%B")
        day = str(date.date())
        month = date.month
        year = date.year
        self.bill_no = StringVar()
        x = random.randint(1000, 9999)
        space = (38 * '=')
        self.bill_no.set(str(x))
        self.billing_area.delete(1.0, END)
        self.billing_area.insert(END, "\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END, "\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END, "\t   Hyderabad 500084\n")
        self.billing_area.insert(END,
                                 f"\n\nBill Num: \t\t{self.bill_no.get()}")
        self.billing_area.insert(END,
                                 f"\nPhone Num: \t\t{self.c_phone.get()}")
        self.billing_area.insert(END, f"\nBill_Date: {date}")
        self.billing_area.insert(END, f"\n\n{space}")
        self.billing_area.insert(END,
                                 "\nProduct\t\tQTY\t\tPrice\tTotal Price")
        self.billing_area.insert(END, "\n{space}\n")
        self.billing_area.configure(font='arial 12 bold')

    def track_loc(self):
        '''Tracks user location'''
        try:
            g = geocoder.ip('me')
            logging.info(f'{a.get()} location: {g.latlng}{g.state}, {g.city}')
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
            logging.error('Have an error, Location not detected')

    def clockin(self):
        '''User clock-in time and date stores'''
        try:
            global clockin_timing
            date = dt.datetime.now()
            day_clockin = str(date.date())
            con = sqlite3.connect(database=saved_database)
            cur = con.cursor()
            cur.execute("SELECT salary from users where username LIKE '%"
                        + str(a.get()) + "%'")
            row = cur.fetchall()
            for sal_row in row:
                date = dt.datetime.now()
                clockin_timing = str(date.time())
                day_clockin = str(date.date())
                month_clockin = date.month
                year_clockin = date.year
                number_of_months = calendar.monthrange(year_clockin,
                                                       month_clockin)[1]
                daily_sal = float(sal_row[0]) / number_of_months

            cur.execute("SELECT username, clockin_date from users_sal")
            row_user_name = cur.fetchall()
            ab = (a.get(), day_clockin)

            if ab in row_user_name:
                messagebox.showinfo("Error", "Today Already Clocked-in")
            else:
                self.db.insert_User_sal(a.get(), day_clockin,
                                        clockin_timing, daily_sal)
                messagebox.showinfo("Success", "Success Clockin")
                logging.error(f'Success, Successfully clocked in by {a.get()}')

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
            logging.error(f'Have an issue in clockin {a.get()}')

    def clockOut(self):
        '''User clock-out time and date stores'''
        try:
            global clockout_timing
            date = dt.datetime.now()
            day_clockin = str(date.date())
            con = sqlite3.connect(database=saved_database)
            cur = con.cursor()
            cur.execute("SELECT salary from users where username LIKE '%"
                        + str(a.get()) + "%'")
            row = cur.fetchall()

            for sal_row in row:
                date = dt.datetime.now()
                clockout_timing = str(date.time())
                day_clockout = str(date.date())
                month_clockout = date.month
                year_clockout = date.year
                number_of_months = calendar.monthrange(year_clockout,
                                                       month_clockout)[1]
                daily_sal = float(sal_row[0])/number_of_months

            cur.execute("SELECT username, clockOut_date from users_clockOut")
            row_user_name = cur.fetchall()
            ab = (a.get(), day_clockin)

            if ab in row_user_name:
                messagebox.showinfo("Error", "Today Already Clocked-Out")
            else:
                if messagebox.askyesno('Exit', 'Want to clock-out'):
                    self.db.insert_User_Clockout(a.get(), day_clockout,
                                                 clockout_timing, daily_sal)
                    messagebox.showinfo("Success", "Success Clock-Out")
                    logging.info(f'Success, clocked-out by {a.get()}')
                else:
                    logging.error('Error, User cannot logged out')
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
            logging.error(f'Have an issue in clock-out {a.get()}')


class Window_user_register(Database, Login_Window):
    '''This class redirects user and admin register page'''
    db = Database(saved_database)

    def __init__(self, register_window):
        self.register_window = register_window
        self.register_window.title("Register User")
        self.register_window.geometry("1920x1080")
        self.register_window.config(bg='blue')
        self.username = StringVar()
        self.password = StringVar()
        self.email = StringVar()
        self.phone_no = StringVar()
        self.address = StringVar()
        self.active = StringVar()
        self.usersal = StringVar()
        self.user_conform_password = StringVar()
        self.basic = StringVar()
        self.hra = StringVar()
        self.conveyance_allowance = StringVar()
        self.medical_allowance = StringVar()
        self.performance_bonus = StringVar()
        self.pf = StringVar()
        self.esi = StringVar()
        self.tax = StringVar()
        global t_sal
        t_sal = 0

        img = Image.open('images/medical.webp')
        logo = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.register_window, image=logo)
        logo_label.image = logo
        logo_label.place(width=1920, height=1080)

        self.user_frame = Frame(self.register_window, bg="light green")
        self.user_frame.place(x=40, y=50, width=800, height=650)

        self.lbluserName = Label(self.user_frame, text="User Name",
                                 font=("Calibri", 14), bg="light green",
                                 fg="black")
        self.lbluserName.grid(row=0, column=0, padx=10, pady=10)
        self.txtuserName = Entry(self.user_frame, textvariable=self.username,
                                 font=("Calibri", 14), bd=7,
                                 relief=SUNKEN, width=20)
        self.txtuserName.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.lblPassword = Label(self.user_frame, text="Password",
                                 font=("Calibri", 14), bg="light green",
                                 fg="black")
        self.lblPassword.grid(row=1, column=0, padx=10,
                              pady=10, sticky="w")
        self.txtpassword = Entry(self.user_frame,
                                 textvariable=self.password,
                                 font=("Calibri", 14),
                                 bd=7, relief=SUNKEN, width=20)
        self.txtpassword.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.txtpassword.config(state=DISABLED)

        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         fg_color='yellow',
                                         corner_radius=8,
                                         text="Generate Password",
                                         text_font=('Helvetica', 10),
                                         command=lambda: [self.enable(),
                                                          self.pass_random(),
                                                          self.disable()])
        self.b.grid(row=7, column=1, padx=50, pady=10, sticky="w")

        self.bu = customtkinter.CTkButton(self.user_frame, width=8,
                                          height=20, border_width=0,
                                          fg_color='yellow',
                                          corner_radius=8,
                                          text="Copy password",
                                          text_font=('Helvetica', 10),
                                          command=lambda: [self.c_admin_p()])
        self.bu.grid(row=7, column=0, padx=5, pady=10, sticky="w")

        self.lblEmail = Label(self.user_frame, text="Email Id",
                              font=("Calibri", 14), bg="light green",
                              fg="black")
        self.lblEmail.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txtEmail = Entry(self.user_frame, textvariable=self.email,
                              font=("Calibri", 14), bd=7,
                              relief=SUNKEN, width=20)
        self.txtEmail.grid(row=2, column=1, padx=10,
                           pady=10, sticky="w")

        self.lblPhone_no = Label(self.user_frame, text="Phone No",
                                 font=("Calibri", 14), bg="light green",
                                 fg="black")
        self.lblPhone_no.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.txtPhone_no = Entry(self.user_frame, textvariable=self.phone_no,
                                 font=("Calibri", 14), bd=7,
                                 relief=SUNKEN, width=20)
        self.txtPhone_no.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.lblAdress = Label(self.user_frame, text="Adress",
                               font=("Calibri", 14),
                               bg="light green", fg="black")
        self.lblAdress.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.txtAdress = Entry(self.user_frame, textvariable=self.address,
                               font=("Calibri", 14), bd=7,
                               relief=SUNKEN, width=20)
        self.txtAdress.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.lbl_edit = Label(self.user_frame, text="Is Active",
                              bg="light green", fg="black",
                              font=("times new roman", 14, "bold"))
        self.lbl_edit.grid(row=6, column=0, pady=10, padx=10, sticky="w")

        self.user_search = ttk.Combobox(self.user_frame,
                                        textvariable=self.active,
                                        width=7,
                                        font=("times new roman",
                                              11, "bold"),
                                        state='readonly')
        self.user_search['values'] = ("Yes", "No")
        self.user_search.grid(row=6, column=1, padx=10, pady=10,
                              sticky="w")

        self.lbluserSal = Label(self.user_frame, text="User Sal",
                                font=("Calibri", 14), bg="light green",
                                fg="black")
        self.lbluserSal.grid(row=5, column=0, padx=10,
                             pady=10, sticky="w")
        self.txtuserSal = Entry(self.user_frame,
                                textvariable=self.usersal,
                                font=("Calibri", 14), bd=7,
                                relief=SUNKEN, width=20)
        self.txtuserSal.grid(row=5, column=1, padx=10,
                             pady=10, sticky="w")

        self.btn_user = Frame(self.user_frame, bg="#535c68")
        self.btn_user.grid(row=6, column=0, columnspan=4,
                           padx=10, pady=10, sticky="w")

        self.b = customtkinter.CTkButton(self.user_frame,
                                         width=8, height=20,
                                         border_width=0,
                                         corner_radius=8,
                                         text="Register User",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.User_register(),
                                                          self.exit_re()])
        self.b.grid(row=8, pady=10, column=1)
        self.btn = customtkinter.CTkButton(self.user_frame, width=8,
                                           height=20,
                                           border_width=0,
                                           corner_radius=8,
                                           text="Send Mail",
                                           text_font=('Helvetica', 12),
                                           command=lambda: [self.send_mail()])
        self.btn.grid(row=8, pady=10, column=2)

        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         text="Registr Admin",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.Admin_regs(),
                                                          self.exit_re()])
        self.b.grid(row=8, pady=10, column=0)
        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         text="Update User",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.update_user_area(),
                                                          self.exit_re()])
        self.b.grid(row=9, pady=10, column=1)
        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         text="Update Admin",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.update_admin(),
                                                          self.exit_re(),])
        self.b.grid(row=9, pady=10, column=0)
        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         text="Delete User",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.delete_users(),
                                                          self.exit_re()])
        self.b.grid(row=10, pady=10, column=1)

        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         text="Delete Admin",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.delete_admins(),
                                                          self.exit_re()])
        self.b.grid(row=10, pady=10, column=0)
        user_tree_frame = Frame(self.register_window, bg="gold")
        user_tree_frame.place(x=900, y=50, width=615, height=295)

        '''Table Show admin data'''
        User_Frame = Frame(user_tree_frame, relief=RIDGE, bg="crimson")
        User_Frame.place(x=10, y=26, width=595, height=255)

        self.lbl_edit1 = Label(user_tree_frame, text="Users", bg="gold",
                               fg="Black",
                               font=("times new roman", 10, "bold"))
        self.lbl_edit1.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        scroll_x = Scrollbar(User_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(User_Frame, orient=VERTICAL)
        self.user_table = ttk.Treeview(User_Frame,
                                       columns=("UserId", "UserName",
                                                "Email", "PhoneNo",
                                                "Address", "Active",
                                                "Salary"),
                                       xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        self.user_table.heading("UserId", text="UserId")
        self.user_table.heading("UserName", text="UserName")
        self.user_table.heading("Email", text="Email")
        self.user_table.heading("PhoneNo", text="PhoneNo")
        self.user_table.heading("Address", text="Address")
        self.user_table.heading("Active", text="Active")
        self.user_table.heading("Salary", text="Salary")
        self.user_table['show'] = 'headings'
        self.user_table.column("UserId", width=10)
        self.user_table.column("UserName", width=10)
        self.user_table.column("Email", width=10)
        self.user_table.column("PhoneNo", width=10)
        self.user_table.column("Address", width=10)
        self.user_table.column("Active", width=10)
        self.user_table.column("Salary", width=10)
        self.user_table.pack(fill=BOTH, expand=1)
        self.user_table.bind("<ButtonRelease-1>", self.get_user_Data)
        self.dispalyUser()
        '''Admin Tree View'''
        admin_tree_frame = Frame(self.register_window, bg="gold")
        admin_tree_frame.place(x=900, y=350, width=615, height=350)

        admin_Frame = Frame(admin_tree_frame, relief=RIDGE, bg="crimson")
        admin_Frame.place(x=10, y=26, width=595, height=285)

        self.lbl_edit1 = Label(admin_tree_frame, text="Admins",
                               bg="gold", fg="Black",
                               font=("times new roman", 10, "bold"))
        self.lbl_edit1.grid(row=0, column=0, pady=5, padx=5,
                            sticky="w")

        scroll_x = Scrollbar(admin_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(admin_Frame, orient=VERTICAL)
        self.admin_table = ttk.Treeview(admin_Frame,
                                        columns=("UserId", "UserName",
                                                 "Email", "PhoneNo",
                                                 "Address", "Active"),
                                        xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.admin_table.xview)
        scroll_y.config(command=self.admin_table.yview)

        self.admin_table.heading("UserId", text="UserId")
        self.admin_table.heading("UserName", text="UserName")
        self.admin_table.heading("Email", text="Email")
        self.admin_table.heading("PhoneNo", text="PhoneNo")
        self.admin_table.heading("Address", text="Address")
        self.admin_table.heading("Active", text="Active")
        self.admin_table['show'] = 'headings'
        self.admin_table.column("UserId", width=10)
        self.admin_table.column("UserName", width=10)
        self.admin_table.column("Email", width=10)
        self.admin_table.column("PhoneNo", width=10)
        self.admin_table.column("Address", width=10)
        self.admin_table.column("Active", width=10)
        self.admin_table.pack(fill=BOTH, expand=1)
        self.admin_table.bind("<ButtonRelease-1>", self.get_admin_Data)
        self.dispalyAdmin()

    def send_mail(self):
        '''This method helps to send mail to users with there
            login credentials username and password'''
        try:
            sender_email = "pythonrgt@gmail.com"
            sender_password = "iyujvqelhcefwcbf"
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            msg = EmailMessage()

            msg.set_content(f"{self.username.get()} and {self.password.get()}")
            '''msg.set_content(f"Use Name :
                {self.username.get()} and Password : {self.password.get()}")'''
            msg['Subject'] = 'Pharmacy Login Credentials'
            msg['From'] = "pythonrgt@gmail.com"
            msg['To'] = self.email.get()

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            logging.info("Email sended with login credentials")
            messagebox.showinfo("Success",
                                "Email sended with login credentials")
        except Exception as e:
            logging.error("Error in sending mail:", e)

    def enable(self):
        '''Enables the password text'''
        self.txtpassword.config(state=NORMAL)

    def disable(self):
        '''Disables the password text'''
        self.txtpassword.config(state=DISABLED)

    def pass_random(self):
        '''Genertaes random password'''
        self.txtpassword.delete(0, END)
        pw_length = int(8)
        my_password = ''
        a_l = string.ascii_letters
        chars = a_l + string.digits + '!@#$%&123456789ABCDabcd'
        my_password = ''.join(random.choice(chars) for i in range(pw_length))
        self.txtpassword.insert(0, my_password)

    def c_admin_p(self):
        '''Copys generated password'''
        self.register_window.clipboard_clear()
        self.register_window.clipboard_append(self.txtpassword.get())

    def User_register(self):
        '''adds user'''
        if (self.txtuserName.get() == " " or self.txtpassword.get() == ""
                or self.txtEmail.get() == "" or self.txtPhone_no.get() == ""
                or self.txtAdress.get() == "" or self.user_search.get() == ""
                or self.usersal.get() == ""):
            messagebox.showerror("Error", "Please fill all details")
            return
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT * from users where username LIKE '%"
                    + str(self.txtuserName.get()) + "%'")
        row = cur.fetchall()
        if row == []:
            self.db.insert_User_register(self.txtuserName.get(),
                                         self.txtpassword.get(),
                                         self.txtEmail.get(),
                                         self.txtPhone_no.get(),
                                         self.txtAdress.get(),
                                         self.user_search.get(),
                                         self.usersal.get())
            self.send_mail()
            messagebox.showinfo("Success", "Record Inserted")
            logging.info('Registered user successfully')
        else:
            messagebox.showinfo("Failure", "User name already exits")

    def exit_re(self):
        '''destroys register window'''
        self.register_window.destroy()
        logging.info('Exited from user register window successfully')

    def Admin_regs(self):
        '''Adds admin data'''
        if (self.txtuserName.get() == " " or self.txtpassword.get() == ""
                or self.txtEmail.get() == "" or self.txtPhone_no.get() == "" or
                self.txtAdress.get() == "" or self.user_search.get() == ""):
            messagebox.showerror("Error", "Please fill all details")
            return
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT * from admins where username LIKE '%"
                    + str(self.txtuserName.get()) + "%'")
        row = cur.fetchall()
        if row == []:
            self.db.insert_admin_register(self.txtuserName.get(),
                                          self.txtpassword.get(),
                                          self.txtEmail.get(),
                                          self.txtPhone_no.get(),
                                          self.txtAdress.get(),
                                          self.user_search.get())
            self.send_mail()
            messagebox.showinfo("Success", "Record Inserted")
            logging.info('Registered user successfully')
        else:
            messagebox.showinfo("Failure", "User name already exits")

    def get_user_Data(self, event):
        '''searches user data from db and displays'''
        self.clearAllUser()
        selected_row = self.user_table.focus()
        data = self.user_table.item(selected_row)
        global row_user
        row_user = data["values"]
        self.username.set(row_user[1])
        self.email.set(row_user[2])
        self.phone_no.set(row_user[3])
        self.address.set(row_user[4])
        self.active.set(row_user[5])
        self.usersal.set(row_user[6])

    def get_admin_Data(self, event):
        '''searches admin data from db and displays'''
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
        '''Clears users data text'''
        self.username.set("")
        self.password.set("")
        self.email.set("")
        self.phone_no.set("")
        self.address.set("")
        self.active.set("")

    def dispalyUser(self, *args):
        '''Displays user data'''
        self.user_table.delete(*self.user_table.get_children())
        for row in self.db.fetch_user():
            self.user_table.insert("", END, values=row)

    def dispalyAdmin(self, *args):
        '''Displays admin data'''
        self.admin_table.delete(*self.admin_table.get_children())
        for row in self.db.fetch_admin():
            self.admin_table.insert("", END, values=row)

    def update_admin(self):
        '''Updates admin data'''
        if (self.txtuserName.get() == "" and self.txtpassword.get() == "" and
                self.user_search.get() == ""):
            messagebox.showerror("Erorr Input", "Please Fill All the Details")
            return
        self.db.update_admin(self.txtuserName.get(), self.txtpassword.get(),
                             self.txtEmail.get(), self.txtPhone_no.get(),
                             self.txtAdress.get(), self.user_search.get(),
                             row_admin[0])
        messagebox.showinfo("Success", "Admin Record Updated")

    def update_user_area(self):
        if (self.txtuserName.get() == "" and self.txtpassword.get() == ""
                and self.user_search.get() == ""):
            messagebox.showerror("Erorr in Input",
                                 "Please Fill All the Details")
            return
        self.db.update_user(self.txtuserName.get(), self.txtpassword.get(),
                            self.txtEmail.get(), self.txtPhone_no.get(),
                            self.txtAdress.get(), self.user_search.get(),
                            self.txtuserSal.get(), row_user[0])
        messagebox.showinfo("Success", "User Record Updated")

    def delete_users(self):
        '''Deletes user'''
        self.db.remove_user(row_user[0])
        self.clearAllUser()

    def delete_admins(self):
        '''Deletes admin'''
        self.db.remove_admin(row_admin[0])
        self.clearAllUser()


class Window_user_edit(Database, Login_Window):
    '''This class modifies user data'''
    db = Database(saved_database)

    def __init__(self, master):
        self.master = master
        self.master.title("Edit User")
        self.master.geometry("1920x1080")
        self.master.config(bg='grey')
        self.username = StringVar()
        self.password = StringVar()
        self.email = StringVar()
        self.phone_no = StringVar()
        self.address = StringVar()
        self.active = StringVar()
        self.user_name = StringVar()
        self.user_conform_password = StringVar()
        self.usersal = StringVar()

        img = Image.open('images/tablet.jpg')
        logo = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.master, image=logo)
        logo_label.image = logo
        logo_label.place(width=1920, height=1080)

        self.user_frame = Frame(self.master, bg="light green")
        self.user_frame.place(x=20, y=100, width=400, height=450)
        self.user_frame1 = Frame(self.master, bg="light green")
        self.user_frame1.place(x=240, y=10, width=600, height=77)
        space = (10 * ' ')
        self.lbluserName = Label(self.user_frame1,
                                 text=f"{space} EDIT USER PROFILE",
                                 font=("times new roman", 30, "bold"),
                                 bg="light green", fg="black")
        self.lbluserName.grid(row=0, column=1)

        self.lbluserName = Label(self.user_frame, text="User Name",
                                 font=("Calibri", 14), bg="light green",
                                 fg="black")
        self.lbluserName.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.txtuserName = Entry(self.user_frame, textvariable=self.username,
                                 font=("Calibri", 14), width=20)
        self.txtuserName.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.txtuserName.config(state=DISABLED)

        self.conform_password = Label(self.user_frame, text="Old Password",
                                      font=("Calibri", 14), bg="light green",
                                      fg="black")
        self.conform_password.grid(row=1, column=0,
                                   pady=10, padx=10, sticky="w")
        self.conform_password = Entry(self.user_frame, show="*",
                                      textvariable=self.user_conform_password,
                                      font=("Calibri", 14), width=20)
        self.conform_password.grid(row=1, column=1, padx=10,
                                   pady=10, sticky="w")

        self.lblPassword = Label(self.user_frame, text="New Password",
                                 font=("Calibri", 14), bg="light green",
                                 fg="black")
        self.lblPassword.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txtpassword = Entry(self.user_frame, show="*",
                                 textvariable=self.password,
                                 font=("Calibri", 14), width=20)
        self.txtpassword.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.txtpassword.config(state=DISABLED)

        self.bt = customtkinter.CTkButton(self.user_frame,
                                          width=8, height=20,
                                          border_width=0,
                                          fg_color='yellow',
                                          corner_radius=8,
                                          text="Generate Password",
                                          text_font=('Helvetica', 12),
                                          command=lambda: [self.enable(),
                                                           self.random_p(),
                                                           self.disable()
                                                           ]).grid(row=7,
                                                                   column=1,
                                                                   padx=50,
                                                                   pady=10,
                                                                   sticky="w")

        self.btn = customtkinter.CTkButton(self.user_frame, width=8,
                                           height=20, border_width=0,
                                           fg_color='yellow',
                                           corner_radius=8,
                                           text="Copy password",
                                           text_font=('Helvetica', 12),
                                           command=lambda: [self.clipper()
                                                            ]).grid(row=7,
                                                                    column=0,
                                                                    padx=5,
                                                                    pady=10,
                                                                    sticky="w")

        self.lblEmail = Label(self.user_frame, text="Email Id",
                              font=("Calibri", 14),
                              bg="light green", fg="black")
        self.lblEmail.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.txtEmail = Entry(self.user_frame, textvariable=self.email,
                              font=("Calibri", 14), width=20)
        self.txtEmail.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.lblPhone_no = Label(self.user_frame, text="Phone No",
                                 font=("Calibri", 14), bg="light green",
                                 fg="black")
        self.lblPhone_no.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.txtPhone_no = Entry(self.user_frame,
                                 textvariable=self.phone_no,
                                 font=("Calibri", 14), width=20)
        self.txtPhone_no.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.lblAdress = Label(self.user_frame, text="Adress",
                               font=("Calibri", 14), bg="light green",
                               fg="black")
        self.lblAdress.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.txtAdress = Entry(self.user_frame, textvariable=self.address,
                               font=("Calibri", 14), width=20)
        self.txtAdress.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.lblSal = Label(self.user_frame, text="Salary",
                            font=("Calibri", 14), bg="light green", fg="black")
        self.lblSal.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.txtSal = Entry(self.user_frame,
                            textvariable=self.usersal,
                            show='*', font=("Calibri", 14), width=20)
        self.txtSal.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.txtSal.config(state=DISABLED)

        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         fg_color='green',
                                         text_color='white',
                                         corner_radius=8,
                                         text="Update User",
                                         text_font=('Calibri', 14),
                                         command=lambda: [self.conform_pass()])
        self.b.grid(row=8, pady=10, column=1)

        '''Admin Tree View'''
        admin_tree_frame = Frame(self.master, bg="light green")
        admin_tree_frame.place(x=500, y=100, width=505, height=450)

        admin_Frame = Frame(admin_tree_frame, relief=RIDGE, bg="crimson")
        admin_Frame.place(x=10, y=20, width=485, height=405)
        scroll_x = Scrollbar(admin_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(admin_Frame, orient=VERTICAL)
        self.admin_table = ttk.Treeview(admin_Frame,
                                        columns=("UserId", "UserName",
                                                 "Email", "PhoneNo",
                                                 "Address", "Salary"),
                                        xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.admin_table.xview)
        scroll_y.config(command=self.admin_table.yview)

        self.admin_table.heading("UserId", text="UserId")
        self.admin_table.heading("UserName", text="UserName")
        self.admin_table.heading("Email", text="Email")
        self.admin_table.heading("PhoneNo", text="PhoneNo")
        self.admin_table.heading("Address", text="Address")
        self.admin_table.heading("Salary", text="Salary")
        self.admin_table['show'] = 'headings'
        self.admin_table.column("UserId", width=10)
        self.admin_table.column("UserName", width=10)
        self.admin_table.column("Email", width=10)
        self.admin_table.column("PhoneNo", width=10)
        self.admin_table.column("Address", width=10)
        self.admin_table.column("Salary", width=10)
        self.admin_table.pack(fill=BOTH, expand=1)
        self.admin_table.bind("<ButtonRelease-1>", self.get_user_edit)
        result = (ai, user_name_edit, user_email_edit,
                  user_ph_no, user_address_edit,
                  user_admin_edit, user_salary_edit)
        self.admin_table.insert("", END, values=result)
        self.clearAllUser()
        self.button_event()

        '''clock-in tree view'''
        tree_frame_clockout = Frame(self.master, bg="light green")
        tree_frame_clockout.place(x=997, y=102, width=507, height=250)

        Table_Frame = Frame(tree_frame_clockout, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=10, width=457, height=200)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table = ttk.Treeview(Table_Frame,
                                          columns=("User_names",
                                                   "Clockin_dates",
                                                   "Clockin_times"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)
        self.billing_table.heading("User_names", text="User_names")
        self.billing_table.heading("Clockin_dates", text="Clockin_dates")
        self.billing_table.heading("Clockin_times", text="Clockin_times")
        self.billing_table['show'] = 'headings'
        self.billing_table.column("User_names", width=10)
        self.billing_table.column("Clockin_dates", width=10)
        self.billing_table.column("Clockin_times", width=10)
        self.billing_table.pack(fill=BOTH, expand=1)
        self.dispalyAll_user_clockin_activity()

        '''clock-out tree view'''
        tree_frame_clockout1 = Frame(self.master, bg="light green")
        tree_frame_clockout1.place(x=997, y=302, width=507, height=250)

        '''Table Show user activity data'''
        Table_Frame = Frame(tree_frame_clockout1, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=10, width=457, height=200)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table = ttk.Treeview(Table_Frame,
                                          columns=("User_Name",
                                                   "Clockout_Date",
                                                   "Clockout_Time"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)
        self.billing_table.heading("User_Name", text="user_name")
        self.billing_table.heading("Clockout_Date", text="Clockout_Date")
        self.billing_table.heading("Clockout_Time", text="Clockout_Time")
        self.billing_table['show'] = 'headings'
        self.billing_table.column("User_Name", width=2)
        self.billing_table.column("Clockout_Date", width=10)
        self.billing_table.column("Clockout_Time", width=10)
        self.billing_table.pack(fill=BOTH, expand=1)
        self.dispalyAll_user_clockOut_activity()

    def dispalyAll_user_clockin_activity(self):
        '''This method will get Clock-in data from database and display it'''
        self.billing_table.delete(*self.billing_table.get_children())
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        cursor.execute('''SELECT username, clockin_date,
                       clockin_time from users_sal where username LIKE '%'''
                       + str(a.get()) + "%' ORDER BY clockin_date DESC")
        rows = cursor.fetchall()
        for i in rows:
            self.billing_table.insert("", END, values=i)

    def dispalyAll_user_clockOut_activity(self):
        '''This method will get clock-out data from database and display it'''
        self.billing_table.delete(*self.billing_table.get_children())
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        cursor.execute('''SELECT username, clockOut_date,
                       clockOut_time from users_clockOut
                       where username LIKE '%'''
                       + str(a.get()) + "%' ORDER BY clockOut_date DESC")
        rows = cursor.fetchall()
        for i in rows:
            self.billing_table.insert("", END, values=i)

    def dispalyAll_user_activity(self):
        '''This method will get Clock-in,
            clock-out data from database and display it'''
        self.billing_table.delete(*self.billing_table.get_children())
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        cursor.execute('''SELECT T.username, T.clockOut_date, T.clockOut_time,
                       S.username, S.clockin_date,
                       S.clockin_time from users_clockOut T join users_sal S
                       on T.username = S.username where S.username LIKE '%'''
                       + str(a.get()) + "%'")
        rows = cursor.fetchall()
        for i in rows:
            self.billing_table.insert("", END, values=i)

    def getData_User_activity(self):
        '''It will get Clock-in, clock-out data from database and display it'''
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]

    def disable(self):
        '''Disables the password text'''
        self.txtpassword.config(state=DISABLED)

    def enable(self):
        '''enable the password text'''
        self.txtpassword.config(state=NORMAL)

    def random_p(self):
        '''Creates random password'''
        self.txtpassword.delete(0, END)
        pw_length = int(8)
        my_password = ''
        s_a_l = string.ascii_letters
        chars = s_a_l + string.digits + '!@#$%&123456789ABCDabcd'
        my_password = ''.join(random.choice(chars) for i in range(pw_length))
        self.txtpassword.insert(0, my_password)

    def clipper(self):
        '''Used to copy generated password'''
        self.master.clipboard_clear()
        self.master.clipboard_append(self.txtpassword.get())

    def clearAllUser(self):
        '''Clear all user text'''
        self.username.set("")
        self.password.set("")
        self.email.set("")
        self.phone_no.set("")
        self.address.set("")
        self.active.set("")

    def get_user_edit(self, event):
        '''Fetches all users data and dispalys on tree view'''
        self.clearAllUser()
        selected_row = self.admin_table.focus()
        data = self.admin_table.item(selected_row)
        global row_admin
        row_admin = data["values"]
        self.username.set(user_name_edit)
        self.email.set(user_email_edit)
        self.phone_no.set(user_ph_no)
        self.address.set(user_address_edit)
        self.usersal.set(user_salary_edit)

    def conform_pass(self, *args):
        '''It checks the password given user is correct or not
            and conform with old password and changes new
            password in user edit profile'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM users")
            row = cur.fetchall()
            for i in row:
                if (i[2] == self.user_conform_password.get()
                        and self.txtuserName.get() == i[1]):
                    self.update_user_area()
                    logging.info('User password updated successfully')
                else:
                    logging.error('User password not updated')
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
            logging.error('Have an error, user data not updated')

    def update_user_area(self):
        '''Updates user data'''
        self.db.update_user_edit(self.txtpassword.get(), self.txtEmail.get(),
                                 self.txtPhone_no.get(), self.txtAdress.get(),
                                 self.txtSal.get(), ai)
        messagebox.showinfo("Success", "User Record Updated")


class Window_coupon_edit(Super_Admin_Window, Database, Login_Window):
    '''This class redirects to coupon page'''
    db = Database(saved_database)

    def __init__(self, cupon_window):
        self.cupon_window = cupon_window
        self.cupon_window.title("Edit User")
        self.cupon_window.geometry("1100x550")
        self.cupon_window.config(bg='grey')

        self.coupon_code_data = StringVar()
        self.coupon_amount = StringVar()
        img = Image.open('images/tablet.jpg')
        logo = img.resize((1100, 550), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.cupon_window, image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=550)

        self.coupon_frame = Frame(self.cupon_window, bg="light green")
        self.coupon_frame.place(x=20, y=100, width=420, height=300)

        self.coupon_frame1 = Frame(self.cupon_window, bg="light green")
        self.coupon_frame1.place(x=200, y=10, width=620, height=70)
        space = (10*' ')
        self.lblcoupon = Label(self.coupon_frame1,
                               text=f"{space} CREATE DISSCOUNT",
                               font=("Times new roman", 34, 'bold'),
                               bg="light green", fg="black")
        self.lblcoupon.grid(row=0, column=0)

        self.lblcoupon = Label(self.coupon_frame,
                               text="Disscount Name :",
                               font=("Calibri", 14),
                               bg="light green", fg="black")
        self.lblcoupon.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.txtcoupon = Entry(self.coupon_frame,
                               textvariable=self.coupon_code_data,
                               bd=7, relief=SUNKEN, font=("Calibri", 14),
                               width=20)
        self.txtcoupon.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.lblcoupon_disscount_amount = Label(self.coupon_frame,
                                                text="Discount % :",
                                                font=("Calibri", 14),
                                                bg="light green", fg="black")
        self.lblcoupon_disscount_amount.grid(row=2, column=0, pady=10,
                                             padx=10, sticky="w")
        c_a = self.coupon_amount
        self.txtcoupon_disscount_amount = Entry(self.coupon_frame,
                                                textvariable=c_a,
                                                bd=7, relief=SUNKEN,
                                                font=("Calibri", 14), width=20)
        self.txtcoupon_disscount_amount.grid(row=2, column=1,
                                             padx=10, pady=10, sticky="w")

        self.btnAdd = Button(self.coupon_frame,
                             command=lambda: [self.add_coupon(),
                                              self.exit_cupon()],
                             text='Generate Disscount',
                             font='arial 14 bold',
                             bg='green', fg='white',
                             padx=5, pady=5,
                             width=14)
        self.btnAdd.grid(row=3, column=1, pady=10)

        self.btnAdd = Button(self.coupon_frame,
                             command=lambda: [self.delete_coupons(),
                                              self.exit_cupon()],
                             text='Delete Disscount',
                             font='arial 16 bold',
                             bg='green', fg='white',
                             padx=5, pady=5,
                             width=14)
        self.btnAdd.grid(row=4, column=1, pady=10)

        '''Admin Tree View'''
        coupon_tree_frame = Frame(self.cupon_window, bg="light green")
        coupon_tree_frame.place(x=500, y=100, width=505, height=300)

        coupon_Frame = Frame(coupon_tree_frame, relief=RIDGE, bg="crimson")
        coupon_Frame.place(x=10, y=20, width=485, height=255)
        scroll_x = Scrollbar(coupon_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(coupon_Frame, orient=VERTICAL)
        self.coupons_table = ttk.Treeview(coupon_Frame,
                                          columns=("DisscountId",
                                                   "DisscountCode",
                                                   "Disscount%"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.coupons_table.xview)
        scroll_y.config(command=self.coupons_table.yview)

        self.coupons_table.heading("DisscountId", text="DisscountId")
        self.coupons_table.heading("DisscountCode", text="DisscountCode")
        self.coupons_table.heading("Disscount%", text="Disscount%")
        self.coupons_table['show'] = 'headings'
        self.coupons_table.column("DisscountId", width=10)
        self.coupons_table.column("DisscountCode", width=10)
        self.coupons_table.column("Disscount%", width=10)
        self.coupons_table.pack(fill=BOTH, expand=1)
        self.coupons_table.bind("<ButtonRelease-1>",
                                self.get_coupon_edit)
        self.dispalyAll_coupons()

    def get_coupon_edit(self, event):
        '''This can update coupon data'''
        self.clearAllCoupon()
        selected_row = self.coupons_table.focus()
        data = self.coupons_table.item(selected_row)
        global row_cupon
        row_cupon = data["values"]
        self.coupon_code_data.set(row_cupon[1])
        self.coupon_amount.set(row_cupon[2])

    def dispalyAll_coupons(self):
        '''It fetches coupon data from database and displays'''
        self.coupons_table.delete(*self.coupons_table.get_children())
        for row in self.db.fetch_cupon():
            self.coupons_table.insert("", END, values=row)

    def clearAllCoupon(self):
        '''Clears coupon Entries'''
        self.coupon_code_data.set("")
        self.coupon_amount.set("")

    def exit_cupon(self):
        '''This destroys coupon window'''
        self.cupon_window.destroy()
        logging.info('Exited from cupon generate Window Successfully')

    def add_coupon(self):
        '''This will add coupons'''
        if self.txtcoupon.get() == "":
            messagebox.showerror("Erorr in Input",
                                 "Please Fill All the Details")
            return
        self.db.insert_coupon(self.txtcoupon.get(),
                              self.txtcoupon_disscount_amount.get())
        messagebox.showinfo("Success", "Cupon Inserted")

    def delete_coupons(self):
        '''This method will delete perticular coupon from database'''
        self.db.remove_coupons(row_cupon[0])


class Window_income(User_Window, Super_Admin_Window, Database, Login_Window):
    '''This class will display revenue from one date to another date'''
    db = Database(saved_database)

    def __init__(self, cupon_window):
        self.cupon_window = cupon_window
        self.cupon_window.title("Edit User")
        self.cupon_window.geometry("1100x750")
        self.cupon_window.config(bg='grey')

        self.income_amounts = StringVar()
        self.search_day = StringVar()
        self.from_date = StringVar()
        self.to_date = StringVar()

        img = Image.open('images/a3.webp')
        logo = img.resize((1100, 750), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.cupon_window, image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=750)

        self.revenue_frame = Frame(self.cupon_window, bg="sky blue")
        self.revenue_frame.place(x=20, y=100, width=1020, height=550)

        self.revenue_frame1 = Frame(self.cupon_window, bg="light green")
        self.revenue_frame1.place(x=200, y=10, width=620, height=50)
        space = (10*' ')
        self.lblcoupon = Label(self.revenue_frame1,
                               text=f"{space} FIND OUT INCOME/REVENUE",
                               font=("Times new roman", 26, 'bold'),
                               bg="sky blue", fg="black")
        self.lblcoupon.grid(row=0, column=0)
        '''Empty'''
        self.lblincome = Label(self.revenue_frame,
                               text="", font=("Calibri", 14),
                               bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.lblincome = Label(self.revenue_frame,
                               text="From Date:",
                               font=("Calibri", 14),
                               bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.txtincome = DateEntry(self.revenue_frame,
                                   textvariable=self.from_date,
                                   date_pattern='y-mm-dd',
                                   bd=7, relief=SUNKEN,
                                   font=("Calibri", 12), width=20)
        self.txtincome.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.lblincome = Label(self.revenue_frame,
                               text="To Date:",
                               font=("Calibri", 14),
                               bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.txtincome = DateEntry(self.revenue_frame,
                                   textvariable=self.to_date,
                                   date_pattern='y-mm-dd',
                                   bd=7, relief=SUNKEN,
                                   font=("Calibri", 12), width=20)
        self.txtincome.grid(row=1, column=4, padx=10, pady=10, sticky="w")

        self.b = customtkinter.CTkButton(self.revenue_frame,
                                         width=14, height=30,
                                         border_width=0,
                                         text_color='white',
                                         fg_color='dark blue',
                                         corner_radius=8,
                                         text="Find Income",
                                         text_font=('Times new roman',
                                                    14),
                                         command=lambda: [self.income(),
                                                          self.search_bt1(),
                                                          self.del_inc()])
        self.b.grid(row=1, column=5, padx=10, pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.revenue_frame,
                                              width=14, height=30,
                                              border_width=0,
                                              text_color='white',
                                              fg_color='dark blue',
                                              corner_radius=8,
                                              text="Clear",
                                              text_font=('Times new roman',
                                                         14),
                                              command=lambda: [self.clear_i()])
        self.button.grid(row=1, column=6, padx=10, pady=10, sticky="w")

        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.cupon_window,
                                  bg="sky blue", bd=10, relief=GROOVE)
        self.billing_area.place(x=70, y=170, width=870, height=470)
        self.billing_tiltle = Label(self.billing_area,
                                    text="Income", font="arial 15 bold",
                                    fg="black", bg="sky blue",
                                    bd=7, relief=GROOVE).pack(fill=X)

        scroll_y = Scrollbar(self.billing_area, orient=VERTICAL)
        self.billing_area = Text(self.billing_area,
                                 yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH, expand=1)

    def income(self, *args):
        '''This method will search date from one
            date to another from database'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        self.search_month = StringVar()
        self.search_month_name = StringVar()
        global to_date_window3
        to_date_window3 = self.to_date
        try:
            cur.execute(f"select * from revenue where day_date >= \'{self.from_date.get()}\' AND day_date <= \'{self.to_date.get()}\'")
            rows = cur.fetchall()
            for row in rows:
                self.db.insert_income_edit(row[1], row[2], row[3], row[4],
                                           row[5], row[6], row[7], row[8],
                                           row[9], row[10], row[11],
                                           row[12])
                logging.info("Record inserted to revenue_edit table")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
            logging.error("Record not inserted to revenue_edit table")

    def search_bt1(self):
        '''It searches data from rvenue table and
            calculates how much profit and all and displays
            on revenue page'''
        sum_amount = 0
        sum_quantity = 0
        tax_amount = 0
        net_profit_amount = 0
        final_profit_amount = 0
        final_profit_paid_amount = 0
        income_after_deduction_emp_sal = 0
        emp_sal = 0
        mrp_amount = 0
        Tax_total1 = 0
        final_profit_price = 0

        for row in self.db.edit_fetch_income():
            mrp_amount = mrp_amount + float(row[7])
            Tax_total1 = Tax_total1 + float(row[6])
            tax_mrp_total = Tax_total1 + mrp_amount
            sum_amount = sum_amount + float(row[9])
            sum_quantity = sum_quantity + float(row[6])
            tax_amount = tax_amount + float(row[8])
            net_profit_amount = net_profit_amount + float(row[7])
            final_profit_amount = (final_profit_amount + float(row[10]))
            final_profit_paid_amount = (final_profit_paid_amount
                                        + float(row[12]))
            final_profit_price = final_profit_amount - final_profit_paid_amount
            con = sqlite3.connect(database=saved_database)
            cur = con.cursor()
            sal_p = f"select salary_per_day from users_sal where clockin_date >= \'{self.from_date.get()}\'"
            sal_c = f"clockin_date <= \'{self.to_date.get()}\'"
            cur.execute(f"{sal_p} AND {sal_c}\'")
            '''cur.execute(f"select salary_per_day from users_sal
                where clockin_date >= \'{self.from_date.get()}\'
                AND clockin_date <= \'{self.to_date.get()}\'")'''
            rows = cur.fetchall()
            sum_sal = 0
            for r1 in rows:
                sum_sal = sum_sal + float(r1[0])
            income_profit = final_profit_price - sum_sal
            income_after_deduction_emp_sal = (income_after_deduction_emp_sal +
                                              (final_profit_price - emp_sal))

        space = (117 * '=')
        m_a = round(mrp_amount, 2)
        T_t = round(Tax_total1, 2)
        t_m_t = round(tax_mrp_total, 2)
        P_P = round(final_profit_price, 2)
        f_p_p = round(final_profit_price, 2)
        s_s = round(sum_sal, 2)
        i_p = round(income_profit, 2)
        self.billing_area.insert(END, "\tAPOLLO MEDICAL\n")
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END, "\tYOUR INCOME\n")
        self.billing_area.configure(font='arial 14 bold')
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END, f"\n{space}\n")
        self.billing_area.insert(END,
                                 f"\t{'MRP_PRICE': <20}\t{'TAX': <20}\t\n")
        self.billing_area.insert(END,
                                 f"\t{m_a: <20}\t{T_t: >20}\t\n")
        self.billing_area.insert(END,
                                 f"\t{'TOTAL_PRI':<20}\t{'PROF_PRI': >30}\t\n")
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END,
                                 f"\t{t_m_t: >20}\t{P_P: >50}\t\n")
        self.billing_area.insert(END, f"\n{space}\n")

        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END, f"\n{space}\n")
        self.billing_area.insert(END, "\tAFTER DEDUCTION OF EMPLOYEE SAL\n")
        self.billing_area.configure(font='arial 14 bold')
        self.billing_area.insert(END, f"\n{space}\n")
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END,
                                 f"\t{'FLOAT_PRICE': <20}\t{'EMP_SAL': >30}\n")
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END,
                                 f"\t{f_p_p: <20}\t\t{s_s: >50}\t\n")
        self.billing_area.insert(END,
                                 f"\t{'PROFIt_DEDUCTION_OF_EMP_SAL': >50}\n")
        self.billing_area.insert(END, "\n")
        self.billing_area.insert(END,
                                 f"\t{i_p: >50}\t\n")
        self.billing_area.insert(END, f"\n{space}\n")
        self.billing_area.configure(font='arial 9 bold')

    def del_inc(self):
        '''This method deletes all data from revenue_edit table'''
        self.db.remove_edit_income()

    def add_income_edit(self):
        '''This method will edits income values and display on window'''
        self.db.insert_income_edit(row[1], row[2], row[3],
                                   row[4], row[5], row[6],
                                   row[7], row[8], row[9])
        messagebox.showinfo("Success", "Cupon Inserted")

    def clear_i(self):
        '''This method clears the income text'''
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0', 'end')
        logging.info('income area cleared')


class Window_add_products(Database, Login_Window):
    '''This class will displays add, update,delete product details'''
    db = Database(saved_database)

    def __init__(self, add_product):
        self.add_product = add_product
        self.add_product.title("Medical billing")
        self.add_product.geometry("1100x700+0+0")
        self.add_product.config(bg='#2c3e50')

        img = Image.open('images/tablet.jpg')
        logo = img.resize((1100, 700), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.add_product, image=logo)
        logo_label.image = logo
        logo_label.place(width=1100, height=700)

        self.items = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.search_by1 = StringVar()
        self.Total_price = StringVar()
        self.total_price = StringVar()
        self.tablet_details = StringVar()
        self.Sheet = StringVar()
        self.amount_purchased = StringVar()
        self.CGST_Amount = StringVar()
        self.SGST_Amount = StringVar()
        self.entries_frame = Frame(self.add_product, bg="light green")
        self.entries_frame.place(x=100, y=10, width=875, height=225)
        title = Label(self.entries_frame,
                      text="BILLING SYSTEM",
                      font=("Calibri", 14, "bold"),
                      bg="light green", fg="white")
        title.grid(row=0, columnspan=2, sticky="w")
        self.lblName = Label(self.entries_frame,
                             text="Product_Name",
                             font=("Calibri", 12),
                             bg="#535c68", fg="white")
        self.lblName.grid(row=1, column=0, padx=10,
                          pady=5, sticky="w")
        self.txtName = Entry(self.entries_frame,
                             textvariable=self.items,
                             font=("Calibri", 12),
                             bd=7, relief=SUNKEN, width=15)
        self.txtName.grid(row=1, column=1, padx=10,
                          pady=5, sticky="w")

        self.lblMrp_Price = Label(self.entries_frame,
                                  text="Product_MRP_Price",
                                  font=("Calibri", 12),
                                  bg="#535c68", fg="white")
        self.lblMrp_Price.grid(row=2, column=0, padx=10,
                               pady=5, sticky="w")
        self.txtMrp_Price = Entry(self.entries_frame,
                                  textvariable=self.price,
                                  font=("Calibri", 12),
                                  bd=7, relief=SUNKEN, width=15)
        self.txtMrp_Price.grid(row=2, column=1, padx=10,
                               pady=5, sticky="w")

        self.lblQuantity = Label(self.entries_frame,
                                 text="Product_Quantity",
                                 font=("Calibri", 12),
                                 bg="#535c68", fg="white")
        self.lblQuantity.grid(row=3, column=0, padx=10,
                              pady=5, sticky="w")
        self.txtQuantity = Entry(self.entries_frame,
                                 textvariable=self.quantity,
                                 font=("Calibri", 12),
                                 bd=7, relief=SUNKEN, width=15)
        self.txtQuantity.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.lblamount_purchased = Label(self.entries_frame,
                                         text="Purchased_disscount%",
                                         font=("Calibri", 12), bg="#535c68",
                                         fg="white")
        self.lblamount_purchased.grid(row=1, column=2,
                                      padx=10, pady=5, sticky="w")
        self.txtamount_purchased = Entry(self.entries_frame,
                                         textvariable=self.amount_purchased,
                                         font=("Calibri", 12),
                                         bd=7, relief=SUNKEN, width=15)
        self.txtamount_purchased.grid(row=1, column=3,
                                      padx=10, pady=5, sticky="w")

        self.lblCGST = Label(self.entries_frame,
                             text="CGST%", font=("Calibri", 12),
                             bg="#535c68", fg="white")
        self.lblCGST.grid(row=2, column=2, padx=10,
                          pady=5, sticky="w")
        self.txtCGST = Entry(self.entries_frame,
                             textvariable=self.CGST_Amount,
                             font=("Calibri", 12), bd=7,
                             relief=SUNKEN, width=15)
        self.txtCGST.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        self.lblSGST = Label(self.entries_frame,
                             text="SGST%", font=("Calibri", 12),
                             bg="#535c68", fg="white")
        self.lblSGST.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.txtSGST = Entry(self.entries_frame,
                             textvariable=self.SGST_Amount,
                             font=("Calibri", 12),
                             bd=7, relief=SUNKEN, width=15)
        self.txtSGST.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        self.lblTablet_details = Label(self.entries_frame,
                                       text="Tablet_details",
                                       font=("Calibri", 10),
                                       bg="#535c68", fg="white")
        self.lblTablet_details.grid(row=4, padx=10, column=0, sticky="w")

        self.txtTablet_deatails = Entry(self.entries_frame,
                                        textvariable=self.tablet_details,
                                        font=("Calibri", 12),
                                        bd=7, relief=SUNKEN, width=15)
        self.txtTablet_deatails.grid(row=4, padx=10, column=1, sticky="w")

        self.bu = customtkinter.CTkButton(self.entries_frame,
                                          width=8, height=20,
                                          border_width=0,
                                          corner_radius=8,
                                          text="Add Product",
                                          text_font=('Helvetica', 8,
                                                     'bold'),
                                          command=lambda: [self.add_items()])
        self.bu.grid(row=1, column=6, padx=10)

        self.b = customtkinter.CTkButton(self.entries_frame,
                                         width=8, height=20,
                                         border_width=0,
                                         corner_radius=8,
                                         text="Update Product",
                                         text_font=('Helvetica', 8,
                                                    'bold'),
                                         command=lambda: [self.update_items()])
        self.b.grid(row=2, column=6, padx=10)
        self.b = customtkinter.CTkButton(self.entries_frame,
                                         width=8, height=20,
                                         border_width=0,
                                         corner_radius=8,
                                         text="Delete Product",
                                         text_font=('Helvetica', 8,
                                                    'bold'),
                                         command=lambda: [self.delete_items()])
        self.b.grid(row=3, column=6, padx=10)
        self.bu = customtkinter.CTkButton(self.entries_frame,
                                          width=8, height=20,
                                          border_width=0,
                                          corner_radius=8,
                                          text="Clear Product",
                                          text_font=('Helvetica', 8,
                                                     'bold'),
                                          command=lambda: [self.clearAll()])
        self.bu.grid(row=4, column=6, padx=10)
        '''Table Frame (displaying data from data base)'''
        tree_frame = Frame(self.add_product, bg="light green")
        tree_frame.place(x=100, y=275, width=875, height=390)
        lbl_search = Label(tree_frame, text="Search Products",
                           bg="green", fg="white",
                           font=("times new roman", 14, "bold"))
        lbl_search.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        txt_Search = Entry(tree_frame, textvariable=self.search_txt,
                           width=20, font=("times new roman",
                                           10, "bold"),
                           bd=5, relief=GROOVE)
        txt_Search.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        txt_Search.bind("<Key>", self.search)

        '''Table Show product data'''
        Table_Frame = Frame(tree_frame, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=70, width=855, height=300)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table = ttk.Treeview(Table_Frame,
                                          columns=("ProductID", "Products",
                                                   "Quantity", "MRP_Price",
                                                   "product_details", "CGST",
                                                   "SGST", "Purchase_price"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)

        self.billing_table.heading("ProductID", text="ProductID")
        self.billing_table.heading("Products", text="Products")
        self.billing_table.heading("Quantity", text="quantity")
        self.billing_table.heading("MRP_Price", text="MRP_Price")
        self.billing_table.heading("product_details", text="product_details")
        self.billing_table.heading("CGST", text="CGST")
        self.billing_table.heading("SGST", text="SGST")
        self.billing_table.heading("Purchase_price", text="Purchase_price")
        self.billing_table['show'] = 'headings'
        self.billing_table.column("ProductID", width=2)
        self.billing_table.column("Products", width=100)
        self.billing_table.column("Quantity", width=10)
        self.billing_table.column("MRP_Price", width=20)
        self.billing_table.column("product_details", width=20)
        self.billing_table.column("CGST", width=10)
        self.billing_table.column("SGST", width=20)
        self.billing_table.column("Purchase_price", width=20)
        self.billing_table.pack(fill=BOTH, expand=1)
        self.billing_table.bind("<ButtonRelease-1>", self.getData)

    def getData(self, event):
        '''It will get data from database and display it'''
        try:
            self.clearAll()
            selected_row = self.billing_table.focus()
            data = self.billing_table.item(selected_row)
            global row
            row = data["values"]
            global quantity_set
            quantity_set = row[2]
            self.items.set(row[1])
            self.quantity.set(row[2])
            self.price.set(row[3])
            self.tablet_details.set(row[4])
            self.SGST_Amount.set(row[5])
            self.CGST_Amount.set(row[6])
            self.amount_purchased.set(row[7])
        except Exception as e:
            logging.error("Error, Error handled by adding products", e)

    def dispalyAll(self):
        ''' This method will display all aitems from database'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.fetch():
            self.billing_table.insert("", END, values=row)

    def search_dispalyAll(self):
        '''It will search the products from database
            according to there alphabets'''
        self.billing_table.delete(*self.billing_table.get_children())
        for row in self.db.search_data():
            self.billing_table.insert("", END, values=row)

    def add_items(self):
        '''This method will add products'''
        if (self.txtName.get() == "" or self.txtMrp_Price.get() == "" or
                self.txtQuantity.get() == "" or
                self.txtamount_purchased.get() == ""
                or self.txtCGST.get() == "" or self.txtSGST.get() == ""
                or self.txtTablet_deatails.get() == ""):
            messagebox.showerror("Erorr in Input",
                                 "Please Fill All the Details or check degit")
            return
        self.add_products_details()

    def add_products_details(self):
        mr = self.txtMrp_Price.get()
        qr = self.txtQuantity.get()
        sr = self.txtSGST.get()
        cr = self.txtCGST.get()
        if (mr.isdigit() or qr.isdigit() or sr.isdigit() or cr.isdigit()):
            txt_Name = float(self.txtMrp_Price.get())
            self.db.insert(self.txtName.get(),
                           self.txtQuantity.get(),
                           txt_Name, self.txtTablet_deatails.get(),
                           self.txtCGST.get(), self.txtSGST.get(),
                           self.txtamount_purchased.get())
            self.clearAll()
            self.dispalyAll()
        else:
            messagebox.showerror("Erorr in Input", "Check degit")

    def update_items(self):
        '''This method will update products'''
        self.db.update(self.txtName.get(), self.txtQuantity.get(),
                       self.txtMrp_Price.get(), self.txtTablet_deatails.get(),
                       self.txtCGST.get(), self.txtSGST.get(),
                       self.txtamount_purchased.get(), row[0])
        messagebox.showinfo("Success", "Record Update")
        logging.info('Updated products successfully')
        self.clearAll()
        self.dispalyAll()

    def delete_items(self):
        '''deletes products'''
        self.db.remove(row[0])
        self.clearAll()
        self.dispalyAll()

    def clearAll(self):
        '''Clear all text of products'''
        self.items.set("")
        self.quantity.set("")
        self.price.set("")
        self.Sheet.set("")
        self.tablet_details.set("")
        self.amount_purchased.set("")
        self.CGST_Amount.set("")
        self.SGST_Amount.set("")

    def search(self, *args):
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        b_t = self.billing_table
        try:
            cur.execute("SELECT * FROM products where product_name LIKE '%"
                        + str(self.search_txt.get()) + "%'")
            row = cur.fetchall()
            if len(row) > 0:
                b_t.delete(*self.billing_table.get_children())
                for i in row:
                    self.billing_table.insert("", END, values=i)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


class Window_Bill_Search(Database, Login_Window):
    '''This class will display user bill history'''
    db = Database(saved_database)

    def __init__(self, master):
        self.master = master
        self.master.title("Medical billing")
        self.master.geometry("900x780+0+0")
        self.master.config(bg='#202A44')

        self.search_bill = StringVar()
        self.search_by1 = StringVar()
        '''displaying bill area and dimenions'''
        self.billing_area = Frame(self.master, bg="#7FFFD4",
                                  bd=10, relief=GROOVE)
        self.billing_area.place(x=100, y=100, width=750, height=670)
        self.billing_tiltle = Label(self.billing_area,
                                    text="Bill Area", font="arial 15 bold",
                                    fg="black", bg="#7FFFD4",
                                    bd=7, relief=GROOVE).pack(fill=X)
        scroll_y = Scrollbar(self.billing_area, orient=VERTICAL)
        self.billing_area = Text(self.billing_area,
                                 yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH, expand=1)
        self.welcome_default()

        self.billing_edit = Frame(self.master, bg="#7FFFD4")
        self.billing_edit.place(x=100, y=20, width=750, height=80)

        self.lbl_edit = Label(self.billing_edit, text="Cart", bg="#7FFFD4",
                              fg="black", font=("times new roman", 14, "bold"))
        self.lbl_edit.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        self.combo_search = ttk.Combobox(self.billing_edit,
                                         textvariable=self.search_by1, width=7,
                                         font=("times new roman", 11, "bold"),
                                         state='readonly')
        self.combo_search['values'] = ("bill_no", "phone")
        self.combo_search.grid(row=0, column=1, padx=5, pady=5)

        self.search_btn = Button(self.billing_edit, text="Search_Cust_Bill",
                                 bg="skyblue", width=17, pady=5,
                                 command=lambda: [self.user_bill()])
        self.search_btn.grid(row=0, column=3, padx=5, pady=5)

        self.search_btn = Button(self.billing_edit, text="Clear",
                                 bg="skyblue", width=12, pady=5,
                                 command=lambda: [self.clear_bill_text()])
        self.search_btn.grid(row=0, column=4, padx=5, pady=5)

        self.txtBillSearch = Entry(self.billing_edit,
                                   width=9, font="arial 11",
                                   bd=7, relief=SUNKEN,
                                   textvariabl=self.search_bill).grid(row=0,
                                                                      column=2,
                                                                      pady=5,
                                                                      padx=10)

    def user_bill(self):
        '''This method will generate user bill
            histroy and display it'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT * from customer_datas where "
                    + str(self.search_by1.get())
                    + "LIKE '%" + self.search_bill.get() + "%'")
        rows1 = cur.fetchall()
        bill_all = ''
        spaceb = (34 * '=')
        for row in rows1:
            r3_ = row[3]
            r4_ = row[4]
            r7_ = (row[7])
            r6_ = row[6]
            r15_ = row[15]
            r11 = row[11]
            r12 = row[12]
            self.billing_area.delete(1.0, END)
            self.billing_area.insert(END, "\tWELCOME APOLLO MEDICAL\n")
            self.billing_area.insert(END, "\t  Hitech City Anjaiya Nagar\n")
            self.billing_area.insert(END, "\t    Hyderabad 500084\n")
            self.billing_area.insert(END, f"\n\nBill Number:\t\t{row[2]}")
            self.billing_area.insert(END, f"\nPhone Number:\t\t{row[1]}")
            self.billing_area.insert(END, f"\nBill_Date:{row[9]}")
            self.billing_area.insert(END,
                                     "\n\n==================================")
            self.billing_area.insert(END, "\nProduct\t\tQTY\t\tPrice Rs.")
            self.billing_area.insert(END,
                                     "\n==================================\n")
            self.billing_area.insert(END,
                                     f"\n{r3_}\t\t{r4_}\t\t{row[5]}\t\t\n")
            self.billing_area.insert(END,
                                     f"\n{spaceb}\n")
            self.billing_area.insert(END,
                                     f"\nTax:{r7_}%\tTotal Amount:Rs. {r6_}\n")
            self.billing_area.insert(END,
                                     f"\nCGST : {r11}% \t SGST : {r12}%\n")
            self.billing_area.insert(END,
                                     f"\nTotal Amount :\t\t Rs.{row[8]}\n")
            self.billing_area.insert(END,
                                     f"\n{spaceb}\n")
            self.billing_area.insert(END,
                                     f"\nCoupon Disscount :\t\t{row[14]}%\n")
            self.billing_area.insert(END,
                                     f"\nTotal Pay Amount :\t\t Rs. {r15_}\n")
            self.billing_area.insert(END,
                                     "\n================================\n")
            self.billing_area.insert(END, "\n\tTHANK YOU\n")
            self.billing_area.insert(END,
                                     "\n==============================\n")
            self.billing_area.configure(font='arial 12 bold')
            logging.info('Customer bill searched successfully')
            bill_all = bill_all + self.billing_area.get('1.0', 'end-1c')
            self.billing_area.delete('1.0', 'end')
            self.billing_area.insert(END, bill_all)

    def disable_text(self):
        '''Disables text billing_area'''
        self.billing_area.config(state=DISABLED)

    def clear_bill_text(self):
        '''clears bill history search'''
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0', 'end')
        logging.info('Bill area cleared')

    def welcome_default(self):
        self.billing_area.insert(END, "\tWELCOME APOLLO MEDICAL\n")
        self.billing_area.insert(END, "\t Hitech City Anjaiya Nagar\n")
        self.billing_area.insert(END, "\t       Hyderabad 500084\n")
        self.billing_area.configure(font='arial 12 bold')


class Window_emp(Database, Login_Window):
    '''This class will display employee/user salary slip'''
    db = Database(saved_database)

    def __init__(self, cupon_window):
        self.cupon_window = cupon_window
        self.cupon_window.title("Edit User")
        self.cupon_window.geometry("1920x1080")
        self.cupon_window.config(bg='#202A44')

        self.search_user_sal = StringVar()
        self.basic = StringVar()
        self.hra = StringVar()
        self.conveyance_allowance = StringVar()
        self.medical_allowance = StringVar()
        self.performance_bonus = StringVar()
        self.pf = StringVar()
        self.esi = StringVar()
        self.tax = StringVar()
        self.revenue_frame = Frame(self.cupon_window, bd=10,
                                   relief=GROOVE, bg="sky blue")
        self.revenue_frame.place(x=20, y=100, width=980, height=650)

        self.user_frame = Frame(self.cupon_window, bd=10,
                                relief=GROOVE, bg="sky blue")
        self.user_frame.place(x=1020, y=20, width=490, height=500)

        self.user_frame12 = Frame(self.cupon_window, bd=10,
                                  relief=GROOVE, bg="sky blue")
        self.user_frame12.place(x=1020, y=530, width=490, height=220)

        '''Table Show Data'''
        Table_Frame = Frame(self.user_frame12, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=5, y=5, width=460, height=190)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table_sal = ttk.Treeview(Table_Frame,
                                              columns=("Id",
                                                       "Basic",
                                                       "HRA",
                                                       "Conveyance_Allowance",
                                                       "Medical_Allowance",
                                                       "performans_bonus",
                                                       "PF",
                                                       "ESI",
                                                       "TAX"),
                                              xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table_sal.xview)
        scroll_y.config(command=self.billing_table_sal.yview)

        self.billing_table_sal.heading("Id", text="Id")
        self.billing_table_sal.heading("Basic", text="Basic")
        self.billing_table_sal.heading("HRA", text="HRA")
        self.billing_table_sal.heading("Conveyance_Allowance",
                                       text="Conveyance_Allowance")
        self.billing_table_sal.heading("Medical_Allowance",
                                       text="Medical_Allowance")
        self.billing_table_sal.heading("performans_bonus",
                                       text="performans_bonus")
        self.billing_table_sal.heading("PF", text="PF")
        self.billing_table_sal.heading("ESI", text="ESI")
        self.billing_table_sal.heading("TAX", text="TAX")
        self.billing_table_sal['show'] = 'headings'
        self.billing_table_sal.column("Id", width=2)
        self.billing_table_sal.column("Basic", width=2)
        self.billing_table_sal.column("HRA", width=20)
        self.billing_table_sal.column("Conveyance_Allowance", width=30)
        self.billing_table_sal.column("Medical_Allowance", width=30)
        self.billing_table_sal.column("performans_bonus", width=30)
        self.billing_table_sal.column("PF", width=10)
        self.billing_table_sal.column("ESI", width=20)
        self.billing_table_sal.column("TAX", width=20)
        self.billing_table_sal.pack(fill=BOTH, expand=1)
        self.billing_table_sal.bind("<ButtonRelease-1>", self.getData_sal)
        self.search_sal_dispalyAll()
        self.revenue_frame1 = Frame(self.cupon_window, bg="sky blue")
        self.revenue_frame1.place(x=160, y=10, width=690, height=50)
        space = (10*' ')
        self.lblcoupon = Label(self.revenue_frame1,
                               text=f"{space} FIND OUT EMPLOYEE SALARY SLIP",
                               font=("Times new roman", 24, 'bold'),
                               bg="sky blue", fg="black")
        self.lblcoupon.grid(row=0, column=0)
        '''Empty'''
        self.lblincome = Label(self.revenue_frame, text="",
                               font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.lblincome = Label(self.revenue_frame, text="Search User:",
                               font=("Calibri", 14), bg="sky blue", fg="black")
        self.lblincome.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.txtincome = Entry(self.revenue_frame,
                               textvariable=self.search_user_sal,
                               bd=7, relief=SUNKEN,
                               font=("Calibri", 12), width=20)
        self.txtincome.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.lblBasic = Label(self.user_frame, text="Basic",
                              font=("times new roman", 12, 'bold'),
                              bg="sky blue", fg="black")
        self.lblBasic.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.txtBasic = Entry(self.user_frame, textvariable=self.basic,
                              font=("times new roman", 12),
                              bd=7, relief=SUNKEN, width=20)
        self.txtBasic.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.lblHRA = Label(self.user_frame, text="HRA",
                            font=("times new roman", 12, 'bold'),
                            bg="sky blue", fg="black")
        self.lblHRA.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.txtHRA = Entry(self.user_frame, textvariable=self.hra,
                            font=("times new roman", 12),
                            bd=7, relief=SUNKEN, width=20)
        self.txtHRA.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        self.lblCon_alow = Label(self.user_frame,
                                 text="Conveyance Allowance",
                                 font=("times new roman", 12, 'bold'),
                                 bg="sky blue", fg="black")
        self.lblCon_alow.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.txtCon_alow = Entry(self.user_frame,
                                 textvariable=self.conveyance_allowance,
                                 font=("times new roman", 12),
                                 bd=7, relief=SUNKEN, width=20)
        self.txtCon_alow.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        self.lblMed_alow = Label(self.user_frame, text="Medical Allowance",
                                 font=("times new roman", 12, 'bold'),
                                 bg="sky blue", fg="black")
        self.lblMed_alow.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        self.txtMed_alow = Entry(self.user_frame,
                                 textvariable=self.medical_allowance,
                                 font=("times new roman", 12), bd=7,
                                 relief=SUNKEN, width=20)
        self.txtMed_alow.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        self.lblBonus = Label(self.user_frame, text="Performance Bonus",
                              font=("times new roman", 12, 'bold'),
                              bg="sky blue", fg="black")
        self.lblBonus.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        self.txtBonus = Entry(self.user_frame,
                              textvariable=self.performance_bonus,
                              font=("times new roman", 12),
                              bd=7, relief=SUNKEN, width=20)
        self.txtBonus.grid(row=4, column=3, padx=10, pady=10, sticky="w")

        self.lblPF = Label(self.user_frame, text="PF",
                           font=("times new roman", 12, 'bold'),
                           bg="sky blue", fg="black")
        self.lblPF.grid(row=5, column=2, padx=10, pady=10, sticky="w")
        self.txtPF = Entry(self.user_frame, textvariable=self.pf,
                           font=("times new roman", 12),
                           bd=7, relief=SUNKEN, width=20)
        self.txtPF.grid(row=5, column=3, padx=10, pady=10, sticky="w")

        self.lblESI = Label(self.user_frame, text="ESI",
                            font=("times new roman", 12, 'bold'),
                            bg="sky blue", fg="black")
        self.lblESI.grid(row=6, column=2, padx=10, pady=10, sticky="w")
        self.txtESI = Entry(self.user_frame, textvariable=self.esi,
                            font=("times new roman", 12),
                            bd=7, relief=SUNKEN, width=20)
        self.txtESI.grid(row=6, column=3, padx=10, pady=10, sticky="w")

        self.lblTax = Label(self.user_frame, text="Tax",
                            font=("times new roman", 12, 'bold'),
                            bg="sky blue", fg="black")
        self.lblTax.grid(row=7, column=2, padx=10, pady=10, sticky="w")
        self.txtTax = Entry(self.user_frame, textvariable=self.tax,
                            font=("times new roman", 12),
                            bd=7, relief=SUNKEN, width=20)
        self.txtTax.grid(row=7, column=3, padx=10, pady=10, sticky="w")

        self.b = customtkinter.CTkButton(self.user_frame, width=8,
                                         height=20, border_width=0,
                                         corner_radius=8,
                                         fg_color="dark blue",
                                         text_color="white",
                                         text="Submit",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.sal_str(),
                                                          self.exit_s()])
        self.b.grid(row=8, column=2, padx=1, pady=10, sticky="w")

        self.bu = customtkinter.CTkButton(self.user_frame,
                                          width=8, height=20,
                                          border_width=0,
                                          corner_radius=8,
                                          fg_color="dark blue",
                                          text_color="white",
                                          text="Update",
                                          text_font=('Helvetica', 12),
                                          command=lambda: [self.upd_sal_s(),
                                                           self.exit_s()])
        self.bu.grid(row=8, column=3, padx=1, pady=10, sticky="w")
        self.b = customtkinter.CTkButton(self.user_frame,
                                         width=8, height=20,
                                         border_width=0,
                                         corner_radius=8,
                                         fg_color="dark blue",
                                         text_color="white",
                                         text="Delete",
                                         text_font=('Helvetica', 12),
                                         command=lambda: [self.delete_s(),
                                                          self.exit_s()])
        self.b.grid(row=8, column=4, padx=1, pady=10, sticky="w")

        self.b = customtkinter.CTkButton(self.revenue_frame, width=14,
                                         height=30, border_width=0,
                                         text_color='white',
                                         fg_color='dark blue',
                                         corner_radius=8,
                                         text="Generate salary slip",
                                         text_font=('Times new roman',
                                                    14),
                                         command=lambda: [self.emp_sal_slip()])
        self.b.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        self.bt = customtkinter.CTkButton(self.revenue_frame,
                                          width=14, height=30,
                                          border_width=0,
                                          text_color='white',
                                          fg_color='dark blue',
                                          corner_radius=8,
                                          text="Clear",
                                          text_font=('Times new roman',
                                                     14),
                                          command=lambda: [self.clear_sal()])
        self.bt.grid(row=1, column=4, padx=10, pady=10, sticky="w")

        self.button = customtkinter.CTkButton(self.revenue_frame,
                                              width=14, height=30,
                                              border_width=0,
                                              text_color='white',
                                              fg_color='dark blue',
                                              corner_radius=8,
                                              text="Print slip",
                                              text_font=('Times new roman',
                                                         14),
                                              command=lambda: [self.prt_sal()])
        self.button.grid(row=1, column=5, padx=10, pady=10, sticky="w")
        '''Bill Area Dimentions'''
        self.billing_area = Frame(self.cupon_window, bg="sky blue")
        self.billing_area.place(x=50, y=170, width=920, height=570)

        scroll_y = Scrollbar(self.billing_area, orient=VERTICAL)
        self.billing_area = Text(self.billing_area,
                                 yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.billing_area.yview)
        self.billing_area.pack(fill=BOTH, expand=1)

    def clear_sal(self):
        '''This method clears the generated salary slip'''
        self.billing_area.config(state=NORMAL)
        self.billing_area.delete('1.0', 'end')
        logging.info('Employee salary area cleared')

    def sal_str(self):
        '''This method will add salary datas like PF, EST etc'''
        self.db.insert_sal_structure(self.txtBasic.get(),
                                     self.txtHRA.get(),
                                     self.txtCon_alow.get(),
                                     self.txtMed_alow.get(),
                                     self.txtBonus.get(),
                                     self.txtPF.get(),
                                     self.txtESI.get(),
                                     self.txtTax.get())

    def upd_sal_s(self):
        '''This method will update salary datas like PF, EST etc'''
        if (self.txtBasic.get() == "" and self.txtHRA.get() == ""
                and self.txtCon_alow.get() == ""
                and self.txtMed_alow.get() == ""
                and self.txtBonus.get() == "" and self.txtPF.get() == ""
                and self.txtESI.get() == "" and self.txtTax.get() == ""):
            messagebox.showerror("Erorr in Input",
                                 "Please Fill All the Details")
            return
        self.db.update_sal_structure(self.txtBasic.get(), self.txtHRA.get(),
                                     self.txtCon_alow.get(),
                                     self.txtMed_alow.get(),
                                     self.txtBonus.get(),
                                     self.txtPF.get(), self.txtESI.get(),
                                     self.txtTax.get(), row[0])
        messagebox.showinfo("Success", "Salary structure Record Updated")

    def delete_s(self):
        '''This method will delete perticular sal structure from database'''
        self.db.remove_sal_structure(row[0])

    def exit_s(self):
        '''Destroys sal structure'''
        logging.info('Destroyed sal structure page Successfully')
        self.cupon_window.destroy()

    def emp_sal_slip(self):
        '''This method fetch salry data like PF,
            ESI etc and generates salary slip'''
        con = sqlite3.connect(database=saved_database)
        cur = con.cursor()
        cur.execute("SELECT * from sal_structure")
        row_sal = cur.fetchall()
        for sal_structure in row_sal:
            global sal_performence_bonus
            sal_basic = (float(sal_structure[1])) * 0.01
            sal_hra = (float(sal_structure[2])) * 0.01
            sal_coveyance_allowance = (float(sal_structure[3])) * 0.01
            sal_performence_bonus = (float(sal_structure[5])) * 0.01
            sal_pf = (float(sal_structure[6])) * 0.01
            sal_esi = (float(sal_structure[7])) * 0.01
            sal_tax = (float(sal_structure[8])) * 0.01
            '''sal_medical_allowance = (float(sal_structure[4]))*0.01'''

        cur.execute("SELECT * from users where username LIKE '%"
                    + str(self.search_user_sal.get()) + "%'")

        '''cur.execute("SELECT * from users where username LIKE '%"+
            str(self.search_user_sal.get())+"%'")'''
        row = cur.fetchall()
        '''print("1111111111112222222:", row)'''
        for rows in row:
            emp_name = rows[1]
            emp_email = rows[3]
            emp_salary = rows[7]
            performance_fee = float(rows[7]) * sal_performence_bonus
            basic1 = float(rows[7]) * sal_basic
            '''basic = float(rows[7])'''
            convey_fee = (float(emp_salary)) * sal_coveyance_allowance
            pf = (float(emp_salary)) * sal_pf
            ESI = (float(emp_salary)) * sal_esi
            tax = (float(emp_salary)) * sal_tax
            HRA = (float(emp_salary)) * sal_hra
            Total_Earnings = basic1 + convey_fee + HRA + performance_fee
            Total_Contribution = pf + ESI
            Net_Pay = Total_Earnings - Total_Contribution - tax
            spaces = (150 * '=')
            T_c = Total_Contribution
            n_p = Net_Pay
            c_ = 'Conveyance Allowance'
            p = 'Performance Bonus'
            t = 'Total Earnings(A)'
            H = 'HRA'
            B = 'Basic'
            b = basic1
            C = convey_fee
            P = performance_fee
            T = Total_Earnings
            h = HRA
            pf = 'PF Employee'
            T_C = 'Total Contributions(B)'
        self.billing_area.insert(END, "PAYSLIP")
        self.billing_area.insert(END,
                                 "\n\nAPOLLO MEDICAL ANJAIAH NAGAR HYDERBAD")
        self.billing_area.insert(END, f"\nName: {emp_name}")
        self.billing_area.insert(END, f"\nEmail: {emp_email}")
        self.billing_area.insert(END, "\n\nSALARY DETAILS")
        self.billing_area.insert(END, f"\n\n{spaces}")
        self.billing_area.insert(END, "\n\nEARNINGS")
        self.billing_area.insert(END,
                                 f"\n{B}\t\t\t{c_}\t\t\t{H}\t\t\t{p}\t\t\t{t}")
        self.billing_area.insert(END,
                                 f"\n{b}\t\t\t{C}\t\t\t{h}\t\t\t{P}\t\t\t{T}#")
        self.billing_area.insert(END, "\n\nCONTRIBUTIONS")
        self.billing_area.insert(END, f"\n{pf}\t\t\tESI Employee\t\t\t{T_C}")
        self.billing_area.insert(END,
                                 f"\n{pf}\t\t\t{ESI}\t\t\t{T_c}")
        self.billing_area.insert(END, "\n\nTAXES & DEDUCTIONS")
        self.billing_area.insert(END,
                                 "\nProfessional Tax\t\t\tTotal Deductions(C)")
        self.billing_area.insert(END, f"\n{tax}\t\t\t{tax}")
        self.billing_area.insert(END, f"\n\n{spaces}")
        self.billing_area.insert(END,
                                 f"\n\nNet Sal Payable:\t\t\t\t\t\t\tRs.{n_p}")
        self.billing_area.insert(END, f"\n\n{spaces}")
        self.billing_area.configure(font='arial 10 bold')
        self.billing_area.configure(state=DISABLED)

    def search_sal_dispalyAll(self):
        '''This method will get salary data from
            database and display it'''
        g_c = self.billing_table_sal.get_children()
        self.billing_table_sal.delete(*g_c)
        for row in self.db.fetch_sal_structure():
            self.billing_table_sal.insert("", END, values=row)

    def clearAll(self):
        '''Clears salary slip'''
        self.basic.set('')
        self.hra.set('')
        self.conveyance_allowance.set('')
        self.medical_allowance.set('')
        self.performance_bonus.set('')
        self.pf.set('')
        self.esi.set('')
        self.tax.set('')

    def getData_sal(self, event):
        '''This method will get salary data from database and
            display it'''
        self.clearAll()
        selected_row = self.billing_table_sal.focus()
        data = self.billing_table_sal.item(selected_row)
        global row
        row = data["values"]
        self.basic.set(row[1])
        self.hra.set(row[2])
        self.conveyance_allowance.set(row[3])
        self.medical_allowance.set(row[4])
        self.performance_bonus.set(row[5])
        self.pf.set(row[6])
        self.esi.set(row[7])
        self.tax.set(row[8])

    def prt_sal(self):
        '''Save the salary slip bill in PC'''
        q = self.billing_area.get('1.0', 'end-1c')
        filename = tempfile.mktemp('.txt')
        open(filename, 'w').write(q)
        os.startfile(filename, 'Print')
        logging.info('Printed salary slip')


class Window_User_Activity(Database, Login_Window):
    '''This class will display user clock-in clock-out timings'''
    db = Database(saved_database)

    def __init__(self, cupon_window):
        self.activity_window = cupon_window
        self.activity_window.title("Edit User")
        self.activity_window.geometry("1920x1080")
        self.activity_window.config(bg='#202A44')

        tree_frame = Frame(self.activity_window, bg="#535c68")
        tree_frame.place(x=50, y=70, width=650, height=670)

        c_frame = Frame(self.activity_window, bg="#535c68")
        c_frame.place(x=650, y=70, width=650, height=670)

        tree_frame_button = Frame(self.activity_window, bg="#7FFFD4")
        tree_frame_button.place(x=50, y=10, width=1257, height=50)
        space = (70*" ")
        self.lblESI = Label(tree_frame_button,
                            text=f"{space} Employee Activity",
                            font=("times new roman", 24, 'bold'),
                            bg="#7FFFD4", fg="black")
        self.lblESI.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        Table_Frame = Frame(c_frame, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=0, y=10, width=640, height=650)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table = ttk.Treeview(Table_Frame,
                                          columns=("User_Name",
                                                   "Clockout_Date",
                                                   "Clockout_Time"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)
        self.billing_table.heading("User_Name", text="user_name")
        self.billing_table.heading("Clockout_Date", text="Clockout_Date")
        self.billing_table.heading("Clockout_Time", text="Clockout_Time")
        self.billing_table['show'] = 'headings'
        self.billing_table.column("User_Name", width=10)
        self.billing_table.column("Clockout_Date", width=10)
        self.billing_table.column("Clockout_Time", width=10)
        self.billing_table.pack(fill=BOTH, expand=1)
        self.dispalyAll_clockOut_activity()
        self.style = ttk.Style()
        self.style.configure("Treeview", background='#7FFFD4',
                             foreground='black',
                             font=('Calibri', 12),
                             rowheight=20)
        self.style.configure("Treeview.Heading", background='blue',
                             foreground='purple', relief='flat',
                             font=('Calibri', 12))
        '''Table Show Data User Clockin Tree View'''
        Table_Frame = Frame(tree_frame, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=10, width=640, height=650)
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.billing_table = ttk.Treeview(Table_Frame,
                                          columns=("User_names",
                                                   "Clockin_dates",
                                                   "Clockin_times"),
                                          xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.billing_table.xview)
        scroll_y.config(command=self.billing_table.yview)
        self.billing_table.heading("User_names", text="User_names")
        self.billing_table.heading("Clockin_dates", text="Clockin_dates")
        self.billing_table.heading("Clockin_times", text="Clockin_times")
        self.billing_table['show'] = 'headings'
        self.billing_table.column("User_names", width=10)
        self.billing_table.column("Clockin_dates", width=10)
        self.billing_table.column("Clockin_times", width=10)
        self.billing_table.pack(fill=BOTH, expand=1)
        self.dispalyAll_clockin_activity()

    def getData_activity(self):
        '''It will get Clock-in, clock-out data from database and display it'''
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]

    def getData_activity_clockin(self):
        '''It will get Clock-in data from database and display it'''
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]

    def getData_activity_clockout(self):
        '''It will get Clock-out data from database and display it'''
        selected_row = self.billing_table.focus()
        data = self.billing_table.item(selected_row)
        global row
        row = data["values"]

    def dispalyAll_edit_area_activity(self):
        '''This method will get Clock-in, clock-out data'''
        self.billing_table.delete(*self.billing_table.get_children())
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        sql = '''SELECT T.username,T.clockOut_date,T.clockOut_time,
                S.username,S.clockin_date,S.clockin_time
                from users_clockOut
                T join users_sal S on T.username = S.username;'''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            self.billing_table.insert("", END, values=i)

    def dispalyAll_clockin_activity(self):
        '''This method will get Clock-in data from database and display it'''
        self.billing_table.delete(*self.billing_table.get_children())
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        sql = '''SELECT username, clockin_date, clockin_time
                from users_sal
                ORDER BY clockin_date DESC;'''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            self.billing_table.insert("", END, values=i)

    def dispalyAll_clockOut_activity(self):
        '''This method will get clock-out data from database and display it'''
        self.billing_table.delete(*self.billing_table.get_children())
        connection = sqlite3.connect(saved_database)
        cursor = connection.cursor()
        sql = '''SELECT username, clockOut_date, clockOut_time
                from users_clockOut
                ORDER BY clockOut_date DESC;'''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for i in rows:
            self.billing_table.insert("", END, values=i)


if __name__ == '__main__':
    main()




