from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidates/<candidate_id>')
def candidate(candidate_id):
    df = pd.read_csv('data/campaigns.csv')
    candidate = df[df.CO_ID == int(candidate_id)]

    return render_template('candidate.html',
            candidate_id=candidate_id,
            **candidate.iloc[0].to_dict()
    )

if __name__ == '__main__':
    app.run(debug=True)
