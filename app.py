from flask import Flask, render_template, request

app = Flask(__name__)

# Define common feed elements and their typical protein content
feed_elements = {
    "Corn": 8.5,
    "Soybean meal": 44.0,
    "Wheat": 12.0,
    "Barley": 11.5,
    "Oats": 11.5,
    "Fishmeal": 60.0,
    "Meat and bone meal": 50.0,
    "Alfalfa meal": 17.0,
    "Cottonseed meal": 41.0,
    "Peanut meal": 45.0,
    "Canola meal": 38.0,
    "Rice bran": 13.0,
    "Distillers dried grains": 27.0,
    "Blood meal": 80.0,
    "Corn gluten meal": 60.0,
    "Other (custom)": 0.0
}

def pearsons_square(protein1, protein2, desired_protein):
    """Calculate the proportions using Pearson's Square method."""
    part1 = abs(protein2 - desired_protein)
    part2 = abs(protein1 - desired_protein)
    total = part1 + part2
    proportion1 = part1 / total
    proportion2 = part2 / total
    return proportion1, proportion2

@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        try:
            feed1 = request.form['feed1']
            protein1 = float(request.form['protein1']) if feed1 == "Other (custom)" else feed_elements[feed1]
            feed2 = request.form['feed2']
            protein2 = float(request.form['protein2']) if feed2 == "Other (custom)" else feed_elements[feed2]
            desired_protein = float(request.form['desired_protein'])
            total_weight = float(request.form['total_weight'])

            if protein1 == protein2:
                return render_template('index.html', error="Protein contents must be different", feed_elements=feed_elements)

            if not (min(protein1, protein2) < desired_protein < max(protein1, protein2)):
                return render_template('index.html', error="Desired protein must be between the two feed protein contents", feed_elements=feed_elements)

            prop1, prop2 = pearsons_square(protein1, protein2, desired_protein)
            weight1 = prop1 * total_weight
            weight2 = prop2 * total_weight

            result = {
                'feed1': feed1,
                'protein1': protein1,
                'weight1': round(weight1, 2),
                'proportion1': round(prop1 * 100, 2),
                'feed2': feed2,
                'protein2': protein2,
                'weight2': round(weight2, 2),
                'proportion2': round(prop2 * 100, 2),
                'total_weight': total_weight,
                'desired_protein': desired_protein
            }

            return render_template('result.html', result=result)
        except ValueError:
            return render_template('index.html', error="Please enter valid numbers", feed_elements=feed_elements)

    return render_template('index.html', feed_elements=feed_elements)

if __name__ == '__main__':
    app.run(debug=True)
