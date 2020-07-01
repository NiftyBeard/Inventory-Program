# Program made by Garrett Witt for use by WMC Help Desk for Inventory control

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import json
#import pandas as pd
#from IPython.display import HTML
#import pandastable as pt
import time
from datetime import datetime
import sqlite3
import os
import csv

def get_date_time(fmt='%Y_%m_%d'):
    date_stamp = datetime.now().strftime(fmt)
    return date_stamp

def get_time(fmt='%H:%M'):
    time_stamp = datetime.now().strftime(fmt)
    return time_stamp




# ======================== Inventory ==========================
assets = ('Assets.json')
tableData = ['AssetTag', 'Type']
'''TABLE NAMES FOR SQL TABLES
assets = Asset information, values are Asset, Type of Device, Manufacturer, and Model
users = User information, values are firstname, lastname, and empnum
checkedin = Asset info from assets table, used to show if a unit is checked in
checkedout = Asset info from assets table, used to show if a unit is checked out'''

# ================= SQLite3 Database Setup ====================
# Commented out since database is already created
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

'''c.execute("""CREATE TABLE assets (
			asset text,
			type text,
			manufacturer text,
			model text
			)""")
c.execute("""CREATE TABLE users (
			firstname text,
			lastname text,
			empnum text
			)""")
c.execute("""CREATE TABLE checkedin (
			asset text,
			type text,
			manufacturer text,
			model text
			)""")
c.execute("""CREATE TABLE checkedout (
			asset text,
			type text,
			manufacturer text,
			model text
			)""")
with open('C:/Users/Garrett/Downloads/employees.csv', 'r') as fin:
	dr = csv.DictReader(fin)
	to_db = [(i['empnum'], i['lastname'], i['firstname'])for i in dr]

c.execute("INSERT INTO users (firstname, lastname, empnum) VALUES (?, ?, ?);", to_db)
conn.commit()
conn.close()'''

#====================== Add User ===============================
def adduserwindow():

	win2=Toplevel(window, bg='#121212')
	win2.title('Add User')
	win2.geometry("1200x800")
	win2.resizable(0,0)

	frame2 = tk.Frame(win2, bg='#121212', bd=0)
	frame2.pack(side='top')

	tk.Label(frame2, text='\n' + '\n' '\n' + '\n' '\n' + '\n' 'Add New User' + '\n' + '\n', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=0, columnspan=2)
	tk.Label(frame2, text='First Name', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=1)
	tk.Label(frame2, text='Last Name', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=2)
	tk.Label(frame2, text='Employee Number', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=3)

	e1 = tk.Entry(frame2, font=("Helvetica", 20))
	e2 = tk.Entry(frame2, font=("Helvetica", 20))
	e3 = tk.Entry(frame2, font=("Helvetica", 20))
	e3entry = e3.get()

	if len(e3entry) >= 8:
		e3.replace("N", "")
	elif len(e3entry) == 8:
		pass

	
	e1.grid(row=1, column=1)
	e2.grid(row=2, column=1)
	e3.grid(row=3, column=1)



	


#======================== Exporting User Capture to users.db ===================
	def adduser():
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		empnum = e3.get()
		fname = e1.get()
		lname = e2.get()

		with conn:
			c.execute("INSERT INTO users VALUES (:firstname, :lastname, :empnum)",
				{
				'firstname': fname,
				'lastname': lname,
				'empnum': empnum.replace("N", "")
				})

		conn.commit()


		tk.messagebox.Message("User " + fname + " " + lname + " " + empnum.replace("N", "") + " " + "has been added to users.db!")
		
		conn.close()

		e1.delete(0, END)
		e2.delete(0, END)
		e3.delete(0, END)

	conn = sqlite3.connect('inventory.db')
	c = conn.cursor()
	c.execute("SELECT * FROM users")
	records = c.fetchall()
	print_records = ''
	for record in records:
		print_records += str(record[0]) + " " + str(record[1]) + "\t" + str(record[2]) + "\n"

	print(print_records)

	adduserOutput = tk.Label(frame2, bg='#121212', text=print_records, fg='white', font=("Helvetica", 20)).grid(row=5, columnspan=2)

	conn.close()
	
	buttonadd = tk.Button(frame2, text='Add User', bg='#03DAC6', font=("Helvetica", 20), command=adduser).grid(row=4)
	buttoncloseuser = tk.Button(frame2, text='Close', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[win2.destroy(), window.mainloop()]).grid(row=4, column=2)

	

	win2.mainloop()


