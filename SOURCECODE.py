import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.integrate
from scipy.integrate import quad
from datetime import datetime
from tkinter import *
import tkinter as tk
from colorama import Fore,Back,Style

# Intro
root = tk.Tk()
root.title("Python End Sem Project")
root.geometry("1366x500")
ascii_art ='''//
//  d888888P dP                                                            d888888P dP                                    dP   
//     88    88                                                               88    88                                    88   
//     88    88d888b. .d8888b. 88d888b. 88d8b.d8b. .d8888b.                   88    88d888b. 88d888b. dP    dP .d8888b. d8888P 
//     88    88'  `88 88ooood8 88'  `88 88'`88'`88 88'  `88    88888888       88    88'  `88 88'  `88 88    88 Y8ooooo.   88   
//     88    88    88 88.  ... 88       88  88  88 88.  .88                   88    88    88 88       88.  .88       88   88   
//     dP    dP    dP `88888P' dP       dP  dP  dP `88888P'                   dP    dP    dP dP       `88888P' `88888P'   dP   
//                                                                                                                             
//                                                                                                                             
//                                                  dP                   888888ba  dP     dP 8888ba.88ba   888888ba            
//                                                  88                   88    `8b 88   .d8' 88  `8b  `8b  88    `8b           
//                                                  88d888b. dP    dP    88     88 88aaa8P'  88   88   88 a88aaaa8P'           
//                                                  88'  `88 88    88    88     88 88   `8b. 88   88   88  88   `8b.           
//                                                  88.  .88 88.  .88    88     88 88     88 88   88   88  88     88           
//                                                  88Y8888' `8888P88    dP     dP dP     dP dP   dP   dP  dP     dP           
//                                                                .88                                                          
//                                                            d8888P                                                           '''

label = Label(root, text=ascii_art, font=("Courier", 11), fg="orange", bg="black", justify='left', anchor='nw')
label.pack(fill='both', expand=True)
root.mainloop()

# Otto cycle graphing function
def graph_otto_cycle(p_min, v_max, r, gma, T3, T2):
    
    # Process 1-2
    p1 = p_min
    v1 = v_max
    v2 = v1 / r
    c1 = p1 * np.power(v1,gma)
    v = np.linspace(v1, v2, 100)
    p = c1 / np.power(v,gma)
    plt.plot(v, p/1000, 'b', linewidth=3)

    # Process 2-3
    v3 = v2
    p2 = c1 / np.power(v2,gma)
    p3 = p2 * (T3 / T2)
    p = np.linspace(p2, p3, 100)
    v = 100 * [v3]
    plt.plot(v, p/1000, 'r', linewidth=3)

    # Process 3-4
    c2 = p3 * np.power(v3,gma)
    v4 = v1
    v = np.linspace(v3, v4, 100)
    p = c2 / np.power(v,gma)
    plt.plot(v, p/1000, 'g', linewidth=3)

    # Process 4-1
    v = 100 * [v4]
    p4 = c2 / np.power(v4,gma)
    p = np.linspace(p1, p4, 100)
    plt.plot(v, p/1000, 'orange', linewidth=3)
    
    # Plot
    plt.title('Otto Cycle')
    plt.xlabel('Volume ($m^3$)')
    plt.ylabel('Pressure (kPa)')
    plt.text(v1, p1 / 1000, '1')
    plt.text(v2, p2 / 1000, '2')
    plt.text(v3, p3 / 1000, '3')
    plt.text(v4, p4 / 1000, '4')
    plt.show()
    
    # Calculating area enclosed by P-V graph
    f1 = lambda v : c2 / np.power(v,gma)
    I1 , err1 = quad(f1 , v2 , v1)
    f2 = lambda v : c1 / np.power(v,gma)
    I2 , err2 = quad(f2 , v2, v1)
    W = I1 - I2
    
    # Data dictionary
    data = {'p': [p1, p2, p3, p4], 'v': [v1, v2, v3, v4]}
    
    return [W, data]

