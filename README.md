# Loan Approval Prediction System

A machine learning-based web application for predicting loan approval status using customer financial and personal information.

## Features

- **Machine Learning Model**: Random Forest classifier trained on loan approval dataset
- **Web Interface**: Modern, responsive frontend for easy data input
- **REST API**: Flask backend with prediction and history endpoints
- **Database Integration**: MySQL database for storing predictions
- **Real-time Predictions**: Instant loan approval probability calculation

## Project Structure

```
loan-approval/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── train.py              # Model training script
│   ├── requirements.txt      # Python dependencies
│   ├── env.example           # Environment variables template
│   ├── model/
│   │   ├── loan_approval_pipeline.pkl  # Trained model
│   │   └── eval_metrics.json           # Model evaluation metrics
│   └── db/
│       ├── db_config.py      # Database configuration
│       └── schema.sql        # Database schema
├── frontend/
│   ├── index.html            # Main web interface
│   ├── script.js             # Frontend JavaScript
│   └── styles.css            # CSS styling
└── loan_approval_dataset.csv # Training dataset
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
- Web browser

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**

   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**

   ```bash
   cp env.example .env
   ```

   Edit `.env` file with your MySQL credentials.

6. **Set up database:**

   - Create MySQL database
   - Run the schema: `mysql -u root -p < db/schema.sql`

7. **Train the model (if needed):**

   ```bash
   python train.py
   ```

8. **Start the backend server:**
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Open index.html in a web browser:**
   - Double-click the file, or
   - Use a local server: `python -m http.server 8000`

## API Endpoints

### Health Check

- **GET** `/api/health`
- Returns system status and model loading status

### Prediction

- **POST** `/api/predict`
- Input: JSON with loan application data
- Output: Prediction result with probability

### History

- **GET** `/api/history`
- Returns recent prediction history

## Input Fields

The application expects the following fields:

- `no_of_dependents`: Number of dependents (0-10)
- `education`: "Graduate" or "Not Graduate"
- `self_employed`: "Yes" or "No"
- `income_annum`: Annual income (numeric)
- `loan_amount`: Requested loan amount (numeric)
- `loan_term`: Loan term in months (1-60)
- `cibil_score`: CIBIL credit score (300-900)
- `residential_assets_value`: Value of residential assets (numeric)
- `commercial_assets_value`: Value of commercial assets (numeric)
- `luxury_assets_value`: Value of luxury assets (numeric)
- `bank_asset_value`: Value of bank assets (numeric)

## Model Information

- **Algorithm**: Random Forest Classifier
- **Features**: 11 input features
- **Target**: Binary classification (Approved/Rejected)
- **Preprocessing**: StandardScaler for numeric features, OneHotEncoder for categorical features

## Troubleshooting

### Common Issues

1. **Model not loading:**

   - Ensure `loan_approval_pipeline.pkl` exists in `backend/model/`
   - Run `train.py` to generate the model

2. **Database connection errors:**

   - Check MySQL server is running
   - Verify credentials in `.env` file
   - Ensure database and tables exist

3. **CORS errors:**

   - Backend includes CORS support
   - Ensure frontend is accessing correct backend URL

4. **Port conflicts:**
   - Backend runs on port 5000
   - Change port in `app.py` if needed

### Error Messages

- **"Model not loaded"**: Check model file exists and is valid
- **"Database connection failed"**: Verify MySQL setup and credentials
- **"Missing required fields"**: Ensure all form fields are filled

## Development

### Adding New Features

1. **New API endpoints**: Add routes in `app.py`
2. **Frontend changes**: Modify `index.html`, `script.js`, or `styles.css`
3. **Model improvements**: Update `train.py` and retrain

### Testing

- Test API endpoints using tools like Postman
- Validate frontend functionality in different browsers
- Check responsive design on mobile devices

## License

This project is for educational purposes. Please ensure compliance with data privacy regulations when using in production.

## Support

For issues or questions:

1. Check the troubleshooting section
2. Verify all setup steps are completed
3. Check console logs for detailed error messages
