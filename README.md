
# SA Price Compare Backend

Flask backend for the South African supermarket price comparison app.

## Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Run the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

- `POST /api/search-product` - Search by product name
- `POST /api/search-barcode` - Search by barcode  
- `POST /api/cache` - Get cached results
- `POST /api/cache/update` - Update cache
- `GET /api/health` - Health check

## Next Steps

1. Implement actual supermarket API integrations
2. Add Supabase database connection for caching
3. Implement web scraping for supermarket websites
4. Add authentication and rate limiting
5. Set up periodic cache refresh jobs

The current implementation returns mock data for testing the frontend.
