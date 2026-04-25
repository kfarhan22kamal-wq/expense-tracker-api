from flask import Flask, request, jsonify

app = Flask(__name__)

expenses = []
expense_id = 1

@app.route("/")
def home():
    return jsonify({"message": "Expense Tracker API Running"})

# CREATE
@app.route("/expenses", methods=["POST"])
def add_expense():
    global expense_id
    
    data = request.get_json()

    if not data or "name" not in data or "amount" not in data:
        return jsonify({"error": "Invalid input"}), 400

    if not isinstance(data["amount"], (int, float)):
        return jsonify({"error": "Amount must be number"}), 400

    expense = {
        "id": expense_id,
        "name": data["name"],
        "amount": data["amount"]
    }

    expenses.append(expense)
    expense_id += 1

    return jsonify({"message": "Expense added", "data": expense}), 201

# READ ALL
@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses)

# DELETE
@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    global expenses
    expenses = [e for e in expenses if e["id"] != id]
    return jsonify({"message": "Deleted if existed"})

# TOTAL
@app.route("/expenses/total", methods=["GET"])
def total_expense():
    total = sum(e["amount"] for e in expenses)
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run(debug=True)