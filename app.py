from flask import Flask, render_template, request, jsonify
import sympy as sp
import re
import os

app = Flask(__name__)
app.debug = True  # Enable Flask Debug Mode for better error tracking

# Preprocessing function to format mathematical expressions correctly.
def preprocess(expr):
    expr = re.sub(r'(?<=[\d\w\)])(?=\()', '*', expr)
    expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
    return expr

# Home route: Processes Partial Fraction and Z-Transform computations via form submissions.
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""   # Holds the Partial Fraction result.
    z_result = "" # Holds the Z-Transform result.

    if request.method == "POST":
        # Partial Fraction Computation
        if "numerator" in request.form and "denominator" in request.form:
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

        # Z-Transform Computation
        elif "sequence" in request.form and "variable" in request.form:
            sequence_expr = request.form["sequence"]
            variable = request.form["variable"]

            try:
                symbol = sp.Symbol(variable)
                seq_expr = sp.sympify(preprocess(sequence_expr))
                z = sp.Symbol('z')
                n = sp.Symbol('n')
                # Compute the Z-transform using finite summation (n = 0 to 20)
                z_transformed = sp.summation(seq_expr * z**(-n), (n, 0, 20))
                z_result = sp.latex(z_transformed)
            except Exception as e:
                z_result = f"Error: {e}"

    return render_template("index.html", result=result, z_result=z_result)

# JSON endpoint for Inverse Matrix & Determinant via AJAX.
@app.route('/inverse_matrix', methods=['POST'])
def inverse_matrix():
    data = request.get_json()
    matrix_values = data.get("matrix")
    try:
        matrix = sp.Matrix(matrix_values)
        # Get the determinant as an exact value.
        determinant = matrix.det()
        if determinant != 0:
            inverse = matrix.inv()
            # Convert each matrix element to its string form,
            # preserving exact fraction representation (P/Q notation).
            inverse_serializable = [[str(cell) for cell in row] for row in inverse.tolist()]
            message = "Inverse computed successfully."
        else:
            inverse_serializable = None
            message = "Matrix is singular; an inverse cannot be computed."
        return jsonify({
            "determinant": str(determinant),
            "inverse": inverse_serializable,
            "message": message
        })
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})

# Run the application.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)