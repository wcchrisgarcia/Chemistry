# https://introtopython.org/terminal_apps.html

import os
import pickle

from chempy import Substance
import quantities as q
from sympy import Eq, symbols
from sympy.solvers.solveset import linsolve

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


def balance_equation():
    """
    Balances a chemical equation by solving linear equations
    based on the law of conservation of mass.
    """
    print("\nEnter your chemical equation in the format: H2 + O2 -> H2O")
    equation = input("Chemical Equation: ")

    try:
        reactants, products = equation.split("->")
        reactants = reactants.strip().split("+")
        products = products.strip().split("+")

        print("\nBalancing equations program is still basic...")
        print("But for H2 + O2 -> H2O, the balanced equation is: 2H2 + O2 -> 2H2O")
    except ValueError:
        print("Invalid format. Please use the correct format (e.g., H2 + O2 -> H2O).")


def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system("clear")

    print("\t**********************************************")
    print("\t************Chemistry Calculator**************")
    print("\t**********************************************")


def get_user_choice():
    # Let users know what they can do.
    print("\n[1] Calculate Molar Mass.")
    print("[2] Balance Chemical Equation.")
    print("[3] Calculate Concentration of an Equilibrium Reaction.")
    print("[q] Quit.")

    return input("What would you like to do? ")


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
names = []  # No longer loading names, as not used in this example

choice = ""
display_title_bar()
while choice != "q":

    choice = get_user_choice()

    # Respond to the user's choice.
    display_title_bar()
    if choice == "1":
        # Example: calculate properties for H2O
        calculate_substance_properties("H2O")
    elif choice == "2":
        # Balancing chemical equations
        balance_equation()
    elif choice == "3":
        print("Concentration calculator not implemented yet.")
    elif choice == "q":
        quit()
        print("\nHave a good day.")
