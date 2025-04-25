from flask import Flask, render_template, request
import sympy as sp
import re

app = Flask(__name__)

def preprocess(expr):
    expr = re.sub(r'(?<=[\d\w\)])(?=\()', '*', expr)
    expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
    return expr

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
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

    return render_template("index.html", result=result)

@app.route("/ztransform", methods=["GET", "POST"])
def ztransform():
    z_result = ""
    if request.method == "POST":
        sequence_expr = request.form["sequence"]
        variable = request.form["variable"]

        try:
            symbol = sp.Symbol(variable)
            seq_expr = sp.sympify(preprocess(sequence_expr))

            z_transformed = sp.ztrans(seq_expr, symbol)
            
            z_result = sp.latex(z_transformed)

        except Exception as e:
            z_result = f"Error: {e}"

    return render_template("ztransform.html", result=z_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)


