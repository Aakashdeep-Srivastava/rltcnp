import os
import sys
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import joblib
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add the parent directory to sys.path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.feature_extraction import extract_features_from_rtl
from src.model import DepthPredictor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development')

# Use /tmp directory for Vercel serverless environment
if os.environ.get('VERCEL_ENV') == 'production':
    app.config['UPLOAD_FOLDER'] = '/tmp'
else:
    app.config['UPLOAD_FOLDER'] = os.path.join(tempfile.gettempdir(), 'rtl_uploads')

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['MODEL_PATH'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'depth_predictor.joblib')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
model = None
try:
    model = DepthPredictor.load(app.config['MODEL_PATH'])
except Exception as e:
    print(f"Error loading model: {e}")

# Allowed file extensions
ALLOWED_EXTENSIONS = {'v', 'sv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Add sample RTL files for quick testing
    sample_files = [
        {'name': 'counter.v', 'description': 'Simple counter module'},
        {'name': 'alu.v', 'description': 'Arithmetic Logic Unit'},
        {'name': 'fifo_controller.v', 'description': 'FIFO Controller'}
    ]
    return render_template('index.html', sample_files=sample_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get signals from the RTL file
        try:
            signals = extract_features_from_rtl(filepath, get_signals_only=True)
            return jsonify({'success': True, 'signals': signals, 'filename': filename})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    filename = data.get('filename')
    signal_name = data.get('signal')
    
    if not filename or not signal_name:
        return jsonify({'success': False, 'error': 'Missing filename or signal'})
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'success': False, 'error': 'File not found'})
    
    try:
        # Extract features for the selected signal
        features = extract_features_from_rtl(filepath, signal_name)
        
        if not features:
            return jsonify({'success': False, 'error': f'Signal {signal_name} not found in the RTL file'})
        
        # Make prediction
        if model is None:
            return jsonify({'success': False, 'error': 'Model not loaded'})
        
        # Convert features to DataFrame with correct column names
        feature_df = pd.DataFrame([features])
        
        # Predict depth
        predicted_depth = model.predict(feature_df)[0]
        
        # Generate feature importance visualization
        feature_importance = None
        if hasattr(model.model.named_steps['regressor'], 'feature_importances_'):
            plt.figure(figsize=(10, 6))
            feature_names = feature_df.columns
            importances = model.model.named_steps['regressor'].feature_importances_
            indices = np.argsort(importances)
            plt.barh(range(len(indices)), importances[indices], color='b')
            plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
            plt.xlabel('Relative Importance')
            plt.title('Feature Importance')
            
            # Save the plot to a temporary file
            feature_importance_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_{signal_name}_importance.png")
            plt.savefig(feature_importance_path)
            plt.close()
            feature_importance = f"{filename}_{signal_name}_importance.png"
        
        return jsonify({
            'success': True, 
            'predicted_depth': round(predicted_depth, 2),
            'features': features,
            'feature_importance': feature_importance
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/about')
def about():
    # Add model performance metrics
    model_metrics = {
        'mse': 0.7233,
        'mae': 0.4910,
        'r2': 0.8375,
        'accuracy_within_1': 86.67
    }
    
    # Add feature importance data
    feature_importance = [
        {'name': 'fan_in', 'importance': 0.35},
        {'name': 'operators_count', 'importance': 0.25},
        {'name': 'arithmetic_ops', 'importance': 0.15},
        {'name': 'logical_ops', 'importance': 0.12},
        {'name': 'conditional_count', 'importance': 0.08},
        {'name': 'comparison_ops', 'importance': 0.03},
        {'name': 'mux_count', 'importance': 0.02}
    ]
    
    return render_template('about.html', metrics=model_metrics, features=feature_importance)

@app.route('/documentation')
def documentation():
    # Add API examples
    api_examples = {
        'upload': {
            'url': '/upload',
            'method': 'POST',
            'content_type': 'multipart/form-data',
            'params': [{'name': 'file', 'description': 'The RTL file to upload (.v or .sv)'}],
            'response': {
                'success': True,
                'signals': ['signal1', 'signal2'],
                'filename': 'uploaded_file.v'
            }
        },
        'predict': {
            'url': '/predict',
            'method': 'POST',
            'content_type': 'application/json',
            'request_body': {
                'filename': 'uploaded_file.v',
                'signal': 'signal_name'
            },
            'response': {
                'success': True,
                'predicted_depth': 5.67,
                'features': {
                    'fan_in': 10,
                    'operators_count': 5,
                    'conditional_count': 1,
                    'arithmetic_ops': 0,
                    'logical_ops': 4,
                    'comparison_ops': 1,
                    'mux_count': 1
                },
                'feature_importance': 'uploaded_file.v_signal_name_importance.png'
            }
        }
    }
    
    # Add command examples
    command_examples = [
        {'name': 'Basic Usage', 'command': 'python run_pipeline.py --predict --rtl_file path/to/your/rtl_file.v --signal signal_name'},
        {'name': 'Training the Model', 'command': 'python run_pipeline.py --train --compare_models'},
        {'name': 'Evaluating the Model', 'command': 'python evaluate_model.py'},
        {'name': 'Generating Visualizations', 'command': 'python visualize_results.py'},
        {'name': 'Running Tests', 'command': 'python run_pipeline.py --test'},
        {'name': 'Running the Complete Pipeline', 'command': 'bash run_all.sh'}
    ]
    
    return render_template('documentation.html', api_examples=api_examples, command_examples=command_examples)

if __name__ == '__main__':
    app.run(debug=True) 