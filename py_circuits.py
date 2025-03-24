from time import sleep
from tkinter import *
from tkinter import ttk

from components import resistors
from components import wires
from components import grounds
from components import sources
from components import capacitors
from components import inductors
from circ_engine import steady_state_analysis

moving_list = [0,0,0,0] # to be used for the moving of components
ovals = [] # to be used for the designation of wire connection points
component_stack = [] # a list with all the components inserted by the user
wir = 0 # to be used to designate the first vertice of a wire

def enable_red():
    unbind_everything()
    top_label.config(text="Resistor")
    C.bind("<Button-1>", add_red)

def enable_cap():
    unbind_everything()
    top_label.config(text="Capacitor")
    C.bind("<Button-1>", add_cap)

def enable_ind():
    unbind_everything()
    top_label.config(text="Inductor")
    C.bind("<Button-1>", add_ind)

def display_vertices(event):
    x, y = event.x, event.y
    global ovals, C
    for comp in component_stack:
        for x_index, comp_x in enumerate(comp.x_coord): # search every component in the stack
            if abs(x - comp_x) < 15 and abs(y - comp.y_coord[x_index]) < 15 and not ovals: # if within node, add oval
                new_oval = C.create_oval(comp_x-7, comp.y_coord[x_index]-7, comp_x+7, comp.y_coord[x_index]+7, fill='green', width=3)
                ovals.append(new_oval)
                break
            if (abs(x - comp_x) > 15 or abs(y - comp.y_coord[x_index]) > 15) and ovals: #if outside, delete oval
                C.delete(ovals)
                ovals = []
        if ovals: # only one oval is possible
            break

def add_red(event):
    global C
    res = resistors.res(event.x, event.y, C)
    res.drawit()
    component_stack.append(res)
    res.showname()

def add_cap(event):
    global C
    cap = capacitors.cap(event.x, event.y, C)
    cap.drawit()
    component_stack.append(cap)
    cap.showname()

def add_ind(event):
    global C
    ind = inductors.ind(event.x, event.y, C)
    ind.drawit()
    component_stack.append(ind)
    ind.showname()

def saveposn(event):
    global lastx, lasty, wir, x_cor, y_cor, C
    if wir == 0:
        lastx, lasty = event.x, event.y
        wir = 1
        top_label.config(text="wire 1")
        for comp in component_stack:
            for x_index, comp_x in enumerate(comp.x_coord):
                if abs(lastx - comp_x) < 15 and abs(comp.y_coord[x_index] - lasty) < 15:
                    lastx = comp_x
                    lasty = comp.y_coord[x_index]
    elif wir == 1:
        final_x = event.x
        final_y = event.y
        for comp in component_stack:
            for x_index, comp_x in enumerate(comp.x_coord):
                if abs(final_x - comp_x) < 15 and abs(comp.y_coord[x_index] - final_y) < 15:
                    final_x = comp_x
                    final_y = comp.y_coord[x_index]
        wire = wires.wire(lastx, lasty, final_x, final_y, C)
        wire.drawit()
        top_label.config(text="wir 0")
        component_stack.append(wire)
        wir = 0

def add_wir():
    unbind_everything()
    top_label.config(text = "wir")
    C.bind("<Motion>", display_vertices)
    C.bind("<Button-1>", saveposn)

def clear_everything():
    top_label.config(text = "Clear")
    unbind_everything()
    C.delete('all')

def enable_src():
    unbind_everything()
    top_label.config(text="Src")
    C.bind("<Button-1>", add_src)

def add_src(event):
    global C
    src = sources.source(event.x, event.y, C)
    src.drawit()
    component_stack.append(src)
    src.showname()

def enable_gnd():
    unbind_everything()
    top_label.config(text="Gnd")
    C.bind("<Button-1>", add_gnd)

def add_gnd(event):
    global C
    gnd = grounds.ground(event.x, event.y, C)
    gnd.drawit()
    component_stack.append(gnd)
    gnd.showname()

def enable_set():
    unbind_everything()
    top_label.config(text="Set")
    C.bind("<Button-1>", set_comp)
    C.bind("<B1-Motion>", move_component)
    C.bind("<Double-Button-1>", set_values)
    root.bind('<KeyPress-d>', del_component)
    root.bind('<KeyPress-r>', rot_component)

