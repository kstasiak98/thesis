import tkinter as tk
import xml.etree.ElementTree as ET

class InstructionApplication:
    def __init__(self, root, instructions):
        self.root = root
        self.instructions = instructions
        self.roles = self.get_roles()
        self.labels = []
        self.buttons = []
        self.last_clicked = {}

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP)

        self.label_frame = tk.Frame(root)
        self.label_frame.pack(side=tk.BOTTOM)

        self.create_buttons()
        self.create_labels()

    def get_roles(self):
        roles = set()
        for instruction in self.instructions:
            _, instruction_roles = instruction
            for role in instruction_roles:
                roles.add(role)

        return roles

    def create_labels(self):
        for idx, instruction in enumerate(self.instructions):
            content, _ = instruction
            label = tk.Label(self.label_frame, text=f"Instruction {idx+1}: {content}")
            label.pack()
            self.labels.append(label)

    def create_buttons(self):
        for i, role in enumerate(self.roles):
            button = tk.Button(self.button_frame, text=role, command=lambda role=role: self.toggle_role(role))
            button.grid(row=0, column=i)
            self.buttons.append(button)
            self.last_clicked[role] = False  # Initially, no button is clicked

    def toggle_role(self, role):
        if self.last_clicked[role]:
            # If the button was previously clicked, show all instructions
            for label in self.labels:
                label.config(fg='black')
            self.last_clicked[role] = False
        else:
            # If the button was not previously clicked, hide non-matching instructions
            for label, instruction in zip(self.labels, self.instructions):
                _, instruction_roles = instruction
                if role in instruction_roles:
                    label.config(fg='black')
                else:
                    label.config(fg='gray')
            self.last_clicked[role] = True

def load_instructions(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    instructions = []

    for instruction in root.findall('instruction'):
        content = instruction.find('content').text
        role_elems = instruction.find('roles').findall('role')
        instruction_roles = [role.text for role in role_elems]

        instructions.append((content, instruction_roles))

    return instructions

def main():
    instructions = load_instructions('instructions.xml')

    root = tk.Tk()
    app = InstructionApplication(root, instructions)
    root.mainloop()

if __name__ == "__main__":
    main()