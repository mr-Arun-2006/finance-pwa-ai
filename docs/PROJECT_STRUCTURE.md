# Project Structure

```
finance-pwa-ai/
├── frontend/                          # React PWA Application
│   ├── public/
│   │   ├── index.html                # Main HTML file
│   │   ├── manifest.json             # PWA manifest
│   │   └── icons/                    # App icons
│   ├── src/
│   │   ├── components/               # Reusable components
│   │   │   ├── Navbar.tsx
│   │   │   ├── StatCard.tsx
│   │   │   └── FinancialChart.tsx
│   │   ├── pages/                    # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Transactions.tsx
│   │   │   ├── Budgets.tsx
│   │   │   ├── Forecasts.tsx
│   │   │   ├── Analytics.tsx
│   │   │   └── Settings.tsx
│   │   ├── store/                    # Redux store
│   │   │   └── store.ts
│   │   ├── services/                 # API services
│   │   │   ├── api.ts
│   │   │   └── auth.ts
│   │   ├── App.tsx                   # Root component
│   │   ├── index.tsx                 # Entry point
│   │   └── index.css                 # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── .env.example
│
├── backend/                           # Node.js Backend API
│   ├── src/
│   │   ├── routes/                   # API routes
│   │   │   ├── auth.ts
│   │   │   ├── transactions.ts
│   │   │   ├── budgets.ts
│   │   │   ├── forecasts.ts
│   │   │   └── analytics.ts
│   │   ├── controllers/              # Route handlers
│   │   ├── middleware/               # Express middleware
│   │   ├── services/                 # Business logic
│   │   ├── models/                   # Database models (Prisma)
│   │   ├── utils/                    # Utility functions
│   │   └── server.ts                 # Server entry point
│   ├── prisma/
│   │   ├── schema.prisma             # Database schema
│   │   └── migrations/               # DB migrations
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env.example
│   └── Dockerfile
│
├── ml-models/                         # Python ML Pipeline
│   ├── src/
│   │   ├── main.py                   # FastAPI app
│   │   ├── expense_categorizer.py    # Category classifier
│   │   ├── fraud_detector.py         # Anomaly detection
│   │   ├── cash_flow_forecaster.py   # Time series forecasting
│   │   ├── data_processor.py         # Feature engineering
│   │   └── model_trainer.py          # Training pipeline
│   ├── models/                       # Trained model files
│   │   ├── expense_classifier.pkl
│   │   ├── fraud_detector.pkl
│   │   └── forecasting_model.pkl
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── README.md
│
├── docker/                            # Docker configuration
│   ├── nginx.conf                    # Nginx reverse proxy
│   ├── Dockerfile.frontend           # Frontend container
│   ├── Dockerfile.backend            # Backend container
│   └── Dockerfile.ml                 # ML service container
│
├── docs/                              # Documentation
│   ├── API.md                        # API documentation
│   ├── SETUP.md                      # Setup guide
│   ├── DEPLOYMENT.md                 # Deployment guide
│   ├── ML_MODELS.md                  # ML documentation
│   ├── CONTRIBUTING.md               # Contributing guide
│   ├── TROUBLESHOOTING.md            # Troubleshooting
│   └── PROJECT_STRUCTURE.md          # This file
│
├── docker-compose.yml                # Docker compose config
├── .gitignore                        # Git ignore rules
├── README.md                         # Main readme
└── LICENSE                           # MIT License
```

## Key Directories

### Frontend (`frontend/`)
- **public/**: Static files and PWA manifest
- **src/components/**: Reusable UI components
- **src/pages/**: Full page components
- **src/store/**: Redux state management
- **src/services/**: API communication layer
- **src/styles/**: Global and component styles

### Backend (`backend/`)
- **src/routes/**: Express route definitions
- **src/controllers/**: Request handlers
- **src/middleware/**: Authentication, validation
- **src/services/**: Business logic
- **src/models/**: Database models
- **prisma/**: Database schema and migrations

### ML Models (`ml-models/`)
- **src/main.py**: FastAPI server
- **src/*.py**: Individual model implementations
- **models/**: Persisted trained models
- **tests/**: Unit tests for models

### Docker (`docker/`)
- Configuration for containerization
- Separate Dockerfiles for each service
- Nginx reverse proxy config

### Docs (`docs/`)
- API documentation
- Setup and deployment guides
- ML model documentation
- Troubleshooting guide

## File Naming Conventions

### TypeScript/React
- Components: PascalCase (e.g., `Dashboard.tsx`)
- Utilities: camelCase (e.g., `dateUtils.ts`)
- Constants: UPPER_SNAKE_CASE (e.g., `API_ENDPOINTS.ts`)

### Python
- Modules: snake_case (e.g., `expense_categorizer.py`)
- Classes: PascalCase (e.g., `ExpenseCategorizer`)
- Functions: snake_case (e.g., `extract_features`)

### Documentation
- Files: UPPER_SNAKE_CASE.md (e.g., `API_DOCUMENTATION.md`)

## Environment Files

### Backend `.env`
- Server config (NODE_ENV, PORT)
- Database credentials
- JWT secrets
- Third-party API keys

### Frontend `.env`
- API endpoint URLs
- Environment type
- Feature flags

### ML Service `.env`
- Service configuration
- Model paths
- Resource limits

## Build Artifacts

Generated during build, not committed:
- `frontend/build/` - Built React app
- `backend/dist/` - Compiled TypeScript
- `ml-models/__pycache__/` - Python bytecode
- `node_modules/` - Dependencies
- `venv/` - Python virtual environment
