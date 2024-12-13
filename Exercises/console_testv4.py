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

    return input("What would you like to do? ")


def balance_chemical_equation(reaction_string):
    """
    Balances a chemical equation using chempy.

    Parameters:
    reaction_string (str): A string representing the chemical equation, e.g., "H2 + O2 -> H2O".

    Returns:
    str: A string representing the balanced chemical equation or an error message if balancing fails.
    """
    print("you choose two")

    try:
        # Parse reactants and products and split by "->"
        reactants_str, products_str = reaction_string.split("->")
        reactants_str = reactants_str.strip()
        products_str = products_str.strip()

        # Parse reactants by "+" and coefficients by spaces
        reactants = {}
        for part in reactants_str.split("+"):
            part = part.strip()
            if part:
                if " " in part:
                    coeff, molecule = part.split()
                    reactants[molecule] = int(coeff)
                else:
                    reactants[part] = 1

        # Parse products by "+" and coefficients by spaces
        products = {}
        for part in products_str.split("+"):
            part = part.strip()
            if part:
                if " " in part:
                    coeff, molecule = part.split()
                    products[molecule] = int(coeff)
                else:
                    products[part] = 1

        reactants, products = balance_stoichiometry(reactants, products)

        balanced_reaction_string = (
            " + ".join(
                [f"{coeff}{' '}{molecule}" for molecule, coeff in reactants.items()]
            )
            + " -> "
            + " + ".join(
                [f"{coeff}{' '}{molecule}" for molecule, coeff in products.items()]
            )
        )

        return balanced_reaction_string

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
    # Define the equilibrium system
    eqsys = EqSystem.from_string(equilibrium_expression)

    # Solve for equilibrium concentrations
    arr, info, sane = eqsys.root(initial_concentrations)
    conc = dict(zip(eqsys.substances, arr))

    # Calculate pH and H+ concentration
    pH = -log10(conc["H+"])
    h_concentration = conc["H+"]

    return conc, pH, h_concentration


### MAIN PROGRAM ###

# Set up a loop where users can choose what they'd like to do.


display_title_bar()
choice = ""
while choice != "q":

    choice = get_user_choice()

    # Respond to the user's choice.
    display_title_bar()
    if choice == "1":
        # choice_1()
        chemical_formula = input("Enter your chemical formula (eg., NaCl, H2O)")
        calculate_substance_properties(chemical_formula)
        # Example usage:
        # chemical_formula = "H2SO4"

        # unicode_formula, molar_mass = calculate_substance_properties(chemical_formula)
        # print("Unicode formula: %s" %(unicode_formula))
        # print("Molar mass: %s" %(molar_mass))
    elif choice == "2":
        # Example usage:
        reaction_string = input(
            "Enter the chemical reaction to balance (e.g, H2 + O2 -> H2O)"
        )
        balanced_reaction_string = balance_chemical_equation(reaction_string)
        print("Balanced Reaction:", balanced_reaction_string)
    elif choice == "3":

        # Example usage:
        initial_conditions = defaultdict(
            float, {"HC2H3O2": 0.2, "H+": 1e-7, "C2H3O2-": 0.1}
        )
        equilibrium_eq = "HC2H3O2 = H+ + C2H3O2-; 1.8*10**-5"
        equilibrium_concentrations, pH_value, h_plus_concentration = (
            calculate_equilibrium_and_ph(initial_conditions, equilibrium_eq)
        )

        print("Equilibrium Concentrations:", equilibrium_concentrations)
        print("pH: %.2f" % pH_value)
        print("H+ concentration: %.2e" % h_plus_concentration)

    elif choice == "q":
        quit()
        print("\nHave a good day.")
