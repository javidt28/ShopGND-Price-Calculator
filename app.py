# app.py

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sale_prices = None

    if request.method == 'POST':
        # Get form data
        total_shipment_cost = float(request.form['total_shipment_cost'])
        total_freight = float(request.form['total_freight'])
        brokerage = float(request.form['brokerage'])
        trucking = float(request.form['trucking'])

        item_names = request.form.getlist('item_name[]')
        cost_per_units = list(map(float, request.form.getlist('cost_per_unit[]')))
        quantities = list(map(float, request.form.getlist('quantity[]')))
        cets = list(map(float, request.form.getlist('cet[]')))
        vats = list(map(float, request.form.getlist('vat[]')))
        cscs = list(map(float, request.form.getlist('csc[]')))
        evls = list(map(float, request.form.getlist('evl[]')))
        markups = list(map(float, request.form.getlist('markup[]')))

        # Calculate sale prices
        sale_prices = []
        for i in range(len(item_names)):
            item_cost = cost_per_units[i] * quantities[i]
            total_cost = item_cost + (item_cost * (cets[i] + vats[i] + cscs[i] + evls[i] + markups[i]) / 100)
            total_cost += total_shipment_cost + total_freight + brokerage + trucking
            sale_prices.append(round(total_cost / quantities[i], 2))

    return render_template('index.html', sale_prices=sale_prices)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