#======================= Check In ===========================
def checkinwindow():


	win3=Toplevel(window, bg='#121212')
	win3.title('Check In')
	win3.geometry("1200x800")
	win3.resizable(0,0)

	frame3 = tk.Frame(win3, bg='#121212', bd=0)
	frame3.pack(side='top')

	tk.Label(frame3, text='\n' + '\n' '\n' + '\n' '\n' + '\n' 'Check In Asset' + '\n' + '\n', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=0, columnspan=2)
	tk.Label(frame3, text='Tech Checking In', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=1)
	tk.Label(frame3, text='User Checking In', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=2)
	tk.Label(frame3, text='Asset', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=3)

	def limitsizebadgeTech(*args):
		value1 = e1.get()
		if len(value1) > 9: e1.set(value1[9])

	e1Value = StringVar()
	e1Value.trace('w', limitsizebadgeTech)
	
	def limitsizebadgeUser(*args):
		value2 = e2.get()
		if len(value2) > 9: e2.set(value2[9])

	e2Value = StringVar()
	e2Value.trace('w', limitsizebadgeUser)


	e1 = tk.Entry(frame3, font=("Helvetica", 20))
	tech = e1.get()
	e2 = tk.Entry(frame3, font=("Helvetica", 20))
	user = e2.get()
	e3 = tk.Entry(frame3, font=("Helvetica", 20))
	asset = e3.get()

	e1.grid(row=1, column=1)
	e2.grid(row=2, column=1)
	e3.grid(row=3, column=1)

#================= Check In and Log =========================

	def checkinlog():
		tech = e1.get()
		user = e2.get()
		asset = e3.get()
		formData = [{
			"Tech": tech.replace("N", ""),
			"User": user.replace("N", ""),
			"AssetTag": asset,
			"Date": get_date_time(),
			"Time":  get_time(),
			"Status": "Checked In"
		}] 
		#"Tech": e1.get(), "User": e2.get(), "AssetTag": e3.get(), "Time": get_date_time(), get_time()

		with open('Log.json') as data_file:
			old_data = json.load(data_file)
		data = (old_data, formData)

		with open('Log.json', 'w') as outfile:
			json.dump(data, outfile, indent=4,)

	def checkinasset():
		assettag = e3.get()
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("SELECT * FROM assets WHERE asset = :asset",
		{
		'asset': str(assettag)
		})
		assetinfo = ''
		typeinfo = ''
		maninfo = ''
		modinfo = ''
		records = c.fetchall()
		for record in records:
			assetinfo += str(record[0])
			typeinfo += str(record[1])
			maninfo += str(record[2])
			modinfo += str(record[3])
		

		with conn:
			c.execute("INSERT INTO checkedin VALUES (:asset, :type, :manufacturer, :model)",
			{
				'asset': assetinfo,
				'type': typeinfo,
				'manufacturer': maninfo,
				'model': modinfo
			})
			c.execute("DELETE FROM checkedout WHERE asset = :asset",
			{
			'asset': str(assettag)
			})


		conn.commit()
		conn.close()
		

	buttoncheckin = tk.Button(frame3, text='Check In', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[checkinlog(), checkinasset()]).grid(row=4)
	buttonclosein = tk.Button(frame3, text='Close', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[win3.destroy(), window.mainloop()]).grid(row=4, column=2)



	win3.mainloop()

