# คู่มือการใช้งาน เฟส 3 (Phase 3) Implementation Guide

## Overview
Phase 3 focuses on internationalization (i18n) enhancements, authentication integration, and user interface improvements for the ABTPro trading platform.

### Quick Links
- [Phase 3 Summary](PHASE3_SUMMARY.md)
- [Phase 2 Summary](PHASE2_SUMMARY.md)
- [Roadmap](ROADMAP.md)

## New Features

### 1. Google OAuth Integration
Seamless authentication using Google accounts for enhanced security and user experience.

#### Features
- Single Sign-On (SSO) with Google
- Automatic user profile creation
- Secure token management
- Session persistence

#### Configuration
```env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/callback/google
```

#### Usage
1. Navigate to login page
2. Click "Sign in with Google"
3. Authorize the application
4. Automatically redirected to dashboard

### 2. Telegram Link & Notification
Real-time trading notifications and alerts via Telegram bot.

#### Features
- Link Telegram account to user profile
- Real-time trade execution alerts
- Risk management notifications
- Circuit breaker alerts
- Custom notification preferences

#### Setup
1. Create a Telegram bot via [@BotFather](https://t.me/botfather)
2. Configure bot token:
```env
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_WEBHOOK_URL=https://your-domain.com/api/telegram/webhook
```

#### Linking Account
1. Go to Settings → Notifications
2. Click "Link Telegram Account"
3. Follow the verification process
4. Configure notification preferences

#### Notification Types
- **Trade Execution**: Buy/Sell confirmations with PnL
- **Risk Alerts**: Drawdown warnings, circuit breaker trips
- **System Status**: Bot start/stop, connection issues
- **Daily Summary**: Portfolio performance summary

### 3. Dynamic Theme / Config GUI
User-friendly interface for customizing application appearance and behavior.

#### Theme Options
- **Light Mode**: Clean, modern light theme
- **Dark Mode**: Eye-friendly dark theme
- **Auto Mode**: Follows system preference
- **Custom Colors**: Customize primary, secondary, accent colors

#### Configuration Options
- **Dashboard Layout**: Grid/List view toggle
- **Chart Settings**: Candlestick/Line chart preferences
- **Refresh Interval**: Auto-refresh frequency
- **Notification Settings**: Enable/disable different alert types
- **Language Preference**: Select UI language

#### Accessing Config GUI
1. Navigate to Settings → Appearance
2. Select theme preference
3. Customize colors and layout
4. Changes apply immediately

### 4. Additional Language Support
Expanded internationalization with Chinese and Japanese language support.

#### Supported Languages
- 🇹🇭 Thai (ไทย) - Default
- 🇬🇧 English
- 🇨🇳 Chinese (简体中文) - New
- 🇯🇵 Japanese (日本語) - New

#### Language Files
Located in `apps/frontend/src/locales/`:
- `th/common.json` - Thai translations
- `en/common.json` - English translations
- `zh/common.json` - Chinese translations (新增)
- `ja/common.json` - Japanese translations (新規)

#### Switching Language
1. Click language selector in header
2. Choose preferred language
3. UI updates immediately
4. Preference saved to user profile

#### Translation Keys
All UI text uses translation keys:
```typescript
import { useTranslation } from 'react-i18next';

function Component() {
  const { t } = useTranslation();
  return <h1>{t('dashboard.title')}</h1>;
}
```

## Installation

### Prerequisites
- Phase 1 and Phase 2 completed
- Node.js 18+ and Python 3.10+
- Docker and Docker Compose

### Setup Steps

1. **Update Dependencies**
```bash
# Backend
cd apps/backend
pip install -r requirements.txt

# Frontend
cd apps/frontend
npm install
```

2. **Configure Environment Variables**
```bash
# Copy and edit .env file
cp .env.example .env
# Add OAuth and Telegram configurations
```

3. **Run Database Migrations**
```bash
cd apps/backend
npx prisma migrate dev
```

4. **Start Services**
```bash
docker-compose up -d
```

## Configuration

### OAuth Configuration
Configure Google OAuth in Google Cloud Console:
1. Create OAuth 2.0 credentials
2. Add authorized redirect URIs
3. Copy client ID and secret to `.env`

### Telegram Bot Configuration
1. Create bot with @BotFather
2. Get bot token
3. Set webhook URL for production
4. Configure notification templates

### Theme Configuration
Default theme settings in `apps/frontend/src/config/theme.ts`:
```typescript
export const defaultTheme = {
  mode: 'auto',
  primaryColor: '#3B82F6',
  secondaryColor: '#8B5CF6',
  accentColor: '#10B981',
};
```

## API Endpoints

### Authentication
```http
POST /auth/google/login
POST /auth/google/callback
GET /auth/me
POST /auth/logout
```

### Telegram
```http
POST /telegram/link
POST /telegram/unlink
GET /telegram/status
POST /telegram/notify
```

### User Preferences
```http
GET /user/preferences
PUT /user/preferences
PATCH /user/theme
PATCH /user/language
```

## Testing

### OAuth Testing
```bash
# Test Google OAuth flow
npm run test:auth

# Verify token validation
npm run test:auth:tokens
```

### Telegram Testing
```bash
# Test bot connection
python -m pytest tests/test_telegram.py

# Test notification sending
npm run test:telegram:notify
```

### i18n Testing
```bash
# Verify all translation files
npm run test:i18n

# Check for missing translations
npm run check:i18n
```

## Troubleshooting

### OAuth Issues
- **Redirect URI mismatch**: Verify URIs in Google Console match `.env`
- **Invalid credentials**: Check client ID and secret
- **Token expiration**: Implement refresh token flow

### Telegram Issues
- **Bot not responding**: Verify bot token and webhook URL
- **Messages not delivered**: Check user has started chat with bot
- **Webhook failures**: Ensure HTTPS for production webhooks

### Theme Issues
- **Changes not applying**: Clear browser cache
- **Custom colors not saving**: Check localStorage permissions
- **Dark mode flicker**: Ensure SSR theme detection

### i18n Issues
- **Missing translations**: Run `npm run check:i18n` to identify gaps
- **Fallback not working**: Check `fallbackLng` in i18n config
- **RTL languages**: Add RTL support for future languages

## Security Considerations

### OAuth Security
- Store tokens securely (httpOnly cookies)
- Implement CSRF protection
- Use state parameter for OAuth flow
- Rotate secrets regularly

### Telegram Security
- Validate webhook signatures
- Encrypt sensitive notification data
- Rate limit notification sending
- Don't send API keys via Telegram

## Performance Optimization

### Theme Performance
- Use CSS variables for dynamic theming
- Implement theme lazy loading
- Cache theme preferences
- Minimize theme bundle size

### i18n Performance
- Lazy load language files
- Cache translations in memory
- Use namespace splitting
- Implement loading states

## Next Steps (Phase 4)
According to the roadmap, Phase 4 includes:
- PromptPay Top-up Flow (QR / Callback)
- Rental Contract Expiry Enforcement
- Module Plugin Loader (Entry Point)
- Portfolio Aggregation / Multi-Account
- Backtester / Paper Trading Mode

## Support

For issues or questions:
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Review [SECURITY.md](SECURITY.md) for security policies
- Open an issue on GitHub for bugs or feature requests
