# GreenCommute Backend

Flask-based REST API for the GreenCommute application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Routes
- `POST /api/routes/search` - Search for optimal routes

### Trips
- `POST /api/trips` - Save a trip
- `GET /api/trips/<user_id>` - Get user's trip history
- `GET /api/trips/stats/<user_id>` - Get user's trip statistics

### Users
- `POST /api/users` - Create a new user
- `GET /api/users/<user_id>` - Get user details

### Transit Data
- `GET /api/transit/stops` - Get all transit stops
- `GET /api/transit/lines` - Get all transit lines

### CO2 Calculator
- `POST /api/co2/compare` - Compare CO2 emissions
