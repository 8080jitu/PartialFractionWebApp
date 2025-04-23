from flask import Flask, render_template, request
import sympy as sp
import re

app = Flask(__name__)

def preprocess(expr):
    # Logic to preprocess input (similar to your original code)
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
            result = str(apart_expr)
        except Exception as e:
            result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

