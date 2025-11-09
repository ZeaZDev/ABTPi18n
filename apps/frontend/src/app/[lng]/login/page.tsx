// ZeaZDev [Frontend Login Page] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React from 'react';
import { initI18n } from '../../i18n/client';
import { useTranslation } from 'react-i18next';
import { GoogleSignIn } from '../../../components/auth/GoogleSignIn';
import { useRouter } from 'next/navigation';

export default function LoginPage({ params }: { params: { lng: string } }) {
  initI18n(params.lng);
  const { t } = useTranslation('translation');
  const router = useRouter();

  const handleSuccess = (user: any) => {
    console.log('Login successful:', user);
    // Redirect to dashboard
    router.push(`/${params.lng}/dashboard`);
  };

  const handleError = (error: string) => {
    console.error('Login error:', error);
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      backgroundColor: '#f3f4f6',
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '48px',
        borderRadius: '12px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        maxWidth: '400px',
        width: '100%',
      }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}>
            ABTPro i18n
          </h1>
          <p style={{ color: '#6b7280' }}>
            Auto Bot Trader Platform
          </p>
        </div>

        <div style={{ marginBottom: '24px' }}>
          <GoogleSignIn onSuccess={handleSuccess} onError={handleError} />
        </div>

        <div style={{ textAlign: 'center', marginTop: '24px' }}>
          <p style={{ fontSize: '14px', color: '#9ca3af' }}>
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
}
