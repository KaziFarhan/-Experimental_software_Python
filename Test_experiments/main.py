from tkinter import *
import data_manager
from functools import partial
from datetime import date
from time import sleep

dates_labels=[]
names_labels=[]
amount_labels=[]
balance_labels=[]
edit_buttons=[]
show_balance_label=[]
deleat_buttons=[]
event=0
error_defender = []
edit_manager=[]

date_of_transition, name_of_transition, amount_of_transition, amount_of_balance = data_manager.csv_reader()

def display_data():
	global date_of_transition, name_of_transition, amount_of_transition, amount_of_balance 
	for i in range(len(date_of_transition)):
		
		dates_labels.append(Label(frame1,bg='snow',text=date_of_transition[i]))
		dates_labels[i].grid(row=i+2,column=0)

		names_labels.append(Label(frame1,bg='snow',text=name_of_transition[i]))
		names_labels[i].grid(row=i+2,column=1)

		amount_labels.append(Label(frame1,bg='snow',text=amount_of_transition[i]))
		amount_labels[i].grid(row=i+2,column=2)

		balance_labels.append(Label(frame1,bg='snow',text=amount_of_balance[i]))
		balance_labels[i].grid(row=i+2,column=3)

		edit_buttons.append(Button(frame1,text='EDIT',command=partial(edit,i,date_of_transition, name_of_transition, amount_of_transition)))
		edit_buttons[i].grid(row=i+2,column=4)

		deleat_buttons.append(Button(frame3,text='D',bg='black',fg='red',command=partial(terminate,i)))
		deleat_buttons[i].grid(row=i+2,column=0)

	show_balance_label.append(Label(frame2,bg='snow', width=15, fg='green',font=(None,17)))
	show_balance_label[0].grid(row=1,column=2)
	try:
		show_balance_label[0].configure(text=amount_of_balance[-1])
	except:
		pass

error_avoit_local=[]
def edit(i,date_of_transition, name_of_transition, amount_of_transition):
	global event
	global error_avoit_local
	for a in range(len(error_defender)):
		print('loop')
		print(a)
		print(error_defender[a])
		if a < error_defender[a]:
			i-=1
			error_avoit_local.append(a)
			print('done')


	if event==0:
		edit_date_containor=Entry(frame1,width=9)
		edit_name_containor=Entry(frame1,width=10)
		edit_amount_containor=Entry(frame1,width=7)
		#edit_balance_containor=Entry(frame1,width=10)	

		edit_date_containor.grid(row=i+2-len(error_avoit_local),column=0)
		edit_name_containor.grid(row=i+2-len(error_avoit_local),column=1)
		edit_amount_containor.grid(row=i+2-len(error_avoit_local),column=2)
		#edit_balance_containor.grid(row=i+2,column=3)
		
		print(error_defender)


		print(i)
		edit_date_containor.insert(0,date_of_transition[i])
		edit_name_containor.insert(0,name_of_transition[i])
		edit_amount_containor.insert(0,amount_of_transition[i])
		#edit_balance_containor.insert(0,amount_of_balance[i])

		edit_buttons[i].configure(text='SAVE',command=lambda:save(i,edit_date_containor,edit_name_containor,edit_amount_containor,date_of_transition, name_of_transition, amount_of_transition))

		event=1		
	else:
		edit_manager.append(Frame(bg='snow'))
		edit_manager[0].grid(row=2,column=0,columnspan=2)
		edit_manager.append(Label(edit_manager[0], bg='snow', text='First Save The File You are Editing !! ', fg='red'))
		edit_manager[1].pack()
		
def save(i,get_date,get_name,get_amount,edit_date_containor,edit_name_containor,edit_amount_containor):
		global event, amount_of_balance
		global edit_manager, error_avoit_local

		try:
			edit_manager[0].destroy()
			edit_manager[1].destroy()
			del edit_manager[0]
			del edit_manager[1]
		except:
			pass
		edit_date_containor[i]=get_date.get()
		edit_name_containor[i]=get_name.get()
		edit_amount_containor[i]=get_amount.get()

		new_dates,new_names,new_ammount,new_balances =  data_manager.csv_write(edit_date_containor,edit_name_containor,edit_amount_containor)

		dates_labels[i].configure(text=new_dates[i])
		names_labels[i].configure(text=new_names[i])
		amount_labels[i].configure(text=new_ammount[i])

		edit_buttons[i].configure(text="EDIT",command=partial(edit,i,new_dates,new_names,new_ammount))

		for r in range(len(new_dates)):
			balance_labels[r].configure(text=new_balances[r-len(error_avoit_local)])

		get_date.destroy()
		get_name.destroy()
		get_amount.destroy()

		show_balance_label[0].configure(text=new_balances[-1])
		
		event=0

		for u in range(len(error_avoit_local)-1):
			del error_avoit_local[u]

