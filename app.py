# Import libraries
from flask import Flask, render_template, request,redirect,url_for
# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id':1, 'date':'2023-05-02', 'amount': 100},
    {'id':2, 'date':'2023-07-23', 'amount': -200},
    {'id':3, 'date':'2023-10-02', 'amount': 400},
    {'id':4, 'date':'2023-10-17', 'amount': 300},
    {'id':5, 'date':'2023-05-11', 'amount': 600},
]

# Read operation
@app.route('/', methods=['GET'])
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route('/add', methods=['GET','POST'])
def add_transaction():
    try:
        if request.method == 'POST':

            new_transaction = {
                'id': len(transactions) + 1,
                'date': request.form['date'],
                'amount' : request.form['amount']
            }
            transactions.append(new_transaction)
        
            return redirect(url_for("get_transactions"))
    except NameError:
        return {"message" : "Error Occured!"}
    return render_template('form.html')

# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    return render_template(url_for("get_transactions"))

# search opreation
@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])

        filtered_transactions = [t for t in transactions if min <= t['amount'] <= max]
        return render_template('transactions.html', transactions=filtered_transactions)
    
    elif request.method == 'GET':
        return render_template('search.html')


#total balance function
@app.route('/balance')
def total_balance():
        total_balance = sum(float(transaction['amount']) for transaction in transactions)
        return render_template('transactions.html', transactions=transactions, total_balance=total_balance)
    





# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)    
