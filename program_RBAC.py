import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET

def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    role_dict = {}
    for role in root.findall('Role'):
        role_name = role.get('name')
        instructions = [instr.text for instr in role.findall('Instruction')]
        role_dict[role_name] = instructions

    return role_dict

def on_role_checked(event):
    lb_instructions.delete(0, tk.END)
    selected_role = [var.get() for var in cb_vars if var.get()]
    if not selected_role:
        return
    instructions = role_dict.get(selected_role[0], [])
    for instruction in instructions:
        lb_instructions.insert(tk.END, instruction)

root = tk.Tk()

role_dict = load_xml('roles.xml')  # load XML file

cb_vars = []
for role in role_dict.keys():
    var = tk.StringVar()
    cb = ttk.Checkbutton(root, text=role, variable=var, onvalue=role, offvalue="")
    var.trace_add('write', on_role_checked)
    cb_vars.append(var)
    cb.pack()

lb_instructions = tk.Listbox(root)
lb_instructions.pack()

root.mainloop()
