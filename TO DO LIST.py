
import tkinter as tk

app = tk.Tk()
app.title("My To-Do List")
app.geometry("400x450")
app.configure(bg="#F0FDF4")

def add_task():
    task = entry.get()

    if task:
        task_list.insert(tk.END, task)
        entry.delete(0, tk.END)

def delete_task():
    selected = task_list.curselection()

    if selected:
        task_list.delete(selected)

def complete_task():
    selected = task_list.curselection()

    if selected:
        task = task_list.get(selected)
        task_list.delete(selected)
        task_list.insert(tk.END, "✓ " + task)

tk.Label(app, text="MY TO-DO LIST",
         font=("Arial", 20, "bold"),
         bg="#F0FDF4").pack(pady=20)

entry = tk.Entry(app, width=30, font=("Arial", 12))
entry.pack(pady=10)

tk.Button(app, text="Add Task",
          command=add_task,
          bg="#16A34A", fg="white").pack(pady=5)

task_list = tk.Listbox(app, width=35, height=12)
task_list.pack(pady=15)

tk.Button(app, text="Complete Task",
          command=complete_task).pack(pady=5)

tk.Button(app, text="Delete Task",
          command=delete_task,
          bg="#DC2626", fg="white").pack(pady=5)

app.mainloop()