#===================== Check Out GUI ============================
def checkoutwindow():
	

	win4=Toplevel(window, bg='#121212', bd=0)
	win4.title('Check Out')
	win4.geometry("1200x800")
	win4.resizable(0,0)

	frame4 = tk.Frame(win4, bg='#121212', bd=0)
	frame4.pack(side='top')

	tk.Label(frame4, text='\n' + '\n' '\n' + '\n' '\n' + '\n' 'Check Out Asset' + '\n' + '\n', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=0, columnspan=2)
	tk.Label(frame4, text='Tech Checking Out', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=1)
	tk.Label(frame4, text='User Checking Out', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=2)
	tk.Label(frame4, text='Asset', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=3)

	e1 = tk.Entry(frame4, font=("Helvetica", 20))
	e2 = tk.Entry(frame4, font=("Helvetica", 20))
	e3 = tk.Entry(frame4, font=("Helvetica", 20))

	e1.grid(row=1, column=1)
	e2.grid(row=2, column=1)
	e3.grid(row=3, column=1)

#=================== Check Out and Log ======================

	def checkoutlog():
			tech = e1.get()
			user = e2.get()
			asset = e3.get()
			formData = [{
				"Tech": tech.replace("N", ""),
				"User": user.replace("N", ""),
				"AssetTag": asset,
				"Date": get_date_time(),
				"Time":  get_time(),
				"Status": "Checked Out"
			}] 
			#"Tech": e1.get(), "User": e2.get(), "AssetTag": e3.get(), "Time": get_date_time(), get_time()

			with open('Log.json') as data_file:
				old_data = json.load(data_file)
			data = (old_data, formData)

			with open('Log.json', 'w') as outfile:
				json.dump(data, outfile, indent=4,)

	def checkoutasset():
		assettag = e3.get()
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("SELECT * FROM assets WHERE asset = :asset",
		{
		'asset': str(assettag)
		})
		assetinfo = ''
		typeinfo = ''
		maninfo = ''
		modinfo = ''
		records = c.fetchall()
		for record in records:
			assetinfo += str(record[0])
			typeinfo += str(record[1])
			maninfo += str(record[2])
			modinfo += str(record[3])
		

		with conn:
			c.execute("INSERT INTO checkedout VALUES (:asset, :type, :manufacturer, :model)",
			{
				'asset': assetinfo,
				'type': typeinfo,
				'manufacturer': maninfo,
				'model': modinfo
			})
			c.execute("DELETE FROM checkedin WHERE asset = :asset",
			{
			'asset': str(assettag)
			})

		print(assetinfo + " " + typeinfo + " " + maninfo + " " + modinfo)

		conn.commit()
		conn.close()

	def checkoutassettest():
		assettag = e3.get()
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("SELECT * FROM assets WHERE asset = :asset",
		{
		'asset': str(assettag)
		})
		records = c.fetchall()
		assetinfo = ''
		typeinfo = ''
		maninfo = ''
		modinfo = ''
		for record in records:
			assetinfo += str(record[0])
			typeinfo += str(record[1])
			maninfo += str(record[2])
			modinfo += str(record[3])
		print(e3.get())
		
		print(records)

	buttoncheckout = tk.Button(frame4, text='Check Out', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[checkoutasset(), checkoutlog()]).grid(row=4)
	buttoncloseout = tk.Button(frame4, text='Close', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[win4.destroy(), window.mainloop()]).grid(row=4, column=2)
	buttoncheckouttest = tk.Button(frame4, text='Check Out Test', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[checkoutassettest()]).grid(row=5, columnspan=2)

	win4.mainloop()

