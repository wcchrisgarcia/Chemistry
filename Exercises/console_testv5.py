from chempy import Substance
import quantities as q
from chempy import balance_stoichiometry
from collections import defaultdict
from chempy.equilibria import EqSystem
from math import log10


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
    print("\t**********************************************")
    print("\t************Chemistry Calculator***************")
    print("\t**********************************************")


def get_user_choice():
    print("\n[1] Calculate Molar Mass.")
    print("[2] Balance Chemical Equation.")
    print("[3] Calculate Concentration of an Equilibrium Reaction.")
    print("[q] Quit.")
    return input("What would you like to do? ").strip().lower()


def balance_chemical_equation(reaction_string):
    """
    Balances a chemical equation using chempy.

    Parameters:
    reaction_string (str): A string representing the chemical equation, e.g., "H2 + O2 -> H2O".

    Returns:
    str: A string representing the balanced chemical equation or an error message if balancing fails.
    """
    try:
        # Parse reactants and products and split by "->"
        reactants, products = reaction_string.split("->")
        reactants = {mol.strip(): 1 for mol in reactants.split("+")}
        products = {mol.strip(): 1 for mol in products.split("+")}
        balanced_reactants, balanced_products = balance_stoichiometry(
            reactants, products
        )

        return (
            " + ".join([f"{coeff} {mol}" for mol, coeff in balanced_reactants.items()])
            + " -> "
            + " + ".join([f"{coeff} {mol}" for mol, coeff in balanced_products.items()])
        )
    except Exception as e:
        return f"Error balancing equation: {e}"


def calculate_equilibrium_and_ph(initial_concentrations, equilibrium_expression):
    """
    Calculate equilibrium concentrations and pH from given initial concentrations and equilibrium expression.

    Parameters:
    initial_concentrations (dict): A dictionary containing the initial concentrations of all species involved in the equilibrium.
    equilibrium_expression (str): The equilibrium expression in the format 'A = B + C; K'.

    Returns:
    dict: A dictionary containing the equilibrium concentrations of all species.
    float: The pH of the solution.
    float: The H+ concentration at equilibrium.
    """
    eqsys = EqSystem.from_string(equilibrium_expression)
    arr, _, _ = eqsys.root(initial_concentrations)
    conc = dict(zip(eqsys.substances, arr))
    pH = -log10(conc.get("H+", 1e-7))
    h_concentration = conc.get("H+", 1e-7)
    return conc, pH, h_concentration


def calculate_equilibrium_and_ph():
    """
    Handles user input for calculating equilibrium and pH.
    """
    print(
        "Enter the equilibrium reaction (e.g., 'HC2H3O2 = H+ + C2H3O2-; 1.8*10**-5'):"
    )
    equilibrium_expression = input("Equilibrium Expression: ").strip()

    print(
        "Enter the initial concentrations of species (e.g., 'HC2H3O2:0.2,H+:1e-7,C2H3O2-:0.1'):"
    )
    concentrations_input = input("Initial Concentrations: ").strip()

    try:
        # Parse user input into a dictionary
        initial_conditions = defaultdict(
            float,
            {
                item.split(":")[0].strip(): float(item.split(":")[1].strip())
                for item in concentrations_input.split(",")
            },
        )
    except Exception as e:
        print(f"Error parsing concentrations: {e}")
        return

    # Perform the equilibrium calculation
    try:
        equilibrium_concentrations, pH_value, h_plus_concentration = (
            calculate_equilibrium_and_ph(initial_conditions, equilibrium_expression)
        )
        print("\nResults:")
        print("Equilibrium Concentrations:", equilibrium_concentrations)
        print(f"pH: {pH_value:.2f}")
        print(f"H+ concentration: {h_plus_concentration:.2e}")
    except Exception as e:
        print(f"Error calculating equilibrium and pH: {e}")


### MAIN PROGRAM ###
display_title_bar()
choice = ""
while choice != "q":
    choice = get_user_choice()
    display_title_bar()

    if choice == "1":
        chemical_formula = input("Enter your chemical formula (e.g., NaCl, H2O): ")
        calculate_substance_properties(chemical_formula)

    elif choice == "2":
        reaction_string = input(
            "Enter the chemical reaction to balance (e.g., H2 + O2 -> H2O): "
        )
        balanced_reaction_string = balance_chemical_equation(reaction_string)
        print("Balanced Reaction:", balanced_reaction_string)

    elif choice == "3":
        calculate_equilibrium_and_ph()

    elif choice == "q":
        print("\nHave a good day!")
