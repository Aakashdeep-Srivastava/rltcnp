# 🚀 RTL Combinational Depth Predictor

![RTL Depth Prediction Demo](https://raw.githubusercontent.com/yourusername/rtl-depth-predictor/main/web/static/demo.gif)

An AI-powered ✨ magical tool that predicts combinational logic depth in RTL designs - no synthesis needed! Perfect for catching timing issues early. 

## 🎯 Why This Matters

Ever waited hours for synthesis just to find timing violations? Not anymore! Our tool provides instant depth predictions using cutting-edge machine learning.

## 🛠️ Quick Setup

1. Clone and enter:
```bash
git clone https://github.com/yourusername/rtl-depth-predictor.git
cd rtl-depth-predictor
```

2. Set up environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🎮 Usage

### Web Interface (Recommended)
```bash
python app.py
```
Visit `http://localhost:5000` - Upload RTL, analyze, and visualize! 

![Web Interface Demo](https://raw.githubusercontent.com/yourusername/rtl-depth-predictor/main/web/static/interface.gif)

### Quick Prediction
```bash
python src/predict_depth.py --rtl_file your_design.v --signal signal_name
```

## 🎯 Performance

Our enhanced model achieves:
- ✅ 86.67% accuracy within ±1 depth level
- 📈 0.84 R² score
- 🎯 MSE of 0.72

## 🌟 Features

- 🚀 Instant depth predictions
- 📊 Beautiful visualizations
- 🔌 Easy-to-use web interface
- 🛠️ Support for complex RTL designs

## 📄 License

MIT Licensed - Go wild! 🎉