#=====================Debug Window=====================
def debugwindow():
	

	win6=Toplevel(window, bg='#121212', bd=0)
	win6.title('Check Out')
	win6.geometry("1200x800")
	win6.resizable(0,0)

	frame6 = tk.Frame(win6, bg='#121212', bd=0)
	frame6.pack(side='top')

	e1label = tk.Label(frame6, text='Asset Tag to Test', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=1, column=0)

	e1 = tk.Entry(frame6, font=("Helvetica", 20))
	e1.grid(row=1, column=1)

	def checkedintest():
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("SELECT *,oid FROM checkedin")
	
		records = c.fetchall()
		print_records = ''
		for record in records:
			print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + " " + str(record[4]) +  "\n"
		tk.Label(frame6, text=print_records, bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=2, columnspan=2)
	
	def checkedouttest():
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("SELECT *,oid FROM checkedout")

		records = c.fetchall()
		print_records = ''
		for record in records:
			print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + " " + str(record[4]) +  "\n"
		tk.Label(frame6, text=print_records, bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=2, columnspan=2)
	
	def deletefromcheckedin():
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("DELETE FROM checkedin WHERE oid = 2")
		conn.commit()
		conn.close()
	
	def deletefromcheckedout():
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		c.execute("DELETE FROM checkedout WHERE oid = 6")
		
		conn.commit()
		
		conn.close()
	tk.Label(frame6, text='\n' + '\n' '\n' + '\n' '\n' + '\n' 'Debug' + '\n' + '\n', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=0, columnspan=2)
	
	
	assettestbutton = tk.Button(frame6, text='Get Checkout DB', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[checkedouttest()]).grid(row=5, column=0)
	assettestbutton2 = tk.Button(frame6, text='Get Checkin DB', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[checkedintest()]).grid(row=5, column=1)
	checkedinbutton = tk.Button(frame6, text='Checkin Delete', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[deletefromcheckedin()]).grid(row=7, column=0)
	checkedoutbutton = tk.Button(frame6, text='Check Out Delete', bg='#03DAC6', font=("Helvetica", 20), command=deletefromcheckedout).grid(row=7, column=1)
	delete_boxlabel = tk.Label(frame6, text='Delete ID #', bg='#03DAC6', font=("Helvetica", 20)).grid(row=6, column=0)
	delete_box = tk.Entry(frame6, font=("Helvetica", 20)).grid(row=6, column=1)

	win6.mainloop()

#=====================Inventory Window=====================
def inventorywindow():
	

	win5=Toplevel(window, bg='#121212', bd=0)
	win5.title('Check Out')
	win5.geometry("1200x800")
	win5.resizable(0,0)

	frame5 = tk.Frame(win5, bg='#121212', bd=0)
	frame5.pack(side='top')

	tk.Label(frame5, text='\n' + '\n' '\n' + '\n' '\n' + '\n' 'Update Inventory' + '\n' + '\n', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=0, columnspan=2)
	tk.Label(frame5, text='Asset', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=1)
	tk.Label(frame5, text='Type', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=2)
	tk.Label(frame5, text='Manufacturer', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=3)
	tk.Label(frame5, text='Model', bg='#121212', fg='white', font=("Helvetica", 20)).grid(row=4)

	e1 = tk.Entry(frame5, font=("Helvetica", 20))
	e2 = tk.Entry(frame5, font=("Helvetica", 20))
	e3 = tk.Entry(frame5, font=("Helvetica", 20))
	e4 = tk.Entry(frame5, font=("Helvetica", 20))

	e1.grid(row=1, column=1)
	e2.grid(row=2, column=1)
	e3.grid(row=3, column=1) 
	e4.grid(row=4, column=1) 

#==========Create Inventory/Edit Inventory=================
	def createinv():
		conn = sqlite3.connect('inventory.db')
		c = conn.cursor()
		assetinfo = e1.get()
		typeinfo = e2.get()
		maninfo = e3.get()
		modinfo = e4.get()

		with conn:
			c.execute("INSERT INTO assets VALUES (:asset, :type, :manufacturer, :model)",
			{
				'asset': assetinfo,
				'type': typeinfo,
				'manufacturer': maninfo,
				'model': modinfo
			})
			c.execute("INSERT INTO checkedin VALUES (:asset, :type, :manufacturer, :model)",
			{
				'asset': assetinfo,
				'type': typeinfo,
				'manufacturer': maninfo,
				'model': modinfo
			})
		conn.commit()
		conn.close()


	buttonaddinventory = tk.Button(frame5, text='Create Inventory', bg='#03DAC6', font=("Helvetica", 20), command=createinv).grid(row=6)
	buttoncloseout = tk.Button(frame5, text='Close', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[win5.destroy(),window.mainloop()]).grid(row=6, column=2)

	win5.mainloop()

