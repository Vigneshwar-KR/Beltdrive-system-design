from tkinter import *
from typing import Dict
from datetime import datetime
from reportlab.pdfgen import canvas

root = Tk()

# Constants Declaration
pi = 3.14

# Reference Data from Design  Data Book
arc_of_contact = [90, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
correction_factor = [1.68, 1.33, 1.26, 1.19, 1.13, 1.08, 1.04, 1.00, 0.97, 0.94, 0.91, 0.88, 0.86, 0.84, 0.82]
number_of_plies = [3, 4, 5, 6, 8]
belt_speeds = [10.0, 15.0, 20.0, 25.0, 30.0]
pulley_diameter_speed_10 = [90, 140, 200, 250, 450]
pulley_diameter_speed_15 = [100, 160, 224, 315, 500]
pulley_diameter_speed_20 = [112, 180, 250, 355, 560]
pulley_diameter_speed_25 = [140, 200, 315, 400, 630]
pulley_diameter_speed_30 = [180, 250, 355, 450, 710]
pulley_diameters = [pulley_diameter_speed_10, pulley_diameter_speed_15, pulley_diameter_speed_20, pulley_diameter_speed_25, pulley_diameter_speed_30]
std_belt_width_3_ply = [25, 40, 50, 63, 76]
std_belt_width_4_ply = [40, 44, 50, 63, 76, 90, 100, 112, 125, 152]
std_belt_width_5_ply = [76, 100, 112, 125, 152, 180, 250]
std_belt_width_6_ply = [112, 125, 152, 180, 200, 250]
std_belt_width_8_ply = [200, 250, 305, 355, 400]
std_belt_widths = [std_belt_width_3_ply, std_belt_width_4_ply, std_belt_width_5_ply, std_belt_width_6_ply, std_belt_width_8_ply]
load_correction_factors: Dict[str, float] = {
    "Normal": 1.0,
    "Steady": 1.2,
    "Intermittent": 1.3,
    "Shock": 1.5
}

# Global Variable Declarations
global_ka = IntVar()
global_ks = IntVar()
global_design_power = IntVar()
global_velocity = IntVar()
global_pinion_pulley_speed = IntVar()
global_belt_rating = IntVar()
global_length = IntVar()
global_center_distance = IntVar()
global_pinion_pulley_diameter = IntVar()
global_output_pulley_diameter = IntVar()
global_number_of_plies = IntVar()
global_speed_ratio = IntVar()
global_contact_angle = IntVar()
global_belt_width = IntVar()
global_std_belt_width = IntVar()
global_reduced_belt_length = IntVar()
global_pulley_width = IntVar()
local_contact_angle = IntVar()
local_velocity = IntVar()
driveTypeId = IntVar()
hpId = IntVar()

# --------------- Calculation Functions Declaration ---------------


def pulley_width_func():
    global global_std_belt_width
    global global_pulley_width
    # ----- Pulley Width Calculation -----
    if global_std_belt_width <= 125:
        global_pulley_width = global_std_belt_width + 13
    elif 125 < global_std_belt_width <= 250:
        global_pulley_width = global_std_belt_width + 25
    elif 250 < global_std_belt_width <= 375:
        global_pulley_width = global_std_belt_width + 38
    elif 375 < global_std_belt_width <= 500:
        global_pulley_width = global_std_belt_width + 50
    print("Pulley Width : ", global_pulley_width)
    #saveBtn.config(state=NORMAL)  
    result_screen()


def length_reduction_func():
    global global_number_of_plies
    global global_length
    global global_reduced_belt_length
    # ----- Reducing Belt Length for Tension -----
    if global_number_of_plies == 3:
        global_reduced_belt_length = global_length - (0.015 * global_length)
    elif global_number_of_plies == 4 or global_number_of_plies == 5 or global_number_of_plies == 6:
        global_reduced_belt_length = global_length - (0.01 * global_length)
    else:
        global_reduced_belt_length = global_length - (0.05 * global_length)
    global_reduced_belt_length = round(global_reduced_belt_length, 3)
    print("Reduced Belt Length : ", global_reduced_belt_length)
    pulley_width_func()


def belt_length_func():
    global global_length
    global global_center_distance
    global global_pinion_pulley_diameter
    global global_output_pulley_diameter
    # ----- Length of Belt -----
    if driveTypeVariable.get() == "Open":
        l1 = (2 * global_center_distance)
        l2 = ((pi / 2) * (global_output_pulley_diameter + global_pinion_pulley_diameter))
        l3 = (((global_output_pulley_diameter - global_pinion_pulley_diameter) ** 2) / (4 * global_center_distance))
        global_length = l1 + l2 + l3
    else:
        l1 = (2 * global_center_distance)
        l2 = ((pi / 2) * (global_output_pulley_diameter + global_pinion_pulley_diameter))
        l3 = (((global_output_pulley_diameter + global_pinion_pulley_diameter) ** 2) / (4 * global_center_distance))
        global_length = l1 + l2 + l3
    print("Length of Belt : ", global_length)
    length_reduction_func()


def belt_standardize_func():
    global global_number_of_plies
    global global_belt_width
    global global_std_belt_width
    limit = 0
    # ----- Belt Width Standardization -----
    for var in std_belt_widths[number_of_plies.index(global_number_of_plies)]:
        if var > global_belt_width:
            global_std_belt_width = var
            break
        limit = limit + 1
    if limit == len(std_belt_widths[number_of_plies.index(global_number_of_plies)]):
        temp_add = number_of_plies.index(global_number_of_plies)
        temp_add = temp_add + 1
        global_number_of_plies = number_of_plies[temp_add]
        belt_rating_func()
    else:
        print("Standard Belt Width : ", global_std_belt_width)
        belt_length_func()


def belt_width_func():
    global global_belt_width
    global global_design_power
    global global_belt_rating
    # ----- Belt Width -----
    global_belt_width = (global_design_power / global_belt_rating)
    print("Belt Width : ", global_belt_width)
    belt_standardize_func()


def belt_rating_func():
    global global_belt_rating
    global global_velocity
    global global_number_of_plies
    global global_contact_angle
    # ----- Belt Rating (kW/mm) -----
    global_belt_rating = (0.0289 * global_number_of_plies * (global_contact_angle / 180) * (global_velocity / 10))
    print("Belt Rating :  ", global_belt_rating, "kW/mm")
    belt_width_func()


def ply_selection_func():
    global global_number_of_plies
    global local_velocity
    global global_pinion_pulley_diameter
    # ----- Number of Ply Selection -----
    for y in belt_speeds:
        if local_velocity < y:
            local_velocity = belt_speeds.index(y)
            break
    for u in pulley_diameters[local_velocity]:
        if (global_pinion_pulley_diameter * 1000) < u:
            temp = pulley_diameters[local_velocity]
            print(temp)
            global_number_of_plies = temp.index(u)
            global_number_of_plies = number_of_plies[global_number_of_plies]
            break
    print("Number of Plies : ", global_number_of_plies)
    belt_rating_func()


def velocity_func():
    global global_pinion_pulley_speed
    global global_velocity
    global local_velocity
    global global_pinion_pulley_diameter
    # ----- Getting Input from Screen -----
    global_pinion_pulley_speed = float(Entry.get(speed))
    # ----- Velocity in m/s -----
    global_velocity = ((pi * global_pinion_pulley_diameter * global_pinion_pulley_speed) / 60)
    local_velocity = int(global_velocity)
    print("Pinion Velocity : ", global_velocity)
    ply_selection_func()


def design_power_func():
    global powerInput
    global global_design_power
    global global_ks
    global global_ka
    global powerOptionVariable
    global hpId
    # ----- Getting Input from Screen -----
    powerInput = float(Entry.get(power))
    if powerOptionVariable.get() == "hp":
        powerInput = (0.743 * powerInput)
        hpId = 1
    else:
        hpId = 0


    # ----- Design Power Calculation -----
    global_design_power = (powerInput * global_ka * global_ks)
    print("Design Power, Pd : ", global_design_power)
    print("hp Id : ", hpId)
    velocity_func()


def ks_func():
    global global_ks
    # ----- Ks -----
    global_ks = loadingConditionVariable.get()
    global_ks = load_correction_factors[global_ks]
    print("Load Correction Factor, Ks : ", global_ks)
    design_power_func()


def ka_func():
    global global_contact_angle
    global global_ka
    global global_pinion_pulley_diameter
    global global_output_pulley_diameter
    global global_center_distance
    global local_contact_angle
    global global_speed_ratio
    global driveTypeId
    # ----- Getting Inputs from Screen -----
    global_center_distance = float(Entry.get(centerDistance))
    global_speed_ratio = float(Entry.get(speedRatio))
    global_pinion_pulley_diameter = float(Entry.get(pinionPulleyDiameter))
    global_output_pulley_diameter = (global_pinion_pulley_diameter * global_speed_ratio)
    global_output_pulley_diameter = round(global_output_pulley_diameter, 2)
    # ----- Contact Angle and Ka -----
    if driveTypeVariable.get() == "Open":
        driveTypeId = 0
        a1 = ((global_output_pulley_diameter - global_pinion_pulley_diameter) / global_center_distance)
        global_contact_angle = (180 - (a1 * 60))
    else:
        driveTypeId = 1
        a1 = ((global_output_pulley_diameter + global_pinion_pulley_diameter) / global_center_distance)
        global_contact_angle = (180 + (a1 * 60))
    print("Contact Angle : ", global_contact_angle)
    local_contact_angle = global_contact_angle
    for x in arc_of_contact:
        if local_contact_angle < x:
            local_contact_angle = x
            local_contact_angle = ((arc_of_contact.index(x)) - 1)
            break
    global_ka = correction_factor[local_contact_angle]
    print("Contact Angle Correction Factor, Ka : ", global_ka)
    ks_func()


def calculate_function():
    ka_func()
    # ----- Function Order -----
    ks_func()
    design_power_func()
    velocity_func()
    ply_selection_func()
    belt_rating_func()
    belt_standardize_func()
    belt_width_func()
    belt_length_func()
    length_reduction_func()
    pulley_width_func()

# --------------- GUI Functions ---------------

def result_screen():
    global global_design_power
    global global_number_of_plies
    global global_belt_rating
    global global_std_belt_width
    global global_pulley_width
    global global_output_pulley_diameter
    global global_pinion_pulley_diameter
    result_frame = Toplevel()
    result_frame.title("Results")
    result_frame.iconbitmap("C:\\Vicky\\Projects\\dataLogger_UsbSerial_python\\beltDriveDesign_python\\images\\tsd_fb_icon.ico")
    result_frame.geometry("700x550")
    result_frame.resizable(width=False, height=False)
    result_frame.config(bg="#645d58")
    # ----- Output Label Declaration -----
    power_output_label = Label(result_frame, text="Design Power : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    pinion_pulley_diameter_label = Label(result_frame, text="Input Pulley Diameter : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    output_pulley_diameter_label = Label(result_frame, text="Output Pulley Diameter : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    belt_type_label = Label(result_frame, text="Belt Type : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    ply_output_label = Label(result_frame, text="Number of Plies : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    belt_rating_output_label = Label(result_frame, text="Belt Rating : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    belt_width_output_label = Label(result_frame, text="Std. Belt Width: ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    belt_length_output_label = Label(result_frame, text="Belt Length (Tension) : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    pulley_width_output_label = Label(result_frame, text="Pulley Width : ", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    # ----- Units Label Declaration -----
    power_unit = Label(result_frame, text="kW", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    pinion_pulley_diameter_unit = Label(result_frame, text="m", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    output_pulley_diameter_unit = Label(result_frame, text="m", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    belt_rating_unit = Label(result_frame, text="kW/mm", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    belt_width_unit = Label(result_frame, text="mm", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    belt_length_unit = Label(result_frame, text="m", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    pulley_width_unit = Label(result_frame, text="mm", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=FLAT)
    # ----- Output Result Variable Declaration -----
    t1 = StringVar()
    power_output = Label(result_frame, textvariable=t1, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t1.set(round(global_design_power, 2))
    t2 = StringVar()
    ply_output = Label(result_frame, textvariable=t2, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t2.set(round(global_number_of_plies, 2))
    t3 = StringVar()
    belt_rating_output = Label(result_frame, textvariable=t3, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t3.set(round(global_belt_rating, 2))
    t4 = StringVar()
    belt_width_output = Label(result_frame, textvariable=t4, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t4.set(global_std_belt_width)
    t5 = StringVar()
    belt_length_output = Label(result_frame, textvariable=t5, font="Verdana 10", bg="#645d58", fg="#ffeb00", relief=RIDGE, bd=2)
    t5.set(global_reduced_belt_length)
    t6 = StringVar()
    pulley_width_output = Label(result_frame, textvariable=t6, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t6.set(round(global_pulley_width, 2))
    t7 = StringVar()
    pinion_pulley_diameter_output = Label(result_frame, textvariable=t7, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t7.set(global_pinion_pulley_diameter)
    t8 = StringVar()
    output_pulley_diameter_output = Label(result_frame, textvariable=t8, font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    t8.set(global_output_pulley_diameter)
    belt_type_output = Label(result_frame, text="Dunlop FORT 949 g Fabric Belting", font="Verdana 10", fg="#ffeb00", bg="#645d58", relief=RIDGE, bd=2)
    # ----- Packing Elements -----
    # - Labels -
    power_output_label.grid(row=1, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    ply_output_label.grid(row=2, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    belt_rating_output_label.grid(row=3, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    belt_width_output_label.grid(row=4, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    belt_length_output_label.grid(row=5, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    pulley_width_output_label.grid(row=6, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    pinion_pulley_diameter_label.grid(row=7, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    output_pulley_diameter_label.grid(row=8, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    belt_type_label.grid(row=9, column=1, padx=50, pady=10, ipadx=7, ipady=7)
    # -- Values --
    # - Output Values and Corresponding Units -
    power_output.grid(row=1, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    power_unit.grid(row=1, column=2, padx=80, pady=10, ipadx=7, ipady=7)
    ply_output.grid(row=2, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    belt_rating_output.grid(row=3, column=2, padx=80, pady=20, ipadx=7, ipady=7, sticky=W)
    belt_rating_unit.grid(row=3, column=2, padx=10, pady=10, ipadx=7, ipady=7)
    belt_width_output.grid(row=4, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    belt_width_unit.grid(row=4, column=2, padx=40, pady=10, ipadx=7, ipady=7)
    belt_length_output.grid(row=5, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    belt_length_unit.grid(row=5, column=2, padx=40, pady=10, ipadx=7, ipady=7)
    pulley_width_output.grid(row=6, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    pulley_width_unit.grid(row=6, column=2, padx=40, pady=10, ipadx=7, ipady=7)
    pinion_pulley_diameter_output.grid(row=7, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    pinion_pulley_diameter_unit.grid(row=7, column=2, padx=80, pady=10, ipadx=7, ipady=7)
    output_pulley_diameter_output.grid(row=8, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)
    output_pulley_diameter_unit.grid(row=8, column=2, padx=80, pady=10, ipadx=7, ipady=7)
    belt_type_output.grid(row=9, column=2, padx=80, pady=10, ipadx=7, ipady=7, sticky=W)


def tsd_fb_quit():
    root.quit()


# Screen Size Declaration
root.resizable(width=FALSE, height=FALSE)
root.geometry("1100x700")
root.title("TSD-FB")
root.iconbitmap("C:\\Vicky\\Projects\\dataLogger_UsbSerial_python\\beltDriveDesign_python\\images\\tsd_fb_icon.ico")
home_screen_bg_image = PhotoImage("C:\Vicky\Projects\dataLogger_UsbSerial_python\beltDriveDesign_python\images\home_screen_bg.png")

bg_image = Label(root, image=home_screen_bg_image)
bg_image.place(x=0, y=0, relwidth=1, relheight=1)

# Menu Bar Declaration
menuBar = Menu(root)
root.config(menu=menuBar)
file_menu = Menu(menuBar)
""" help_menu = Menu(menuBar)
source_menu = Menu(menuBar)
"""
menuBar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=tsd_fb_quit)


# Declaring Home Screen Elements
# -----------  1. Label Declaration  -----------
powerInputLabel = Label(root, text="Power : ", font="Verdana 10", bg="#a7a7a7", relief=RIDGE, bd=2)
speedInputLabel = Label(root, text="Speed : ", font="Verdana 10", bg="#b5b5b5", relief=RIDGE, bd=2)
rpmLabel = Label(root, text="RPM", font="Verdana 10", bg="#b5b5b5", relief=FLAT, bd=2)
speedRatioInputLabel = Label(root, text="Speed ratio : ", font="Verdana 10", bg="#aeaeae", relief=RIDGE, bd=2)
centerDistanceInputLabel = Label(root, text="Center Distance : ", font="Verdana 10", bg="#a7a7a7", relief=RIDGE, bd=2)
pinionPulleyDiameterInputLabel = Label(root, text="Diameter : ", font="Verdana 10", bg="#bbbbbb", relief=RIDGE, bd=2)
loadingConditionInputLabel = Label(root, text="Loading Condition : ", font="Verdana 10", bg="#b5b5b5", relief=RIDGE, bd=2)
beltTypeInputLabel = Label(root, text="Belt Type : ", font="Verdana 10", bg="#a7a7a7", relief=RIDGE, bd=2)
driveTypeInputLabel = Label(root, text="Drive Type : ", font="Verdana 10", bg="#a7a7a7", relief=RIDGE, bd=2)
# Optional Title
# flatBeltTitle = Label(root, text="Flat Belt Design", anchor=CENTER, font="Arial 20 bold", bg="#a7a7a7", relief=RAISED)

# -----------  2. Entry Box Declaration -----------
# Motor Pulley Diameter = pinionPulleyDiameter
# Speed Ratio = i
# Center Distance = c
# Rotations per minute of motor pulley = n
# Power = P
initialSampleText = ["P", "Pinion", "i", "C in meters", "Pinion in m"]
powerInput = StringVar()
powerInput.set(initialSampleText[0])
power = Entry(root, justify=CENTER, bg="#aeaeae", textvariable=powerInput)
speedInput = StringVar()
speedInput.set(initialSampleText[1])
speed = Entry(root, justify=CENTER, bg="#b5b5b5", textvariable=speedInput)
speedRatioInput = StringVar()
speedRatioInput.set(initialSampleText[2])
speedRatio = Entry(root, justify=CENTER, bg="#a7a7a7", textvariable=speedRatioInput)
centerDistanceInput = StringVar()
centerDistanceInput.set(initialSampleText[3])
centerDistance = Entry(root, justify=CENTER, bg="#b5b5b5", textvariable=centerDistanceInput)
pinionPulleyDiameterInput = StringVar()
pinionPulleyDiameterInput.set(initialSampleText[4])
pinionPulleyDiameter = Entry(root, justify=CENTER, bg="#bbbbbb", textvariable=pinionPulleyDiameterInput)
# -----------  3. Comment Box Declaration -----------


# -----------  4. Buttons Declaration -----------
calculateBtn = Button(root, text="CALCULATE", font="system 15", bg="#a7a7a7", relief=RAISED, bd=2, state=NORMAL, command=calculate_function)

# -----------  5. Drop Down Menu Declaration -----------
# -> Power Input Type Menu Declaration
powerOptions = ["kW", "hp"]
powerOptionVariable = StringVar()
powerOptionVariable.set(powerOptions[0])
powerOptionMenu = OptionMenu(root, powerOptionVariable, *powerOptions)
powerOptionMenu.config(font="Verdana 10", bg="#a7a7a7", relief=RIDGE, bd=2)
# -> Loading Condition Menu Declaration
loadingConditions = ["Normal", "Steady", "Intermittent", "Shock"]
loadingConditionVariable = StringVar()
loadingConditionVariable.set(loadingConditions[0])
loadingConditionMenu = OptionMenu(root, loadingConditionVariable, *loadingConditions)
loadingConditionMenu.config(font="Verdana 10", bg="#a7a7a7", relief=RIDGE, bd=1)
# -> Drive Type Menu Declaration
driveTypes = ["Open", "Cross"]
driveTypeVariable = StringVar()
driveTypeVariable.set(driveTypes[0])
driveTypeMenu = OptionMenu(root, driveTypeVariable, *driveTypes)
driveTypeMenu.config(font="Verdana 10", bg="#bbbbbb", relief=RIDGE, bd=1)

# >>>>>>>  Binding elements to the home screen  <<<<<<<
powerInputLabel.grid(row=1, column=1, padx=20, pady=30, ipadx=7, ipady=7, sticky=W)
powerOptionMenu.grid(row=1, column=1, padx=20, pady=30, ipadx=5, ipady=5, sticky=E)
power.grid(row=1, column=2, ipadx=7, ipady=7)
speedInputLabel.grid(row=1, column=3, padx=50, pady=30, ipadx=7, ipady=7)
speed.grid(row=1, column=4, ipadx=7, ipady=7)
rpmLabel.grid(row=1, column=5, padx=5, pady=10, ipadx=7, ipady=7)
speedRatioInputLabel.grid(row=1, column=6, padx=20, pady=30, ipadx=7, ipady=7)
speedRatio.grid(row=1, column=7, ipadx=7, ipady=7, sticky=W)
centerDistanceInputLabel.grid(row=2, column=1, padx=20, pady=30, ipadx=7, ipady=7)
centerDistance.grid(row=2, column=2, ipadx=7, ipady=7)
pinionPulleyDiameterInputLabel.grid(row=2, column=3, padx=20, pady=30, ipadx=7, ipady=7)
pinionPulleyDiameter.grid(row=2, column=4, ipadx=7, ipady=7)
loadingConditionInputLabel.grid(row=2, column=6, padx=30, pady=30, ipadx=7, ipady=7)
loadingConditionMenu.grid(row=2, column=7, padx=30, pady=30, ipadx=5, ipady=5, sticky=W)
driveTypeInputLabel.grid(row=3, column=1, padx=30, pady=30, ipadx=5, ipady=5)
driveTypeMenu.grid(row=3, column=2, padx=30, pady=30, ipadx=5, ipady=5)
root.grid_rowconfigure(4, minsize=250)
calculateBtn.grid(row=5, column=1, padx=30, pady=30, ipadx=5, ipady=5)

root.mainloop()
