import tkinter as tk
from tkinter import ttk
import math
import re

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        
        # Calculator state
        self.current_input = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.memory = 0
        self.history = []
        self.is_scientific = False
        
        # Color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'display_bg': '#2d2d2d',
            'display_text': '#ffffff',
            'number_bg': '#404040',
            'number_hover': '#505050',
            'operator_bg': '#ff9500',
            'operator_hover': '#ffad33',
            'function_bg': '#505050',
            'function_hover': '#606060',
            'equals_bg': '#ff9500',
            'equals_hover': '#ffad33',
            'text_color': '#ffffff'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.bind_keyboard()
    
    def setup_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Number.TButton',
                       background=self.colors['number_bg'],
                       foreground=self.colors['text_color'],
                       font=('Arial', 14, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Number.TButton',
                 background=[('active', self.colors['number_hover'])])
        
        style.configure('Operator.TButton',
                       background=self.colors['operator_bg'],
                       foreground=self.colors['text_color'],
                       font=('Arial', 14, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Operator.TButton',
                 background=[('active', self.colors['operator_hover'])])
        
        style.configure('Function.TButton',
                       background=self.colors['function_bg'],
                       foreground=self.colors['text_color'],
                       font=('Arial', 12, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Function.TButton',
                 background=[('active', self.colors['function_hover'])])
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🧮 Advanced Calculator", 
                              font=('Arial', 16, 'bold'), 
                              bg=self.colors['bg'], fg=self.colors['text_color'])
        title_label.pack(pady=(0, 10))
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg=self.colors['display_bg'], 
                                relief=tk.RAISED, bd=2)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # History display (small)
        self.history_var = tk.StringVar()
        history_label = tk.Label(display_frame, textvariable=self.history_var,
                                font=('Arial', 10), bg=self.colors['display_bg'],
                                fg='#888888', anchor='e', justify='right')
        history_label.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Main display
        display_label = tk.Label(display_frame, textvariable=self.display_var,
                                font=('Arial', 24, 'bold'), bg=self.colors['display_bg'],
                                fg=self.colors['display_text'], anchor='e',
                                justify='right', height=2)
        display_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Mode toggle frame
        mode_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.mode_btn = tk.Button(mode_frame, text="Scientific Mode",
                                 command=self.toggle_mode,
                                 bg=self.colors['function_bg'],
                                 fg=self.colors['text_color'],
                                 font=('Arial', 10, 'bold'),
                                 relief=tk.FLAT, pady=5)
        self.mode_btn.pack(side=tk.LEFT)
        
        # Memory indicators
        self.memory_label = tk.Label(mode_frame, text="M: 0",
                                    font=('Arial', 10), bg=self.colors['bg'],
                                    fg='#888888')
        self.memory_label.pack(side=tk.RIGHT)
        
        # Button container
        self.button_container = tk.Frame(main_frame, bg=self.colors['bg'])
        self.button_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_basic_buttons()
    
    def create_basic_buttons(self):
        # Clear existing buttons
        for widget in self.button_container.winfo_children():
            widget.destroy()
        
        if not self.is_scientific:
            self.create_standard_layout()
        else:
            self.create_scientific_layout()
    
    def create_standard_layout(self):
        buttons = [
            ['MC', 'MR', 'M+', 'M-', 'AC'],
            ['±', '%', '√', '÷', '⌫'],
            ['7', '8', '9', '×', '('],
            ['4', '5', '6', '−', ')'],
            ['1', '2', '3', '+', 'x²'],
            ['0', '00', '.', '=', '1/x']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                self.create_button(btn_text, i, j)
    
    def create_scientific_layout(self):
        buttons = [
            ['sin', 'cos', 'tan', 'ln', 'log'],
            ['x^y', '√', 'x²', 'x³', '!'],
            ['MC', 'MR', 'M+', 'M-', 'AC'],
            ['π', 'e', '(', ')', '⌫'],
            ['7', '8', '9', '÷', 'mod'],
            ['4', '5', '6', '×', 'abs'],
            ['1', '2', '3', '−', '±'],
            ['0', '00', '.', '+', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                self.create_button(btn_text, i, j, scientific=True)
    
    def create_button(self, text, row, col, scientific=False):
        # Determine button style and command
        if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '00', '.']:
            style = 'Number.TButton'
            cmd = lambda t=text: self.on_number_click(t)
        elif text in ['+', '−', '×', '÷', '=']:
            style = 'Operator.TButton'
            cmd = lambda t=text: self.on_operator_click(t)
        else:
            style = 'Function.TButton'
            cmd = lambda t=text: self.on_function_click(t)
        
        btn = ttk.Button(self.button_container, text=text, style=style,
                        command=cmd)
        
        # Special sizing for some buttons
        colspan = 2 if text in ['0', '00'] else 1
        btn.grid(row=row, column=col, columnspan=colspan, 
                sticky='nsew', padx=1, pady=1)
        
        # Configure grid weights
        self.button_container.grid_rowconfigure(row, weight=1)
        self.button_container.grid_columnconfigure(col, weight=1)
    
    def on_number_click(self, number):
        if self.display_var.get() == "0" or self.display_var.get() == "Error":
            self.current_input = number
        else:
            self.current_input += number
        self.update_display()
    
    def on_operator_click(self, operator):
        if operator == '=':
            self.calculate()
        else:
            # Convert display operators to calculation operators
            op_map = {'×': '*', '÷': '/', '−': '-'}
            calc_op = op_map.get(operator, operator)
            
            if self.current_input and not self.current_input.endswith(('+', '-', '*', '/')):
                self.current_input += calc_op
                self.update_display()
    
    def on_function_click(self, function):
        try:
            if function == 'AC':
                self.clear_all()
            elif function == '⌫':
                self.backspace()
            elif function == '±':
                self.toggle_sign()
            elif function == '%':
                self.percentage()
            elif function == '√':
                self.square_root()
            elif function == 'x²':
                self.square()
            elif function == '1/x':
                self.reciprocal()
            elif function == 'MC':
                self.memory_clear()
            elif function == 'MR':
                self.memory_recall()
            elif function == 'M+':
                self.memory_add()
            elif function == 'M-':
                self.memory_subtract()
            elif function in ['(', ')']:
                self.current_input += function
                self.update_display()
            # Scientific functions
            elif function == 'sin':
                self.apply_trig_function(math.sin)
            elif function == 'cos':
                self.apply_trig_function(math.cos)
            elif function == 'tan':
                self.apply_trig_function(math.tan)
            elif function == 'ln':
                self.natural_log()
            elif function == 'log':
                self.log_base_10()
            elif function == 'x^y':
                self.current_input += '**'
                self.update_display()
            elif function == 'x³':
                self.cube()
            elif function == '!':
                self.factorial()
            elif function == 'π':
                self.add_constant(math.pi)
            elif function == 'e':
                self.add_constant(math.e)
            elif function == 'mod':
                self.current_input += '%'
                self.update_display()
            elif function == 'abs':
                self.absolute_value()
                
        except Exception as e:
            self.display_var.set("Error")
    
    def clear_all(self):
        self.current_input = ""
        self.display_var.set("0")
        self.history_var.set("")
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.display_var.set("0")
            else:
                self.update_display()
    
    def toggle_sign(self):
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        try:
            if self.current_input:
                result = float(eval(self.current_input)) / 100
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def square_root(self):
        try:
            if self.current_input:
                result = math.sqrt(float(eval(self.current_input)))
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def square(self):
        try:
            if self.current_input:
                result = float(eval(self.current_input)) ** 2
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def cube(self):
        try:
            if self.current_input:
                result = float(eval(self.current_input)) ** 3
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def reciprocal(self):
        try:
            if self.current_input:
                result = 1 / float(eval(self.current_input))
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def factorial(self):
        try:
            if self.current_input:
                num = int(float(eval(self.current_input)))
                if num < 0:
                    self.display_var.set("Error")
                else:
                    result = math.factorial(num)
                    self.current_input = str(result)
                    self.update_display()
        except:
            self.display_var.set("Error")
    
    def apply_trig_function(self, func):
        try:
            if self.current_input:
                # Convert to radians for calculation
                radians = math.radians(float(eval(self.current_input)))
                result = func(radians)
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def natural_log(self):
        try:
            if self.current_input:
                result = math.log(float(eval(self.current_input)))
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def log_base_10(self):
        try:
            if self.current_input:
                result = math.log10(float(eval(self.current_input)))
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def absolute_value(self):
        try:
            if self.current_input:
                result = abs(float(eval(self.current_input)))
                self.current_input = str(result)
                self.update_display()
        except:
            self.display_var.set("Error")
    
    def add_constant(self, constant):
        if self.display_var.get() == "0":
            self.current_input = str(constant)
        else:
            self.current_input += str(constant)
        self.update_display()
    
    def memory_clear(self):
        self.memory = 0
        self.update_memory_display()
    
    def memory_recall(self):
        self.current_input = str(self.memory)
        self.update_display()
    
    def memory_add(self):
        try:
            if self.current_input:
                self.memory += float(eval(self.current_input))
                self.update_memory_display()
        except:
            pass
    
    def memory_subtract(self):
        try:
            if self.current_input:
                self.memory -= float(eval(self.current_input))
                self.update_memory_display()
        except:
            pass
    
    def update_memory_display(self):
        self.memory_label.config(text=f"M: {self.memory:.4g}")
    
    def calculate(self):
        try:
            if self.current_input:
                # Store the expression for history
                expression = self.current_input
                
                # Replace display operators with Python operators
                calc_expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                
                # Evaluate the expression
                result = eval(calc_expression)
                
                # Add to history
                self.history.append(f"{expression} = {result}")
                if len(self.history) > 5:
                    self.history.pop(0)
                
                # Update displays
                self.history_var.set(expression + " =")
                self.current_input = str(result)
                self.update_display()
                
        except Exception as e:
            self.display_var.set("Error")
    
    def update_display(self):
        if self.current_input:
            # Format display with proper operators
            display_text = self.current_input.replace('*', '×').replace('/', '÷').replace('-', '−')
            self.display_var.set(display_text)
        else:
            self.display_var.set("0")
    
    def toggle_mode(self):
        self.is_scientific = not self.is_scientific
        if self.is_scientific:
            self.mode_btn.config(text="Standard Mode")
            self.root.geometry("400x800")
        else:
            self.mode_btn.config(text="Scientific Mode")
            self.root.geometry("400x650")
        
        self.create_basic_buttons()
    
    def bind_keyboard(self):
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def on_key_press(self, event):
        key = event.char
        if key.isdigit():
            self.on_number_click(key)
        elif key in ['+', '-', '*', '/']:
            operator_map = {'*': '×', '/': '÷', '-': '−'}
            self.on_operator_click(operator_map.get(key, key))
        elif key == '.':
            self.on_number_click('.')
        elif key == '=' or event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.clear_all()

def main():
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
