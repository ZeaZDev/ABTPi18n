// ZeaZDev [Telegram Link Component] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface TelegramLinkProps {
  userId: number;
}

interface TelegramStatus {
  linked: boolean;
  chatId?: string;
  username?: string;
  verified?: boolean;
}

export function TelegramLink({ userId }: TelegramLinkProps) {
  const { t } = useTranslation();
  const [status, setStatus] = useState<TelegramStatus>({ linked: false });
  const [loading, setLoading] = useState(false);
  const [chatId, setChatId] = useState('');
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');

  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

  // Load Telegram link status
  useEffect(() => {
    loadStatus();
  }, [userId]);

  const loadStatus = async () => {
    try {
      const response = await fetch(`${backendUrl}/telegram/status/${userId}`);
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Failed to load Telegram status:', error);
    }
  };

  const handleLink = async () => {
    if (!chatId.trim()) {
      setMessage('Please enter your Telegram Chat ID');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${backendUrl}/telegram/link`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          chat_id: chatId.trim(),
          username: username.trim() || null,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Telegram account linked successfully!');
        setChatId('');
        setUsername('');
        await loadStatus();
      } else {
        setMessage(data.detail || 'Failed to link Telegram account');
      }
    } catch (error) {
      setMessage('Error linking Telegram account');
      console.error('Link error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUnlink = async () => {
    if (!confirm('Are you sure you want to unlink your Telegram account?')) {
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${backendUrl}/telegram/unlink`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Telegram account unlinked successfully');
        await loadStatus();
      } else {
        setMessage(data.detail || 'Failed to unlink Telegram account');
      }
    } catch (error) {
      setMessage('Error unlinking Telegram account');
      console.error('Unlink error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTestNotification = async () => {
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch(`${backendUrl}/telegram/notify/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Test notification sent! Check your Telegram.');
      } else {
        setMessage(data.detail || 'Failed to send notification');
      }
    } catch (error) {
      setMessage('Error sending notification');
      console.error('Notification error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3 style={{ marginBottom: '16px' }}>Telegram Integration</h3>

      {status.linked ? (
        <div>
          <div style={{ marginBottom: '16px' }}>
            <p><strong>Status:</strong> {t('telegram.linked')}</p>
            {status.username && <p><strong>Username:</strong> @{status.username}</p>}
            <p><strong>Chat ID:</strong> {status.chatId}</p>
          </div>

          <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
            <button
              onClick={handleTestNotification}
              disabled={loading}
              style={{
                padding: '10px 20px',
                backgroundColor: '#0088cc',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {t('telegram.test_notification')}
            </button>

            <button
              onClick={handleUnlink}
              disabled={loading}
              style={{
                padding: '10px 20px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {t('telegram.unlink')}
            </button>
          </div>
        </div>
      ) : (
        <div>
          <p style={{ marginBottom: '16px', color: '#666' }}>
            {t('telegram.not_linked')}
          </p>

          <div style={{ marginBottom: '12px' }}>
            <label style={{ display: 'block', marginBottom: '4px' }}>
              Telegram Chat ID *
            </label>
            <input
              type="text"
              value={chatId}
              onChange={(e) => setChatId(e.target.value)}
              placeholder="Enter your Chat ID"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '6px',
              }}
            />
            <small style={{ color: '#666' }}>
              Get your Chat ID by messaging <a href="https://t.me/userinfobot" target="_blank">@userinfobot</a>
            </small>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '4px' }}>
              Telegram Username (optional)
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="@yourusername"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '6px',
              }}
            />
          </div>

          <button
            onClick={handleLink}
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: '#0088cc',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Linking...' : t('telegram.link')}
          </button>
        </div>
      )}

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
