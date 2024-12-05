from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def equilibrium():
    equilibrium_expr = None
    reaction = None

    if request.method == "POST":
        reaction = request.form["reaction"]

        # Parse the reaction and construct the equilibrium expression
        reactants, products = reaction.split("->")
        reactants = reactants.split("+")
        products = products.split("+")

        # Prepare the LaTeX formatted equilibrium expression
        reactants_str = " * ".join([f"[{r.strip()}]" for r in reactants])
        products_str = " * ".join([f"[{p.strip()}]" for p in products])
        equilibrium_expr = f"K = \\frac{{ {products_str} }}{{ {reactants_str} }}"

    # HTML Template with MathJax
    html_template = """
    <!doctype html>
    <html>
    <head>
        <title>Equilibrium Calculator</title>
        <script type="text/javascript" async
            src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>
    </head>
    <body>
        <h2>Enter the chemical reaction (e.g., 2A + 4B -> 3C + 10D):</h2>
        <form method="post">
            <input type="text" name="reaction" style="width: 400px;" value="{{ reaction if reaction }}">
            <input type="submit" value="Calculate">
        </form>

        {% if equilibrium_expr %}
        <h3>Equilibrium Expression:</h3>
        <p>$$ {{ equilibrium_expr }} $$</p>
        {% endif %}
    </body>
    </html>
    """

    return render_template_string(
        html_template, equilibrium_expr=equilibrium_expr, reaction=reaction
    )


if __name__ == "__main__":
    app.run(debug=True)
