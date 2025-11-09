// ZeaZDev [Notification Preferences Component] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface NotificationPreferencesProps {
  userId: number;
}

interface Preferences {
  tradeAlerts: boolean;
  riskAlerts: boolean;
  systemAlerts: boolean;
  dailySummary: boolean;
}

export function NotificationPreferences({ userId }: NotificationPreferencesProps) {
  const { t } = useTranslation();
  const [preferences, setPreferences] = useState<Preferences>({
    tradeAlerts: true,
    riskAlerts: true,
    systemAlerts: true,
    dailySummary: true,
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

  useEffect(() => {
    loadPreferences();
  }, [userId]);

  const loadPreferences = async () => {
    try {
      const response = await fetch(`${backendUrl}/user/notifications/preferences/${userId}`);
      const data = await response.json();
      setPreferences(data);
    } catch (error) {
      console.error('Failed to load notification preferences:', error);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${backendUrl}/user/notifications/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          trade_alerts: preferences.tradeAlerts,
          risk_alerts: preferences.riskAlerts,
          system_alerts: preferences.systemAlerts,
          daily_summary: preferences.dailySummary,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Notification preferences saved successfully!');
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage(data.detail || 'Failed to save preferences');
      }
    } catch (error) {
      setMessage('Error saving preferences');
      console.error('Save error:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePreference = (key: keyof Preferences) => {
    setPreferences((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3 style={{ marginBottom: '16px' }}>{t('notifications.title')}</h3>

      <div style={{ marginBottom: '20px' }}>
        <label
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '12px',
            marginBottom: '8px',
            backgroundColor: '#f9fafb',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          <input
            type="checkbox"
            checked={preferences.tradeAlerts}
            onChange={() => togglePreference('tradeAlerts')}
            style={{ marginRight: '12px', width: '18px', height: '18px' }}
          />
          <div>
            <div style={{ fontWeight: '500' }}>{t('notifications.trade_alerts')}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              Get notified when trades are executed
            </div>
          </div>
        </label>

        <label
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '12px',
            marginBottom: '8px',
            backgroundColor: '#f9fafb',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          <input
            type="checkbox"
            checked={preferences.riskAlerts}
            onChange={() => togglePreference('riskAlerts')}
            style={{ marginRight: '12px', width: '18px', height: '18px' }}
          />
          <div>
            <div style={{ fontWeight: '500' }}>{t('notifications.risk_alerts')}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              Get alerted when risk thresholds are exceeded
            </div>
          </div>
        </label>

        <label
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '12px',
            marginBottom: '8px',
            backgroundColor: '#f9fafb',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          <input
            type="checkbox"
            checked={preferences.systemAlerts}
            onChange={() => togglePreference('systemAlerts')}
            style={{ marginRight: '12px', width: '18px', height: '18px' }}
          />
          <div>
            <div style={{ fontWeight: '500' }}>{t('notifications.system_alerts')}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              Receive system status and important updates
            </div>
          </div>
        </label>

        <label
          style={{
            display: 'flex',
            alignItems: 'center',
            padding: '12px',
            marginBottom: '8px',
            backgroundColor: '#f9fafb',
            borderRadius: '6px',
            cursor: 'pointer',
          }}
        >
          <input
            type="checkbox"
            checked={preferences.dailySummary}
            onChange={() => togglePreference('dailySummary')}
            style={{ marginRight: '12px', width: '18px', height: '18px' }}
          />
          <div>
            <div style={{ fontWeight: '500' }}>{t('notifications.daily_summary')}</div>
            <div style={{ fontSize: '14px', color: '#6b7280' }}>
              Get daily performance summaries
            </div>
          </div>
        </label>
      </div>

      <button
        onClick={handleSave}
        disabled={loading}
        style={{
          padding: '12px 24px',
          backgroundColor: '#3B82F6',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: loading ? 'not-allowed' : 'pointer',
          fontWeight: '500',
          opacity: loading ? 0.6 : 1,
        }}
      >
        {loading ? 'Saving...' : 'Save Preferences'}
      </button>

      {message && (
        <div
          style={{
            marginTop: '16px',
            padding: '12px',
            backgroundColor: message.includes('success') ? '#d4edda' : '#f8d7da',
            color: message.includes('success') ? '#155724' : '#721c24',
            borderRadius: '6px',
          }}
        >
          {message}
        </div>
      )}
    </div>
  );
}
