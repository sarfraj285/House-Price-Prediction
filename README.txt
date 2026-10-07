# SmartHouseAI - House Price Prediction

## Project structure

SmartHouseAI/
├── app.py
├── requirements.txt
├── model/
│   └── model.pkl          # Put your trained model here
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── images/
        └── house.png

## Run

1. Create/activate a virtual environment.
2. Install dependencies:

   pip install -r requirements.txt

3. Put your trained sklearn model at:

   model/model.pkl

4. Start:

   python app.py

5. Open:

   http://127.0.0.1:5000/

## Important

The code expects your model pipeline to accept these columns:

area, bedrooms, bathrooms, stories, parking, location, property_type

If your existing model uses different columns, change the input_data DataFrame in app.py to match your training dataset exactly.

If model.pkl is not present, the app uses a simple demo formula so the UI can still be tested.
