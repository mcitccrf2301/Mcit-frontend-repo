from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_ENDPOINT = os.environ.get('API_ENDPOINT')

@app.route('/')
def index():
    # In a real application, you'd fetch this from your database
    hospitals = ['Hospital A', 'Hospital B', 'Hospital C']
    return render_template('index.html', hospitals=hospitals)

@app.route('/form/<hospital>')
def form(hospital):
    return render_template('form.html', hospital=hospital)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    
    # Make API call to Lambda function via API Gateway
    response = requests.post(f"{API_ENDPOINT}/submit", json=data)
    result = response.json()
    
    return render_template('result.html', result=result)

@app.route('/check_queues')
def check_queues():
    # Make API call to Lambda function to get queue status
    response = requests.get(f"{API_ENDPOINT}/check_queues")
    queues = response.json()
    return jsonify(queues)

if __name__ == '__main__':
    app.run(debug=True)