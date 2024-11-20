from flask import Flask, request, render_template, send_from_directory
import boto3
import json

# Initialize Flask app
app = Flask(__name__)

# AWS SageMaker Endpoint Name (replace with your endpoint name)
ENDPOINT_NAME = "Custom-sklearn-model-2024-11-19-07-30-02"

# Initialize AWS SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime', region_name='ap-south-1')  # Replace 'your-region'

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page with a form to input smartphone features and display the prediction result.
    """
    prediction_text = None
    prediction_image = 'placeholder.svg'

    if request.method == 'POST':
        try:
            # Collect input data from the form - keeping original implementation
            features = [
                int(request.form['battery_power']),
                int(request.form['blue']),
                float(request.form['clock_speed']),
                int(request.form['dual_sim']),
                int(request.form['fc']),
                int(request.form['four_g']),
                int(request.form['int_memory']),
                float(request.form['m_dep']),
                int(request.form['mobile_wt']),
                int(request.form['n_cores']),
                int(request.form['pc']),
                int(request.form['px_height']),
                int(request.form['px_width']),
                int(request.form['ram']),
                int(request.form['sc_h']),
                int(request.form['sc_w']),
                int(request.form['talk_time']),
                int(request.form['three_g']),
                int(request.form['touch_screen']),
                int(request.form['wifi']),
            ]
            
            # Convert input data into the format expected by the model
            payload = json.dumps([features])  # SageMaker expects JSON serialized input
            
            # Call SageMaker endpoint
            response = sagemaker_runtime.invoke_endpoint(
                EndpointName=ENDPOINT_NAME,
                ContentType="application/json",
                Body=payload
            )
            
            # Parse the prediction response
            prediction = json.loads(response['Body'].read().decode())[0]
            
            # Map prediction result to human-readable text and corresponding image
            if prediction == 0:
                prediction_text = "Budget mobile phone"
                prediction_image = "budget.jpg"
            elif prediction == 1:
                prediction_text = "Lower mid-range phone"
                prediction_image = "lower-mid.jpg"
            elif prediction == 2:
                prediction_text = "Upper mid-range phone"
                prediction_image = "upper-mid.jpg"
            elif prediction == 3:
                prediction_text = "Premium phone"
                prediction_image = "premium.png"
            else:
                prediction_text = "Unknown prediction result"
                prediction_image = "placeholder.svg"
        
        except Exception as e:
            prediction_text = f"Error: {e}"
            prediction_image = "placeholder.svg"

    return render_template('index.html', 
                         prediction=prediction_text,
                         prediction_image=prediction_image)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
