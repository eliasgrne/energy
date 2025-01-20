import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage



#tasks to complete and servers at 30C
tasks_needed_to_be_completed = [f"task{i}" for i in range(1, 41)]
C = 1
servers = servers = [
    ["serv1", 20 * C, []], 
    ["serv2", 20 * C, []], 
    ["serv3", 20 * C, []], 
    ["serv4", 20 * C, []]
]
MAX_TEMP = 29 * C
TTime = 35000  #30 seconds

login_win = tk.Tk()
login_win.title("NetApp Login")
login_win.geometry('500x500')


def login():
    username = "user"
    password = "password"
    global verification  #Make verification global to use it in `verify_code`
    verification = 1234

    if username_entry.get() == username and password_entry.get() == password:
        password_entry.grid_remove()
        password_label.grid_remove()

        #Display verification entry fields
        verification_label = tk.Label(frame, text="Verification Code:", font=("Arial", 16))
        global verification_entry
        verification_entry = tk.Entry(frame)
        verification_label.grid(row=1, column=0)
        verification_entry.grid(row=1, column=1, pady=20)

        EMAIL_label = tk.Label(frame, text="CODE SENT TO YOUR WORK EMAIL", font=("Arial", 16))
        EMAIL_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)

        #Update the button to verify code instead of login
        login_button.config(text="Verify", command=verify_code)

    else:
        messagebox.showerror(title="Error", message="Invalid login")

def verify_code():
    try:
        #Retrieve and compare the verification code entered
        if int(verification_entry.get()) == verification:
            messagebox.showinfo(title="Accepted", message="Welcome NetApp Employee")
            login_win.withdraw()  #hide login window
            open_task_window()
        else:
            messagebox.showerror(title="Error", message="Incorrect verification code. Please try again.")
    except ValueError:
        messagebox.showerror(title="Error", message="Please enter a valid numeric code.")

#set up the main window
def open_task_window():
    main_win = tk.Tk()
    main_win.title("Data Demand")
    main_win.geometry("600x700")

    def complete_task(task):
        for server in servers:
            if server[1] <= MAX_TEMP:
                server[2].append(task)
                server[1] += C
                set_task_removal(server, task)  #call the function to remove task after 30 sec
                break
        display_tasks()  # Update task display after adding a task

    #function to remove tasks after TTime (30 seconds)
    def set_task_removal(server, task):
        main_win.after(TTime, remove_task, server, task)

    #function to delete the task and decrease temp
    def remove_task(server, task):
        server[2].remove(task)
        server[1] -= C 
        display_tasks()

    #function to distribute tasks
    def distribute_tasks():
        if tasks_needed_to_be_completed:
            complete_task(tasks_needed_to_be_completed.pop(0))
            main_win.after(1000, distribute_tasks)  # Distribute next task after 1 second

    #function to update the display
    def display_tasks():
        for widget in main_win.winfo_children():
            widget.destroy()
        #display updated server data
        for server in servers:
            tk.Label(main_win, text=f"{server[0]} - Temperature: {server[1]}°C", font=("Arial", 12)).pack(anchor='w', pady=5)

            task_display = tk.Text(main_win, width=50, height=5, wrap=tk.WORD, font=("Arial", 10))
            task_display.pack(padx=10, pady=5)
            task_display.insert(tk.END, "\n".join([f"  - {task}" for task in server[2]]) or "  No tasks assigned.\n")


    #title
    title_label = tk.Label(main_win, text="Automated Task Distribution Across Servers", font=("Arial", 14))
    title_label.pack(pady=10)
    #start distributing tasks
    main_win.after(1000, distribute_tasks)

    #run
    main_win.mainloop()

frame = tk.Frame(login_win)

# Initial login widgets
login_label = tk.Label(frame, text="Login", font=("Arial", 16))
username_label = tk.Label(frame, text="Username", font=("Arial", 16))
username_entry = tk.Entry(frame)
password_entry = tk.Entry(frame, show="*")
password_label = tk.Label(frame, text="Password", font=("Arial", 16))
login_button = tk.Button(frame, text="Next", font=("Arial", 16), command=login)

# Position widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()

login_win.mainloop()