# Otto cycle value deducer
def thermal_otto(p_min, v_max, r, gma):
    
    # Initial temperature input
    temp = input(Fore.YELLOW+Back.BLACK+"\nEnter the temp unit to be input as k for kelvin,c for celsius or f for fahrenheit : ")
    T1 = float(input(Fore.YELLOW+Back.BLACK+"\nEnter temperature corresponding to initial phase of cycle : "))
    
    # Unit converter
    if temp == "c" or temp == "C":
        T1 = 273.15 + T1
    elif temp == "f" or temp == "F":
        T1 = (T1 - 32) * (5 / 9) + 273.15
    else:
        T1 = T1
    
    # Input parameters
    Cv = float(input(Fore.YELLOW+Back.BLACK+'\nEnter specific heat capacity of the mixture at constant volume : '))
    f = float(input(Fore.YELLOW+Back.BLACK+'\nEnter fuel/air ratio : '))
    q = float(input(Fore.YELLOW+Back.BLACK+'\nEnter heat released per kg of fuel : '))
    den = float(input(Fore.YELLOW+Back.BLACK+'\nEnter the density of air : '))
    
    # Temperature deductions
    T2 = T1 * np.power(r, gma - 1)
    T3 = T2 + f * q / Cv
    T4 = T3 * np.power(r, (1 - gma))
    
    [W, data] = graph_otto_cycle(p_min, v_max, r, gma, T3, T2)
    
    # Power and efficiency calculation
    cps = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the number of engine cycles run per second : "))
    mass = den * v_max
    pl = (mass * Cv * (T4 - T1)) * cps
    n = 1 - ((T4 - T1) / (T3 - T2))
    power = cps * W
    
    # Display
    print(Fore.BLACK+Back.YELLOW+f'\n\nThe temperatures are as follows :\n\n T1={round(T1,2)}K\n\n T2={round(T2,2)}K\n\n T3={round(T3,2)}K\n\n T4={round(T4,2)}K\n')
    print(Fore.BLACK+Back.YELLOW+f'\nThe power produced by this cycle : {round(power,2)} W')
    print(Fore.BLACK+Back.YELLOW+f'\nThe power lost during isochoric heat rejection : {round(pl,2)} W')
    print(Fore.BLACK+Back.YELLOW+'\nThe change in internal energy per cycle : 0')
    print(Fore.BLACK+Back.YELLOW+'\nThe change in enthalpy per cycle : 0')
    print(Fore.BLACK+Back.YELLOW+'\nThe change in entropy per cycle : 0')
    print(Fore.BLACK+Back.YELLOW+f'\nThe efficiency of this cycle : {round(n,4)}\n\n')
    
    # Otto cycle cooling coefficient function
    def cooling_coefficient(T4, T1, Tc, cps):
        c = T4 - Tc
        K = (- np.log((T1 - Tc + 0.01) / c)) / (1 / (cps * 4))
        return K
    
    # Input cooling parameters
    temp = input(Fore.YELLOW+Back.BLACK+"Enter the temp unit to be input as k for kelvin,c for celsius or f for fahrenheit : ")
    Tc = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the working temperature of coolant : "))
    
    # Unit conversion
    if temp == "c" or temp == "C":
        Tc = 273.15 + Tc
    elif temp == "f" or temp == "F":
        Tc = (Tc - 32) * (5 / 9) + 273.15
    else:
        Tc = Tc
        
    K = cooling_coefficient(T4, T1, Tc, cps)
    print(Fore.BLACK+Back.YELLOW+f'\nThe cooling coefficient : {round(K,4)} per second')
    
    # Cooling estimation
    c = T4 - Tc
    time_range = np.linspace(0, (1 / (cps * 4)), 1000)
    temp = (Tc + c * np.exp(-K * time_range))
    
    # Plot
    plt.plot(time_range, temp)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (kelvin)')
    plt.title('Temperature vs Time')
    plt.grid(True)
    plt.show()
    
    # Data capturing
    fh = open('otto.csv','a',newline = "") 
    wob = csv.writer(fh)
    now = datetime.now()
    dt = now.strftime('%B %d, %Y')
    ti = now.strftime('%H:%M:%S')
    wob.writerow([dt,ti])
    wob.writerow(['P1 (kPa)','P2 (kPa)','P3 (kPa)','P4 (kPa)','V1 (m^3)','V2 (m^3)','V3 (m^3)','V4 (m^3)','T1 (K)','T2 (K)','T3 (K)','T4 (K)','Cooling coefficient (per sec.)','Power (W)','Power loss (W)','Del internal energy (J)','Del enthalpy (J)','Del entropy (J/K)','Efficiency'])
    cal = [round((data['p'][0])/1000,2),round((data['p'][1])/1000,2),round((data['p'][2])/1000,2),round((data['p'][3])/1000,2),round(data['v'][0],6),round(data['v'][1],6),round(data['v'][2],6),round(data['v'][3],6),round(T1,2),round(T2,2),round(T3,2),round(T4,2),round(K,4),round(power,2),round(pl,2),0,0,0,round(n,4)]
    wob.writerow(cal)
    print(Fore.BLACK+Back.YELLOW+"\ndata captured successfully\n")
    fh.close()

