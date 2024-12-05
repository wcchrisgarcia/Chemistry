import re


def parse_reaction(reaction):
    sides = reaction.split("->")
    reactants = parse_compounds(sides[0])
    products = parse_compounds(sides[1])
    return reactants, products


def parse_compounds(compound_string):
    compounds = compound_string.strip().split("+")
    compound_dict = {}
    for compound in compounds:
        match = re.match(r"(\d*)\s*([A-Za-z0-9]+)", compound.strip())
        if match:
            coeff = int(match.group(1)) if match.group(1) else 1
            name = match.group(2)
            compound_dict[name] = coeff
    return compound_dict


def get_equilibrium_expression(reactants, products):
    reactants_part = " * ".join(
        [f"[{name}]**{coeff}" for name, coeff in reactants.items()]
    )
    products_part = " * ".join(
        [f"[{name}]**{coeff}" for name, coeff in products.items()]
    )
    return f"K = ({products_part}) / ({reactants_part})"


def main():
    reaction = input("Enter the chemical reaction (e.g., 2A + 4B -> 3C + 10D): ")
    reactants, products = parse_reaction(reaction)

    print("\nParsed Reaction:")
    print("Reactants:", reactants)
    print("Products:", products)

    equilibrium_expression = get_equilibrium_expression(reactants, products)
    print("\nEquilibrium Expression:")
    print(equilibrium_expression)

    # Ask the user what they want to solve for
    variables = list(reactants.keys()) + list(products.keys()) + ["K"]
    print("\nAvailable variables to solve for:", ", ".join(variables))
    to_solve = input("Which variable would you like to solve for? ").strip()

    if to_solve in variables:
        known_values = {}
        for variable in variables:
            if variable != to_solve:
                value = float(
                    input(f"Enter the value for {variable} (concentration or K): ")
                )
                known_values[variable] = value

        # Calculate the requested variable
        if to_solve == "K":
            # Calculate equilibrium constant K
            numerator = 1
            for name, coeff in products.items():
                numerator *= known_values[name] ** coeff

            denominator = 1
            for name, coeff in reactants.items():
                denominator *= known_values[name] ** coeff

            K = numerator / denominator
            print(f"\nEquilibrium constant (K): {K:.2f}")

        else:
            # Solve for concentration of a specific compound
            if to_solve in reactants:
                coeff = reactants[to_solve]
            else:
                coeff = products[to_solve]

            # Rearranging to solve for the desired concentration
            if to_solve in products:
                K = known_values["K"]
                denominator = 1
                for name, c in reactants.items():
                    denominator *= known_values[name] ** c
                numerator = K * denominator
                for name, c in products.items():
                    if name != to_solve:
                        numerator /= known_values[name] ** c
                concentration = numerator ** (1 / coeff)
            elif to_solve in reactants:
                K = known_values["K"]
                numerator = 1
                for name, c in products.items():
                    numerator *= known_values[name] ** c
                denominator = numerator / K
                for name, c in reactants.items():
                    if name != to_solve:
                        denominator /= known_values[name] ** c
                concentration = denominator ** (1 / coeff)

            print(f"\nConcentration of {to_solve}: {concentration:.2f}")

    else:
        print("Invalid variable selected.")


if __name__ == "__main__":
    main()
