import tkinter
import math

#  Math Helper Functions (Degrees) 
def sin_deg(x):
    return math.sin(math.radians(x))

def cos_deg(x):
    return math.cos(math.radians(x))

def tan_deg(x):
    return math.tan(math.radians(x))

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return f"{num: .15g}"

#  UI Configuration 
COLOR_BACKGROUND = "#202124"
COLOR_DISPLAY = "#202124"
COLOR_DISPLAY_TEXT = "#FFFFFF"
COLOR_DIGIT_BG = "#3c4043"
COLOR_DIGIT_FG = "#E8EAED"
COLOR_OPERATOR_BG = "#4285F4"
COLOR_OPERATOR_FG = "#FFFFFF"
COLOR_SPECIAL_BG = "#5f6368"
COLOR_SPECIAL_FG = "#E8EAED"

button_values = [
    ["sin", "cos", "tan", "√"],
    ["(", ")", "AC", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="] 
]

right_symbols = ["÷", "×", "-", "+", "="]
func_symbols = ["sin", "cos", "tan", "√", "(", ")", "⌫"]
top_symbols = ["AC"]

row_count = len(button_values)
column_count = len(button_values[0])

#  Window Setup 
window = tkinter.Tk()
window.title("Scientific Calculator")
window.config(bg=COLOR_BACKGROUND)
window.minsize(300, 450)

frame = tkinter.Frame(window, bg=COLOR_BACKGROUND)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frame.grid(row=0, column=0, sticky="nsew")

#  Display Label 
label = tkinter.Label(frame, text="0", font=("Arial", 60), 
                      background=COLOR_DISPLAY,
                      foreground=COLOR_DISPLAY_TEXT, 
                      anchor="e", padx=20,
                      wraplength=1000)
label.grid(row=0, column=0, columnspan=column_count, sticky="nsew", ipady=20)

#  Core Logic Functions 
def calculate():
    global label
    expression = label["text"]
    
    try:
        safe_expression = expression.replace("×", "*").replace("÷", "/").replace("√", "sqrt")

        safe_globals = {
            "__builtins__": {},
            "sin": sin_deg,
            "cos": cos_deg,
            "tan": tan_deg,
            "sqrt": math.sqrt
        }
        
        result = eval(safe_expression, safe_globals, {})
        label["text"] = remove_zero_decimal(result)

    except ZeroDivisionError:
        label["text"] = "Error: Div by 0"
    except Exception as e:
        label["text"] = "Error"
        print(f"Calculation Error: {e}")

def button_clicked(value):
    global label
    current_expression = label["text"]

    if current_expression == "Error" or current_expression == "Error: Div by 0":
        current_expression = "0"

    if value == "AC":
        label["text"] = "0"
    elif value == "⌫":
        if len(current_expression) > 1:
            label["text"] = current_expression[:-1]
        else:
            label["text"] = "0"
    elif value == "=":
        calculate()
    elif value in ["sin", "cos", "tan", "√"]:
        if current_expression == "0":
            label["text"] = value + "("
        else:
            label["text"] += value + "("
    else:
        if current_expression == "0":
            label["text"] = value
        else:
            label["text"] += value

#  Configure Frame Grid Weights 
frame.grid_rowconfigure(0, weight=1)
for row in range(row_count):
    frame.grid_rowconfigure(row + 1, weight=1)
for col in range(column_count):
    frame.grid_columnconfigure(col, weight=1)

#  Button Creation Loop 

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]

        button = tkinter.Button(frame, text=value, font=("Arial", 24, "bold"),
                                borderwidth=0,
                                command=lambda value=value: button_clicked(value))
        
        if value in top_symbols or value in func_symbols:
            button.config(foreground=COLOR_SPECIAL_FG, background=COLOR_SPECIAL_BG)
        elif value in right_symbols:
            button.config(foreground=COLOR_OPERATOR_FG, background=COLOR_OPERATOR_BG)
        else:
            button.config(foreground=COLOR_DIGIT_FG, background=COLOR_DIGIT_BG)
        
        # This grid call is now simpler and correct
        button.grid(row=row+1, column=column, columnspan=1, 
                    sticky="nsew", 
                    padx=1, pady=1)

# Run Code
window.mainloop()