def set_values(event):
    component_list = [] # the component to be modified

    def get_button_value():
        if component_list[0].name[0] == "R":
            if float(input_field.get()) >= 0:
                component_list[0].resistance = float(input_field.get())
                resistor_name_before = ""
                for i in component_list[0].name:
                    resistor_name_before = resistor_name_before + i
                    if i == " ":
                        break
                component_list[0].name = resistor_name_before + str(component_list[0].resistance)
                component_list[0].showname()
                a.grab_release()
                a.destroy()
        if component_list[0].name[0] == "L":
            if float(input_field.get()) >= 0:
                component_list[0].inductance = float(input_field.get())
                inductance_name_before = ""
                for i in component_list[0].name:
                    inductance_name_before = inductance_name_before + i
                    if i == " ":
                        break
                component_list[0].name = inductance_name_before + str(component_list[0].inductance)
                component_list[0].showname()
                a.grab_release()
                a.destroy()
        if component_list[0].name[0] == "C":
            if float(input_field.get()) >= 0:
                component_list[0].capacitance = float(input_field.get())
                capacitance_name_before = ""
                for i in component_list[0].name:
                    capacitance_name_before = capacitance_name_before + i
                    if i == " ":
                        break
                component_list[0].name = capacitance_name_before + str(component_list[0].capacitance)
                component_list[0].showname()
                a.grab_release()
                a.destroy()
        elif component_list[0].name[0] == "S":
            if float(input_field_1.get()) and (float(input_field_2.get()) >= 0):
                component_list[0].amplitude = float(input_field_1.get())
                source_name_before = ""
                for i in component_list[0].name:
                    source_name_before = source_name_before + i
                    if i == " ":
                        break
                component_list[0].name = source_name_before + str(component_list[0].amplitude)
                #component_list[0].name = component_list[0].name + "V "
                if float(input_field_2.get()) == 0:
                    component_list[0].name = component_list[0].name + " DC"
                else:
                    component_list[0].name = component_list[0].name + " " + str(input_field_2.get()) + " Hz"
                component_list[0].frequency = float(input_field_2.get())
                component_list[0].showname()
                a.grab_release()
                a.destroy()

    for comp in component_stack:
        if comp.hl == 1:
            if comp.name[0] == "R":
                component_list.append(comp)
                a = Toplevel(root)
                a.grab_set()
                label_text = "Resistance (Ohm) = "
                txt = Label(a)
                txt.config(text=label_text)
                txt.grid(column=0, row=0)
                input_field = Entry(a)
                input_field.grid(column=1, row=0)
                btn = Button(a)
                btn.config(text="Submit", command=get_button_value)
                btn.grid(column=0, row=1, columnspan=2)
            elif comp.name[0] == "C":
                component_list.append(comp)
                a = Toplevel(root)
                a.grab_set()
                label_text = "Capacitance (F) = "
                txt = Label(a)
                txt.config(text=label_text)
                txt.grid(column=0, row=0)
                input_field = Entry(a)
                input_field.grid(column=1, row=0)
                btn = Button(a)
                btn.config(text="Submit", command=get_button_value)
                btn.grid(column=0, row=1, columnspan=2)
            elif comp.name[0] == "L":
                component_list.append(comp)
                a = Toplevel(root)
                a.grab_set()
                label_text = "Inductance (H) = "
                txt = Label(a)
                txt.config(text=label_text)
                txt.grid(column=0, row=0)
                input_field = Entry(a)
                input_field.grid(column=1, row=0)
                btn = Button(a)
                btn.config(text="Submit", command=get_button_value)
                btn.grid(column=0, row=1, columnspan=2)
            elif comp.name[0] == "S":
                component_list.append(comp)
                a = Toplevel(root)
                a.grab_set()
                label_text_1 = "Voltage (V) = "
                label_text_2 = "Frequency (Hz) = "
                txt1 = Label(a)
                txt1.config(text=label_text_1)
                txt1.grid(column=0, row=0)
                txt2 = Label(a)
                txt2.config(text=label_text_2)
                txt2.grid(column=0, row=1)
                input_field_1 = Entry(a)
                input_field_1.grid(column=1, row=0)
                input_field_2 = Entry(a)
                input_field_2.grid(column=1, row=1)
                btn = Button(a)
                btn.config(text="Submit", command=get_button_value)
                btn.grid(column=0, row=2, columnspan=2)


def set_comp(event):
    moving_list[2] = event.x
    moving_list[3] = event.y
    cid=C.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
    if not cid:
        cid = (-1, -1) # if empty, assign it an impossible canvas id
    for comp in component_stack:
        hl_var = 0 # this is to mark that a highlighted component has already been encountered
        for line in range(comp.nol):
            if hl_var == 1:
                continue
            if comp.canvas_id[line] == cid[0]:
                comp.highlighted()
                comp.hl = 1
                hl_var = 1
            elif comp.label_id == cid[0]:
                comp.label_hl = 1
                comp.label_highlighted()
                comp.unhighlighted()
                comp.hl = 0
            else:
                comp.unhighlighted()
                comp.hl = 0
                comp.label_unhighlighted()
                comp.label_hl = 0

def del_component(event=None):
    for comp in component_stack:
        if comp.hl:
            comp.selfdelete()
            component_stack.remove(comp)

