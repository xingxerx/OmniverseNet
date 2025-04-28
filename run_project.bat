@echo off
cargo run
cd ./Assets/Scripts
csc /t:library UserManager.cs AIController.cs
cd ../../..
python -m venv.venv
.venv\Scripts\activate
python -m pip install -r.venv\Lib\site-packages\pandas\requirements.txt
cd ai_models
python prediction_model.py conversation_model.py
cd ..
unity .