# Diesel cycle graphing function
def graph_diesel_cycle(p_min, v_max, gma, rv, T2, T3):
    
    # Process 1-2
    p1 = p_min
    v1 = v_max
    c1 = p1 * np.power(v1, gma)
    v2 = v1 / rv
    p2 = c1 / np.power(v2, gma)
    v = np.linspace(v1, v2, 100)
    p = c1 / np.power(v, gma)
    plt.plot(v, p / 1000, 'b', linewidth = 3)
    
    # Process 2-3
    p3 = p2
    v3 = v2 / T2 * T3
    v = np.linspace(v2, v3, 100)
    p = 100 * [p3 / 1000]
    plt.plot(v, p, 'r', linewidth = 3)

    # Process 3-4
    c2 = p3 * np.power(v3, gma)
    v4 = v1
    p4 = c2 / np.power(v4, gma)
    v = np.linspace(v4, v3, 100)
    p = c2 / np.power(v, gma)
    plt.plot(v, p / 1000, 'g', linewidth = 3)

    # Process 4-1
    p = np.linspace(p1, p4, 100)
    v = 100 * [v1]
    plt.plot(v, p / 1000, 'orange', linewidth = 3)
    
    # Plot
    plt.title('Diesel cycle')
    plt.xlabel('Volume ($m^3$)')
    plt.ylabel('Pressure (kpa)')
    plt.text(v1, p1 / 1000, '1')
    plt.text(v2, p2 / 1000, '2')
    plt.text(v3, p3 / 1000, '3')
    plt.text(v4, p4 / 1000, '4')
    plt.show()
    
    # Calculating area enclosed by P-V graph
    f1 = lambda v : c2 / np.power(v, gma)
    I1 , err1 = quad(f1, v3, v1)
    f2 = lambda v : c1 / np.power(v, gma)
    I2 , err2 = quad(f2, v2, v1)
    W = I1 + (p3 * (v3 - v2)) - I2
    
    # rc calculation
    rc = v3 / v2
    
    # Enthalpy
    en = p2 * (v3 - v2)
    
    # Data dictionary
    data = {'p': [p1, p2, p3, p4], 'v': [v1, v2, v3, v4]}
    
    return [W, rc, en, data]
 