def add_transition():
	master=Tk()
	Label(master,bg='snow',text='Enter Transition name : ').grid(row=0,column=0)
	Label(master,bg='snow',text='Enter Transition amount : ').grid(row=1,column=0)
	new_name_to_add=Entry(master)
	new_amount_to_add=Entry(master)
	new_name_to_add.grid(row=0,column=1)
	new_amount_to_add.grid(row=1,column=1)
	Button(master,text='Add',command=lambda:add_transition_main(new_name_to_add.get(),new_amount_to_add.get(),master),width=20).grid(row=2,column=1)
	master.mainloop()

def add_transition_main(name,amount,master):
	global date_of_transition, name_of_transition, amount_of_transition, amount_of_balance
	global dates_labels,names_labels,amount_labels,balance_labels,edit_buttons,show_balance_label

	date_of_transition, name_of_transition, amount_of_transition, amount_of_balance = data_manager.csv_append(date.today(),name,amount)
	for i in range(len(dates_labels)):
		del dates_labels[0]
		del	names_labels[0]
		del	amount_labels[0]
		del	balance_labels[0]
		del	edit_buttons[0]

	del	show_balance_label[0]

	display_data()
	master.destroy()

def terminate(i):
	global date_of_transition, name_of_transition, amount_of_transition, amount_of_balance
	global dates_labels,names_labels,amount_labels,balance_labels,edit_buttons
	global error_defender
	error_defender.append(i)

	for t in error_defender:
		if i > t:
			i-=1

	del date_of_transition[i] 
	del name_of_transition[i] 
	del amount_of_transition[i] 
	del amount_of_balance[i]	
	
	date_of_transition, name_of_transition, amount_of_transition, amount_of_balance = data_manager.csv_write(date_of_transition,name_of_transition,amount_of_transition)

	dates_labels[i].destroy()
	names_labels[i].destroy()
	amount_labels[i].destroy()
	balance_labels[i].destroy()
	edit_buttons[i].destroy()
	deleat_buttons[i].destroy()

	del dates_labels[i]
	del names_labels[i]
	del amount_labels[i]
	del balance_labels[i]
	del edit_buttons[i]
	del deleat_buttons[i]

	try:
		show_balance_label[0].configure(text=amount_of_balance[-1])
	except:
		show_balance_label[0].configure(text=0)
	
	
	for r in range(len(balance_labels)):
		balance_labels[r].configure(text=amount_of_balance[r])
	

root=Tk()
root.resizable(False,False)	
frame1 = Frame(bg='snow')
frame1.grid(row=0,column=0)

																														   		
Label(frame1,bg='snow',text='------------Date-------------Transitin Type---------------Transition Ammount----------------Balance                           EDIT           ').grid(row=0,column=0,columnspan=5)
Label(frame1,bg='snow',text='____________________________________________________________________________________________________________________________________________').grid(row=1,column=0,columnspan=5)

frame2 = Frame(bg='snow')
frame2.grid(row=1,column=0,columnspan=2)

frame3 = Frame(bg='snow')
frame3.grid(row=0,column=1)
Label(frame3,bg='snow',text='Deleat').grid(row=0,column=0)
Label(frame3,bg='snow',text='_________________').grid(row=1,column=0)

display_data()

Label(frame2,bg='snow',text="__________________________________________________________________________________________________________________________________________________________").grid(row=0,column=0,columnspan=3)
Add_transition_button=Button(frame2,text='ADD TRANSITION',font=(None,13),bg='blue',command=lambda:add_transition())
Add_transition_button.grid(row=1,column=0)

root.bind('<Control-w>',exit)
root.mainloop()