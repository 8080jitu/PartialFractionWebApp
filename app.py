from flask import Flask, render_template, request
import sympy as sp
import re
import os

app = Flask(__name__)
app.debug = True  # Enable Flask Debug Mode for better error tracking

# Preprocessing function to format mathematical expressions correctly
def preprocess(expr):
    expr = re.sub(r'(?<=[\d\w\)])(?=\()', '*', expr)
    expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
    return expr

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""  # Partial Fraction result
    z_result = ""  # Z-Transform result

    if request.method == "POST":
        if "numerator" in request.form and "denominator" in request.form:  # Partial Fraction Computation
            numerator = request.form["numerator"]
            denominator = request.form["denominator"]
            variable = request.form["variable"]

            try:
                symbol = sp.Symbol(variable)
                num_expr = sp.sympify(preprocess(numerator))
                denom_expr = sp.sympify(preprocess(denominator))

                expr = num_expr / denom_expr
                apart_expr = sp.apart(expr, symbol)

                result = sp.latex(apart_expr)

            except Exception as e:
                result = f"Error: {e}"

        elif "sequence" in request.form and "variable" in request.form:  # Z-Transform Computation
            sequence_expr = request.form["sequence"]
            variable = request.form["variable"]

            try:
                symbol = sp.Symbol(variable)
                seq_expr = sp.sympify(preprocess(sequence_expr))

                # Compute Z-transform using finite summation
                z = sp.Symbol('z')
                n = sp.Symbol('n')
                z_transformed = sp.summation(seq_expr * z**(-n), (n, 0, 20))

                z_result = sp.latex(z_transformed)

            except Exception as e:
                z_result = f"Error: {e}"

    return render_template("index.html", result=result, z_result=z_result)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Correctly sets port for deployment
    app.run(host="0.0.0.0", port=port)
