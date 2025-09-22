import pickle

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sklearn.preprocessing import StandardScaler

# Initialize FastAPI app
app = FastAPI()

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

# Templates (similar to Flask's render_template)
templates = Jinja2Templates(directory="templates")

standard_to = StandardScaler()

# Home route (renders index.html)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Predict route
@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    Year: int = Form(...),
    Present_Price: float = Form(...),
    Kms_Driven: int = Form(...),
    Owner: int = Form(...),
    Fuel_Type: str = Form(...),
    Seller_Type: str = Form(...),
    Transmission: str = Form(...)
):
    # Fuel type mapping
    if Fuel_Type == "CNG":
        Fuel_Type_val = 0
    elif Fuel_Type == "Diesel":
        Fuel_Type_val = 1
    else:
        Fuel_Type_val = 2

    # Adjust Year
    Year_val = 2023 - Year

    # Seller type mapping
    Seller_Type_val = 1 if Seller_Type == "Individual" else 0

    # Transmission mapping
    Transmission_val = 1 if Transmission == "Manual" else 0

    # Prediction
    prediction = model.predict(
        [[Present_Price, Kms_Driven, Owner, Year_val, Fuel_Type_val, Seller_Type_val, Transmission_val]]
    )
    output = round(prediction[0], 2)

    # Response (render template with prediction)
    if output < 0:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "prediction_texts": "Sorry you cannot sell this car"},
        )
    else:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "prediction_text": f"You Can Sell The Car at {output}"},
        )