# Diesel cycle values deducer
def thermal_diesel(p_min, v_max, gma, rv):
    
    # Initial temperature input
    temp = input(Fore.YELLOW+Back.BLACK+"\nEnter the temp unit to be input as k for kelvin,c for celsius or f for fahrenheit : ")
    T1 = float(input(Fore.YELLOW+Back.BLACK+"\nEnter temperature corresponding to initial phase of cycle : "))
    
    # Unit converter
    if temp == "c" or temp == "C":
        T1 = 273.15 + T1
    elif temp == "f" or temp == "F":
        T1 = (T1 - 32) * (5 / 9) + 273.15
    else:
        T1 = T1
    
    # Input parameters
    Cv = float(input(Fore.YELLOW+Back.BLACK+'\nEnter specific heat capacity of the mixture at constant volume : '))
    Cp = float(input(Fore.YELLOW+Back.BLACK+'\nEnter specific heat capacity of the mixture at constant pressure : '))
    f = float(input(Fore.YELLOW+Back.BLACK+'\nEnter fuel/air ratio : '))
    q = float(input(Fore.YELLOW+Back.BLACK+'\nEnter heat released per kg of fuel : '))
    den = float(input(Fore.YELLOW+Back.BLACK+'\nEnter the density of air : '))
     
    # Temperature deductions
    T2 = T1 * np.power(rv,gma - 1)
    T3 = T2 + f * q / Cp
    
    [W, rc, en, data] = graph_diesel_cycle(p_min, v_max, gma, rv, T2, T3)
    
    T4 = T3 * np.power((rc / rv),(gma - 1))
    
    # Power and efficiency calculation
    cps = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the number of engine cycles run per second : "))
    mass = den * v_max
    pl = (mass * Cv * (T4 - T1)) * cps
    p = W * cps
    n = 1 - ((Cv * (T4 - T1)) / (Cp * (T3 - T2)))
    
    # Display
    print(Fore.BLACK+Back.YELLOW+f'\nThe temperatures are as follows:\n\n T1={round(T1,2)}K\n\n T2={round(T2,2)}K\n\n T3={round(T3,2)}K\n\n T4={round(T4,2)}K\n')
    print(Fore.BLACK+Back.YELLOW+f'\nThe power produced by this cycle : {round(p,2)} W')
    print(Fore.BLACK+Back.YELLOW+f'\nThe power lost during isochoric heat rejection : {round(pl,2)} W')
    print(Fore.BLACK+Back.YELLOW+'\nThe change in internal energy per cycle : 0')
    print(Fore.BLACK+Back.YELLOW+f'\nThe change in enthalpy per cycle : {round(en,2)} J')
    print(Fore.BLACK+Back.YELLOW+'\nThe change in entropy per cycle : 0')
    print(Fore.BLACK+Back.YELLOW+f'\nThe efficiency of this cycle : {round(n,4)}\n\n')
    
    # Diesel cycle cooling coefficient function
    def cooling_coefficient(T4, T1, Tc, cps):
        c = T4 - Tc
        K = (- np.log((T1 - Tc + 0.01) / c)) / (1 / (cps * 4))
        return K
    
    # Input cooling parameters
    temp = input(Fore.YELLOW+Back.BLACK+"Enter the temp unit to be input as k for kelvin,c for celsius or f for fahrenheit : ")
    Tc = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the working temperature of coolant : "))

    # Unit converter
    if temp == "c" or temp == "C":
        Tc = 273.15 + Tc
    elif temp == "f" or temp == "F":
        Tc = (Tc - 32) * (5 / 9) + 273.15
    else:
        Tc = Tc

    K = cooling_coefficient(T4, T1, Tc, cps)
    print(Fore.BLACK+Back.YELLOW+f'\nThe cooling coefficient : {round(K,4)} per second')
    
    # Cooling estimation
    c = T4 - Tc
    time_range = np.linspace(0, (1 / (cps * 4)), 1000)
    temp = (Tc + c * np.exp(-K * time_range))

    # Plot
    plt.plot(time_range, temp)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (kelvin)')
    plt.title('Temperature vs Time')
    plt.grid(True)
    plt.show()
    
    # Data capturing
    fh=open('diesel.csv','a',newline = "")
    wob=csv.writer(fh)
    now = datetime.now()
    dt = now.strftime('%B %d, %Y')
    ti = now.strftime('%H:%M:%S')
    wob.writerow([dt,ti])
    wob.writerow(['P1 (kPa)','P2 (kPa)','P3 (kPa)','P4 (kPa)','V1 (m^3)','V2 (m^3)','V3 (m^3)','V4 (m^3)','T1 (K)','T2 (K)','T3 (K)','T4 (K)','Cooling Coefficient (per sec.)','Power (W)','Power loss (W)','Del Internal Energy (J)','Del Enthalpy (J)','Del Entropy (J/K)','Efficiency'])
    cal=[round((data['p'][0])/1000,2),round((data['p'][1])/1000,2),round((data['p'][2])/1000,2),round((data['p'][3])/1000,2),round(data['v'][0],6),round(data['v'][1],6),round(data['v'][2],6),round(data['v'][3],6),round(T1,2),round(T2,2),round(T3,2),round(T4,2),round(K,4),round(p,2),round(pl,2),0,round(en,2),0,round(n,4)]
    wob.writerow(cal)
    print(Fore.BLACK+Back.YELLOW+"\ndata captured successfully\n")
    fh.close()
 
 # Initiator
choice = int(input(Fore.CYAN+Back.BLACK+"\nEnter 1 for otto cycle or 2 for diesel cycle : "))
contin = input(Fore.CYAN+Back.BLACK+'\nEnter y to start the process or else type n to not execute it : ')
while contin == 'y' or contin == 'Y':
     
    if choice == 1:
        p_min = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the initial pressure developed in the cycle in Pa : "))
        v_max = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the max volume of the engine cylinder in metre cube : "))
        r = float(input(Fore.YELLOW+Back.BLACK+'\nEnter compression ratio : '))
        gma = float(input(Fore.YELLOW+Back.BLACK+'\nEnter gamma value : '))
    
        thermal_otto(p_min, v_max, r, gma)
        
    elif choice == 2:
        p_min = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the initial pressure developed in the cycle in Pa : "))
        v_max = float(input(Fore.YELLOW+Back.BLACK+"\nEnter the max volume of the engine cylinder in metre cube : "))
        rv = float(input(Fore.YELLOW+Back.BLACK+'\nEnter compression ratio : '))
        gma = float(input(Fore.YELLOW+Back.BLACK+'\nEnter gamma value : '))
        
        thermal_diesel(p_min, v_max, gma, rv)
        
    else:
        print(Fore.BLACK+Back.YELLOW+'\nPlease retry using the specifications mentioned\nTry to re-run the code\n')
    
    contin = input(Fore.CYAN+Back.BLACK+'\nEnter y to continue the process or else type n to stop it : ')
    if contin == 'N' or contin == 'n':
        break
    choice = int(input(Fore.CYAN+Back.BLACK+"\nEnter 1 for otto cycle or 2 for diesel cycle : "))