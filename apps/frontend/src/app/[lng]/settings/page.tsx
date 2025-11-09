// ZeaZDev [Frontend Screen Settings API Keys] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React, { useState } from 'react';
import { initI18n } from '../../i18n/client';
import { useTranslation } from 'react-i18next';
import { ThemeCustomizer } from '../../../components/settings/ThemeCustomizer';
import { TelegramLink } from '../../../components/settings/TelegramLink';
import { NotificationPreferences } from '../../../components/settings/NotificationPreferences';

export default function SettingsPage({ params }: { params: { lng: string } }) {
  initI18n(params.lng);
  const { t } = useTranslation('translation');
  const [exchange, setExchange] = useState('binance');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  // TODO: Replace with actual user ID from authentication
  const userId = 1;

  const save = () => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/exchange/keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exchange, api_key: apiKey, api_secret: apiSecret })
    })
      .then(r => r.json())
      .then(d => setStatus('OK'))
      .catch(e => setStatus(e.message));
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem' }}>{t('settings.title')}</h1>

      {/* API Keys Section */}
      <div style={{ marginBottom: '2rem', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2 style={{ marginBottom: '1rem' }}>Exchange API Keys</h2>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>{t('settings.exchange')}</label>
          <select 
            value={exchange} 
            onChange={e => setExchange(e.target.value)}
            style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="binance">Binance</option>
            <option value="bybit">Bybit</option>
          </select>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>{t('settings.api_key')}</label>
          <input 
            value={apiKey} 
            onChange={e => setApiKey(e.target.value)} 
            type="password"
            style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #ddd' }}
          />
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>{t('settings.api_secret')}</label>
          <input 
            value={apiSecret} 
            onChange={e => setApiSecret(e.target.value)} 
            type="password"
            style={{ width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #ddd' }}
          />
        </div>
        <button 
          onClick={save}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#3B82F6', 
            color: 'white', 
            border: 'none', 
            borderRadius: '6px',
            cursor: 'pointer'
          }}
        >
          {t('settings.submit')}
        </button>
        {status && <div style={{ marginTop: '1rem' }}>Status: {status}</div>}
      </div>

      {/* Theme Customizer */}
      <div style={{ marginBottom: '2rem' }}>
        <ThemeCustomizer />
      </div>

      {/* Telegram Integration */}
      <div style={{ marginBottom: '2rem' }}>
        <TelegramLink userId={userId} />
      </div>

      {/* Notification Preferences */}
      <div style={{ marginBottom: '2rem' }}>
        <NotificationPreferences userId={userId} />
      </div>
    </div>
  );
}