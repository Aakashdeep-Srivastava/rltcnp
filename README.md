# RTL Combinational Depth Predictor

An AI-based tool to predict the combinational logic depth of signals in RTL designs without running full synthesis, helping to identify potential timing violations early in the design process.

## Problem Statement

Timing analysis is a crucial step in the design of any complex IP/SoC. However, timing analysis reports are generated after synthesis is complete, which is a very time-consuming process. This leads to overall delays in project execution time as timing violations can require architectural refactoring.

This tool uses machine learning to predict the combinational logic depth of signals in behavioral RTL, which can greatly speed up the timing analysis process.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Icarus Verilog for RTL parsing

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/rtl-depth-predictor.git
cd rtl-depth-predictor
```

2. Create and activate the virtual environment:

```bash
# On Unix/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create necessary directories:

```bash
mkdir -p models plots
```

## Usage

### Web Interface

The easiest way to use the tool is through the web interface:

```bash
# On Unix/macOS
python3 app.py

# On Windows
python app.py
```

Then open your browser and navigate to `http://localhost:5000`.

The web interface allows you to:

- Upload RTL files
- Select signals to analyze
- View predicted combinational depths
- Visualize feature importance
- Access documentation and help

### Running the Complete Pipeline

The easiest way to run the pipeline is using the `run_pipeline.py` script:

```bash
# On Unix/macOS
# Train the model and compare different model types
python3 run_pipeline.py --train --compare_models

# On Windows
# Train the model and compare different model types
python run_pipeline.py --train --compare_models
```

For predicting depth or running tests:

```bash
# On Unix/macOS
# Predict depth for a signal in an RTL file
python3 run_pipeline.py --predict --rtl_file path/to/your/rtl_file.v --signal signal_name

# Run tests
python3 run_pipeline.py --test

# On Windows
# Predict depth for a signal in an RTL file
python run_pipeline.py --predict --rtl_file path/to/your/rtl_file.v --signal signal_name

# Run tests
python run_pipeline.py --test
```

### Training the Model

```bash
# On Unix/macOS
# Basic training
python3 src/train_model.py --data_path data/training_data.csv --test_data_path data/test_data.csv --model_output models/depth_predictor.joblib

# On Windows
# Basic training
python src/train_model.py --data_path data/training_data.csv --test_data_path data/test_data.csv --model_output models/depth_predictor.joblib
```

For comparing different model types:

```bash
# On Unix/macOS
python3 src/train_model.py --data_path data/training_data.csv --test_data_path data/test_data.csv --model_output models/depth_predictor.joblib --compare_models --plot_results

# On Windows
python src/train_model.py --data_path data/training_data.csv --test_data_path data/test_data.csv --model_output models/depth_predictor.joblib --compare_models --plot_results
```

### Predicting Combinational Depth

```bash
# On Unix/macOS
python3 src/predict_depth.py --rtl_file path/to/your/rtl_file.v --signal signal_name --model_path models/depth_predictor.joblib

# On Windows
python src/predict_depth.py --rtl_file path/to/your/rtl_file.v --signal signal_name --model_path models/depth_predictor.joblib
```

### Evaluating the Model

```bash
# On Unix/macOS
# Evaluate on test data
python3 evaluate_model.py

# Generate detailed visualizations
python3 visualize_results.py

# On Windows
# Evaluate on test data
python evaluate_model.py

# Generate detailed visualizations
python visualize_results.py
```

### Running Tests

```bash
# On Unix/macOS
python3 -m unittest discover tests

# On Windows
python -m unittest discover tests
```

### Running the Complete Pipeline with Shell Script

On Unix/macOS:

```bash
bash run_all.sh
```

On Windows (using Git Bash or WSL):

```bash
bash run_all.sh
```

## Deployment

### Local Deployment

For local deployment, you can run:

```bash
python app.py
```

### Vercel Deployment

This project is configured for deployment on Vercel. To deploy:

1. **Using the deployment helper script**:

   ```bash
   python deploy.py
   ```

   Follow the prompts to deploy using Vercel CLI or prepare for GitHub deployment.

2. **Manual deployment**:
   - See the detailed instructions in `VERCEL_DEPLOYMENT.md`

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t rtl-depth-predictor .
```

2. Run the container:

```bash
docker run -p 5000:5000 rtl-depth-predictor
```

## Project Structure

```
rtl_depth_predictor/
├── data/                  # Training and test datasets
│   ├── training_data.csv  # Training dataset
│   ├── test_data.csv      # Test dataset
│   ├── sample_rtl_1.v     # Sample RTL file (counter)
│   ├── sample_rtl_2.v     # Sample RTL file (alu)
│   └── sample_rtl_3.v     # Sample RTL file (fifo_controller)
├── models/                # Trained model files
│   └── depth_predictor.joblib  # Saved model
├── notebooks/             # Jupyter notebooks for exploration
│   └── model_exploration.ipynb
├── plots/                 # Visualization plots
├── src/                   # Source code
│   ├── feature_extraction.py  # RTL feature extraction
│   ├── model.py           # ML model definition
│   ├── train_model.py     # Model training script
│   └── predict_depth.py   # Prediction script
├── tests/                 # Test files
│   └── test_model.py      # Model tests
├── web/                   # Web application
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   └── app.py             # Flask application
├── app.py                 # Main entry point
├── evaluate_model.py      # Model evaluation script
├── visualize_results.py   # Visualization script
├── run_pipeline.py        # Pipeline execution script
├── run_all.sh             # Shell script to run complete pipeline
├── Procfile               # For Heroku deployment
├── vercel.json            # For Vercel deployment
├── deploy.py              # Deployment helper script
├── test_app.py            # Script to test the app locally
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not in version control)
├── .gitignore             # Git ignore file
├── VERCEL_DEPLOYMENT.md   # Vercel deployment guide
└── README.md              # Project documentation
```

## Model Performance

The Random Forest Regressor model performs best on our enhanced dataset with the following metrics:

- MSE: 0.7233 (improved from 0.8135)
- MAE: 0.4910 (improved from 0.6238)
- R²: 0.8375 (improved from 0.5119)
- Within ±1 depth level: 86.67% (improved from 77.78%)

### Enhanced Dataset

We significantly improved the model's performance by enhancing the dataset:

1. **Enhanced Training Data**:

   - Added 60 new examples covering 5 additional module types (FPU, DSP, Video Processor, Crypto Engine, PCIe Controller, and Cache Controller)
   - Included more complex circuits with higher combinational depths (up to 12)
   - Added more diverse signal types with various combinations of operators

2. **Enhanced Test Data**:
   - Added 12 new test examples from the new module types
   - Included signals with higher combinational depths to test the model's ability to predict more complex circuits

The significant improvement in model performance after enhancing the dataset demonstrates the importance of diverse and representative training data in machine learning applications for hardware design.

## Approach

1. **Data Collection**: Generate synthetic RTL designs and extract their combinational depth using synthesis tools.
2. **Feature Engineering**: Extract relevant features from RTL code that influence combinational depth.
3. **Model Selection**: Compare different ML algorithms to find the best predictor.
4. **Training**: Train the selected model on the dataset.
5. **Evaluation**: Evaluate the model's accuracy and performance.
6. **Dataset Enhancement**: Expand the dataset with more diverse RTL designs and module types.
7. **Model Refinement**: Retrain and optimize the model with the enhanced dataset.
8. **Web Interface**: Create a user-friendly web interface for easy access to the tool.
9. **Deployment**: Deploy the application to make it accessible to users.

## License

MIT
