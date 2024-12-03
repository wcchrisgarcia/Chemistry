# https://introtopython.org/terminal_apps.html

import os
import pickle

from chempy import Substance
import quantities as q

import re
from sympy import Matrix, lcm

# Greeter is a terminal application that greets old friends warmly,
#   and remembers new friends.


### FUNCTIONS ###


def calculate_substance_properties(formula):
    """Calculates and prints properties of a chemical substance.

    Args:
      formula: The chemical formula of the substance (e.g., 'Fe(CN)6-3').

    Returns:
      None. substance's unicode name and molar mass in g/mol.
    """
    substance = Substance.from_formula(formula)
    mass_with_units = substance.mass * q.gram / q.mol  # Store mass with units
    print("mass with units: %s" % mass_with_units)
    return (substance.unicode_name, mass_with_units)


def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system("clear")

    print("\t**********************************************")
    print("\t************Chemistry Calculator***************")
    print("\t**********************************************")


def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Calculate Molar Mass.")
    print("[2] Balance Chemical Equation.")
    print("[3] Calculate Concentration of an Equilibrium Reaction.")
    print("[q] Quit.")

    return input("What would you like to do? ")


def show_names():
    # Shows the names of everyone who is already in the list.
    print("\nHere are the people I know.\n")
    for name in names:
        print(name.title())


def get_new_name():
    # Asks the user for a new name, and stores the name if we don't already
    #  know about this person.
    new_name = input("\nPlease tell me this person's name: ")
    if new_name in names:
        print("\n%s is an old friend! Thank you, though." % new_name.title())
    else:
        names.append(new_name)
        print("\nI'm so happy to know %s!\n" % new_name.title())


def load_names():
    # This function loads names from a file, and puts them in the list 'names'.
    #  If the file doesn't exist, it creates an empty list.
    try:
        file_object = open("names.pydata", "rb")
        names = pickle.load(file_object)
        file_object.close()
        return names
    except Exception as e:
        print(e)
        return []


def choice_1():
    print("Selected 1")


def choice_2():
    print("Selected 2")


def choice_3():
    print("Selected 3")


def quit():
    # This function dumps the names into a file, and prints a quit message.
    try:
        file_object = open("names.pydata", "wb")
        pickle.dump(names, file_object)
        file_object.close()
        print("\nThanks for using this program.")
    except Exception as e:
        print("\nThanks for playing. I won't be able to remember these names.")
        print(e)


### MAIN PROGRAM ###

# Set up a loop where users can choose what they'd like to do.
names = load_names()

choice = ""
display_title_bar()
while choice != "q":

    choice = get_user_choice()

    # Respond to the user's choice.
    display_title_bar()
    if choice == "1":
        # choice_1()
        calculate_substance_properties("H2O")
        # Example usage:
        # chemical_formula = "H2SO4"

        # unicode_formula, molar_mass = calculate_substance_properties(chemical_formula)
        # print("Unicode formula: %s" %(unicode_formula))
        # print("Molar mass: %s" %(molar_mass))
    elif choice == "2":
        choice_2()

    elif choice == "3":
        choice_3()
    elif choice == "q":
        quit()
        print("\nHave a good day.")
