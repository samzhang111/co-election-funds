from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('data/campaigns.csv')

@app.route('/')
def index():
    races = df.groupby(['race_id'])[['office', 'jurisdiction', 'district', 'race_id']].first()
    races['declared_year'] = df.groupby(['race_id']).declared_year.agg(lambda x:x.value_counts().index[0])
    race_data = list(sorted(races.T.to_dict().values(), key=lambda x: [
        x['office'], x['jurisdiction'], x['district'], x['declared_year']
    ]))
    return render_template('index.html', races=race_data)

@app.route('/race/<race_id>')
def race(race_id):
    candidates = df[df.race_id == int(race_id)]
    candidates_data = list(sorted(candidates.T.to_dict().values(), key=lambda row: row['mean']))
    return render_template('race.html', candidates=candidates_data, first=candidates_data[0])

@app.route('/candidates/<candidate_id>')
def candidate(candidate_id):
    candidate = df[df.CO_ID == int(candidate_id)]

    return render_template('candidate.html',
            candidate_id=candidate_id,
            **candidate.iloc[0].to_dict()
    )

if __name__ == '__main__':
    app.run(debug=True)