def rot_component(event=None):
    component_rotated = 0
    for comp in component_stack:
        if comp.name[0] == "W":
            continue
        if comp.hl:
            x_coordinates_before, y_coordinates_before = get_coordinates(comp)
            comp.rotate()
            x_coordinates_after, y_coordinates_after = get_coordinates(comp)
            comp.x_coord = x_coordinates_after
            comp.y_coord = y_coordinates_after
            component_rotated = 1

    for comp in component_stack: # find the connected wires and rotate them
        if comp.name[0] == "W" and component_rotated == 1:
            wire_x, wire_y = get_coordinates(comp)
            for i in range(len(x_coordinates_before)):
                if x_coordinates_before[i] == wire_x[0] and y_coordinates_before[i] == wire_y[0]:
                    C.coords(comp.canvas_id[0], [x_coordinates_after[i], y_coordinates_after[i], wire_x[1], wire_y[1]])
                elif x_coordinates_before[i] == wire_x[1] and y_coordinates_before[i] == wire_y[1]:
                    C.coords(comp.canvas_id[0], [wire_x[0], wire_y[0], x_coordinates_after[i], y_coordinates_after[i]])

def move_component(event):
    component_moved = 0
    moving_list[0] = moving_list[2]
    moving_list[1] = moving_list[3]
    moving_list[2] = event.x
    moving_list[3] = event.y
    x_dif = moving_list[2] - moving_list[0]
    y_dif = moving_list[3] - moving_list[1]
    for comp in component_stack:
        if comp.name[0] == "W":
            continue
        if comp.hl:
            x_coordinates_before, y_coordinates_before = get_coordinates(comp)
            comp.move_comp(x_dif, y_dif)
            x_coordinates_after, y_coordinates_after = get_coordinates(comp)
            comp.x_coord = x_coordinates_after
            comp.y_coord = y_coordinates_after
            component_moved = 1
        elif comp.label_hl == 1:
            comp.move_label(x_dif,y_dif)

    for comp in component_stack: # find the connected wires and move them
        if comp.name[0] == "W" and component_moved == 1:
            wire_x, wire_y = get_coordinates(comp)
            for i in range(len(x_coordinates_before)):
                if x_coordinates_before[i] == wire_x[0] and y_coordinates_before[i] == wire_y[0]:
                    C.coords(comp.canvas_id[0], [x_coordinates_after[i], y_coordinates_after[i], wire_x[1], wire_y[1]])
                elif x_coordinates_before[i] == wire_x[1] and y_coordinates_before[i] == wire_y[1]:
                    C.coords(comp.canvas_id[0], [wire_x[0], wire_y[0], x_coordinates_after[i], y_coordinates_after[i]])


def unbind_everything():
    for widget_list in root.grid_slaves():
        widget_list.unbind("<Button-1>")
        widget_list.unbind("<B1-Motion>")
        widget_list.unbind("<Motion>")
        widget_list.unbind("<Double-Button-1>")

def undo(event=None):
    if not component_stack:
        print("Nothing to undo")
        return None
    global x_cor, y_cor
    component_stack.pop().selfdelete()

def get_coordinates(cnvs): #returns first and last x and y coordinates of component
    global C
    x_coordinates = []
    y_coordinates = []

    for i in range(cnvs.nol):
        coordinates = C.coords(cnvs.canvas_id[i])
        x_coordinates.append(coordinates[0])
        y_coordinates.append(coordinates[1])
        x_coordinates.append(coordinates[-2])
        y_coordinates.append(coordinates[-1])

    return x_coordinates, y_coordinates

def start_simulation():
    global component_stack
    s = steady_state_analysis.ssa(component_stack)

root = Tk()
C = Canvas(root, bg="white", height = 600, width =1200)
#C = Canvas(root, bg="white", height = 400, width =400)
C.grid(column=1, row=0, rowspan=10)
button_red = ttk.Button(root, text="Resistor", command=enable_red)
button_red.grid(column=0, row=1)
button_red = ttk.Button(root, text="Capacitor", command=enable_cap)
button_red.grid(column=0, row=2)
button_red = ttk.Button(root, text="Inductor", command=enable_ind)
button_red.grid(column=0, row=3)
button_wir = ttk.Button(root, text="Wire", command=add_wir)
button_wir.grid(column=0, row=4)
button_none = ttk.Button(root, text="Source", command=enable_src)
button_none.grid(column=0, row=5)
button_none = ttk.Button(root, text="Gnd", command=enable_gnd)
button_none.grid(column=0, row=6)
button_none = ttk.Button(root, text="Set", command=enable_set)
button_none.grid(column=0, row=7)
button_none = ttk.Button(root, text="Clear", command=clear_everything)
button_none.grid(column=0, row=8)
button_none = ttk.Button(root, text="Simulate", command=start_simulation)
button_none.grid(column=0, row=9)
top_label = ttk.Label(root, text="Clear")
top_label.grid(column=0, row =0)

root.bind_all("<Control-z>", undo)

root.mainloop()