# Version to be excecuted in the console 
from tqdm import tqdm
import time
import os
import json
from win11toast import toast
from PyQt5.QtWidgets import *
os.system("cls")
# File Version details
version = "v1.0"
modules = ["os","time","json"]
default_settings = {
            "Session": 25,
            "Short Break": 5,
            "Long Break": 15,
            "Sessions to Long Break": 4
        }


def bootup():
    print("="*40)
    print("POMODOO TIMER MODULE")
    print("="*40)
    print(f"Version: {version}")
    for module in tqdm(modules,desc="Loading Dependencies"):
        exec(f"import {module}")
        time.sleep(0.1)
    print("\nModules Installed!\n")
    time.sleep(3)

def print_slow(text):
    for char in text:
        print(char,sep='',end='',flush=True)
        time.sleep(0.01)

def loadTimerData(filename):
    try:
        with open(filename,"r") as file:
            timer_options = json.load(file)
        file.close()
        return timer_options
    except:
        with open(filename,"w") as file:
            json.dump(default_settings, file)
        file.close()
        print_slow(f"\nCould not find custom settings! Reverting to default. See {filename} in the directory")
        return default_settings
    
def dumpData(filename,data):
    with open(filename,"w") as file:
        json.dump(data,file)
    file.close()
    print_slow("Data Saved!\n")

def setTimerConsole(settings=default_settings):
    print("-"*40)
    print_slow("Enter how many sessions you'd like to complete!\n")
    sessions = int(input("Number of Sessions: "))
    long_break_counter = settings["Sessions to Long Break"]
    print("-"*40)
    print_slow(f"Timer Set!\n")
    restart = True
    start = 0
    while restart:
        for session in range(1,sessions+1):
            try:
                # print(f"SESSION {session}")
                restart = False
                print("-"*40)
                for i in tqdm(range(start,60*settings["Session"]),desc=f"Session {session}"):
                    time.sleep(1)
                if long_break_counter == 0:
                    print("-"*40)
                    print("Please take a LONG BREAK!")
                    try: 
                        toast("LONG BREAK","Congradulations you've earned a long break!\nStep away from the screen and have a walk or do something you enjoy")
                    except:
                        pass
                    for i in tqdm(range(60*settings["Long Break"]),desc=f"Long Break"):
                        time.sleep(1)
                else:
                    print("-"*40)
                    print("Please take a SHORRT BREAK!")
                    toast("SHORT BREAK","Congradulations you've earned a short break!\nHave a quick reset to prepare yourself for the next session")
                    for i in tqdm(range(60*settings["Short Break"]),desc=f"Short Break"):
                        time.sleep(1)
                long_break_counter = long_break_counter - 1 
            except KeyboardInterrupt:
                print_slow("Timer Paused!\n")
                cont = input("Enter (e) to exit or any key to continue: ").lower()
                if cont == "e":
                    return 
                else: 
                    restart = True
                    start = i
    toast("Pomodoro Timer Finished!","Your study timer has expired! Enjoy your day!")

def adjustOptions(options):
    print_slow("Select the option you'd like to edit and enter the value youd like to change\n")
    option_list = []
    for option in options:
        option_list.append(option)
    valid_options = []
    for i in range(1,len(option_list)+1):
        valid_options.append(i)
        print_slow(f"-> {i}. {option_list[i-1]}\n")
    valid_options.append(len(option_list)+2)
    while True:
        try:
            selection = int(input("What would you like to alter?: "))
            print_slow(f"You have selected -> {option_list[selection-1]}\n")
            new_option = int(input("Enter new value: "))
            options[option_list[selection-1]] = new_option
            dumpData("settings.json",options)
            break
        except ValueError:
            print_slow("Please enter a valid option\n")
        except IndexError:
            print("Exiting Settings...")
            break
    
def menuOptionsConsole():
    # To be replaced using GUI
    options = loadTimerData("settings.json")
    possible_choices = [1,2,3]
    while True:
        try:
            print("-"*40)
            print_slow("Welcome to the Pomodoro Timer!\nReview and adjust session times before choosing your study session length!\n")
            print("-"*40)
            print_slow("Timer Component lengths (mins): \n")
            for option in options:
                print_slow(f"-> {option}: {options[option]}\n")
            print("-"*40)
            print_slow("Would you like to set a timer (1) adjust these settings (2) or Exit (3)?\n")
            choice = int(input("Option: "))
            if choice in possible_choices:
                if choice == 1:
                    setTimerConsole(options)
                elif choice == 2:
                    adjustOptions(options)
                elif choice == 3:
                    print_slow("Thank you for using this timer! Goodbye!")
                    break
                else:
                    print("Something went wrong! Please try again!")
            else:
                print("Please enter a valid option")
        except KeyboardInterrupt:
            print("Exiting Program...")
        except ValueError:
            print("Please enter a valid option")
    
if __name__ == "__main__":
    bootup()
    menuOptionsConsole()