#====================Available Devices=====================
def status():
	win7=Toplevel(window, bg='#121212', bd=0)
	win7.title('Status')
	win7.geometry("1200x800")
	win7.resizable(0,0)

	frame7 = tk.Frame(win7, bg='#121212', bd=0)
	frame7.pack(side='bottom')

	lowerFrame = tk.LabelFrame(win7, text="Checked In", font=('OpenSans-Light', 15, 'bold'), bg="#FB4E14", width=800, height=500, bd=8.5, relief='flat', padx=5, pady=5)
	lowerFrame.pack(side='left', anchor='n')#, relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6)

	lowerFrame2 = tk.LabelFrame(win7, text="Checked Out", font=('OpenSans-Light', 15, 'bold'), bg="#FB4E14", width=500, height=500, bd=8.5, relief='flat', padx=5, pady=5)
	lowerFrame2.pack(side='right', anchor='n')#, relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6)

	display = tk.Button(frame7, text='Display', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[checkedin(), checkedout()]).grid(row=0)
	
# ============== Checkin Table =======================
	def checkedin():
			conn = sqlite3.connect('inventory.db')
			c = conn.cursor()
			c.execute("SELECT * FROM checkedin")
		
			records = c.fetchall()
			print_records = ''
			for record in records:
				print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) +  "\n"
			tk.Label(lowerFrame, text=print_records, bg='#121212', fg='white', font=("Helvetica", 20), pady=30, padx=30).grid(row=2, columnspan=2)


# ============ Checkout Table =======================
	def checkedout():
			conn = sqlite3.connect('inventory.db')
			c = conn.cursor()
			c.execute("SELECT * FROM checkedout")

			records = c.fetchall()
			print_records = ''
			for record in records:
				print_records += str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) +  "\n"
			tk.Label(lowerFrame2, text=print_records, bg='#121212', fg='white', font=("Helvetica", 20), pady=30, padx=30).grid(row=2, columnspan=2)


	close = tk.Button(frame7, text='Close', bg='#03DAC6', font=("Helvetica", 20), command=lambda:[win7.destroy()]).grid(row=1, columnspan=4)
	win7.mainloop()
	
'''df = pd.read_json(assets)
df1 = pd.DataFrame(df[df['CheckedIn/Out'] == 'Checked In'])
df2 = pd.DataFrame(df[df['CheckedIn/Out'] == 'Checked Out'])
print(df1[tableData])
checkedinTable['text']=df1[tableData]
checkedoutTable['text']=df2[tableData]'''
# ========================GUI==============================

window = Tk()
window.title("Kody Systems Inventory Management")
window.geometry("1200x800")
window.resizable(0,0)
window.configure(bg='#121212', bd=28)

frame = tk.Frame(window, bg='#121212')
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

updateinventorybutton = tk.Button(frame, text='Update Inventory', bg='#03DAC6', font=("Helvetica", 20), relief='sunken', command=inventorywindow, pady=20)
updateinventorybutton.pack(side='bottom',fill='both')

checkinbutton = tk.Button(frame, text='Check In', bg='#03DAC6', font=("Helvetica", 20), relief='sunken', command=checkinwindow, pady=20)
checkinbutton.pack(side='bottom', fill='both')

checkoutbutton = tk.Button(frame, text="Checkout", bg='#03DAC6', font=("Helvetica", 20), relief='sunken', command=checkoutwindow, pady=20)
checkoutbutton.pack(side='bottom',fill='both')

adduserbutton = tk.Button(frame, text='Add User', bg='#03DAC6', font=("Helvetica", 20), relief='sunken', command=adduserwindow, pady=20)
adduserbutton.pack(side='bottom',fill='both')

'''assettestbutton = tk.Button(frame, text='assettest', bg='#03DAC6', font=("Helvetica", 20), command=debugwindow, pady=20)
assettestbutton.pack(side='bottom', fill='both')'''

statusbutton = tk.Button(frame, text='Current Asset Status', bg='#03DAC6', font=("Helvetica", 20), command=status, pady=20)
statusbutton.pack(side='top', fill='both')


window.mainloop()