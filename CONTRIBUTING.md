# CONTRIBUTING GUIDE

## Development Setup

### Prerequisites
- Docker 24+
- Docker Compose
- Node.js 18+
- pnpm 8+
- Python 3.10+
- Git 2.40+

### Quick Start
```bash
# Clone and setup
git clone https://github.com/CVSz/ABTPi18n.git
cd ABTPi18n

# Automated setup
./install.sh

# Or manual setup
cp .env.example .env
# Edit .env and replace ENCRYPTION_KEY with: openssl rand -base64 32
pnpm install
docker compose up -d --build
```

### Verification
```bash
./verify.sh
```

## Project Structure

```
ABTPi18n/
├── apps/
│   ├── backend/          # FastAPI + Celery + Prisma
│   │   ├── src/
│   │   │   ├── api/      # API endpoints
│   │   │   ├── security/ # AES-GCM encryption
│   │   │   ├── services/ # Exchange connectors
│   │   │   ├── trading/  # Strategy engine
│   │   │   └── worker/   # Celery tasks
│   │   ├── prisma/       # Database schema
│   │   ├── main.py       # FastAPI entry
│   │   └── worker.py     # Worker entry
│   └── frontend/         # Next.js + react-i18next
│       ├── src/app/      # App router pages
│       └── public/locales/ # Translation files
├── docker-compose.yml    # Infrastructure
└── install.sh           # Setup script
```

## Development Workflow

### Adding a New Strategy

1. Create file in `apps/backend/src/trading/strategies/your_strategy.py`:
```python
"""// ZeaZDev [Backend Strategy Your Name] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: YourName //
// --- DO NOT EDIT HEADER --- //"""
from src.trading.strategy_interface import Strategy, StrategyRegistry

class YourStrategy(Strategy):
    name = "YOUR_STRATEGY"
    
    def execute(self, ticker_data, context):
        # Your logic here
        return {"signal": "HOLD", "confidence": 0.5}

StrategyRegistry.register(YourStrategy)
```

2. Strategy will auto-register on import

### Adding Translations

Edit `apps/frontend/public/locales/{lang}/translation.json`:
```json
{
  "your.key": "Your translation"
}
```

Usage in components:
```tsx
const { t } = useTranslation();
return <div>{t('your.key')}</div>;
```

### Database Changes

```bash
# Modify apps/backend/prisma/schema.prisma
# Generate migration
pnpm prisma migrate dev --name your_migration

# Generate client
pnpm prisma generate
```

### Running Tests

```bash
# Backend tests (when added)
cd apps/backend
python -m pytest

# Frontend tests (when added)
cd apps/frontend
pnpm test
```

## Code Standards

### Python
- Follow PEP 8
- Use type hints
- Include docstrings for public functions
- Required header on all .py files

### TypeScript
- Use TypeScript strict mode
- Prefer functional components
- Use proper typing
- Required header on all .ts/.tsx files

### Required File Header
All source files (except JSON) must include:
```
// ZeaZDev [File Type] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: [Your Name or ZeaZDev Meta-Intelligence] //
// --- DO NOT EDIT HEADER --- //
```

## Security Guidelines

1. **Never** commit secrets or API keys
2. Always encrypt sensitive data using crypto_service
3. Use environment variables for configuration
4. Review SECURITY.md before making changes
5. Run security scans before PR

## Pull Request Process

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with proper headers
3. Test locally: `./verify.sh`
4. Commit with clear message
5. Push and create PR
6. Wait for CI checks and review

## Common Issues

### Prisma Client Not Found
```bash
pnpm prisma generate
```

### Docker Build Fails
```bash
docker compose down -v
docker compose up -d --build
```

### Port Already in Use
Edit docker-compose.yml to change ports

## Getting Help

- Check STRATEGY_GUIDE.md for strategy development
- Check ROADMAP.md for planned features
- Open an issue for bugs
- Check existing issues for common problems

## License

See LICENSE file for details.
