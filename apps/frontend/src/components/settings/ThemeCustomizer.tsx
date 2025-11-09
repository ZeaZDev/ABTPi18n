// ZeaZDev [Theme Customizer Component] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../../contexts/ThemeContext';

export function ThemeCustomizer() {
  const { t } = useTranslation();
  const {
    theme,
    setTheme,
    primaryColor,
    secondaryColor,
    accentColor,
    setPrimaryColor,
    setSecondaryColor,
    setAccentColor,
  } = useTheme();

  const [tempPrimaryColor, setTempPrimaryColor] = useState(primaryColor);
  const [tempSecondaryColor, setTempSecondaryColor] = useState(secondaryColor);
  const [tempAccentColor, setTempAccentColor] = useState(accentColor);

  const handleApplyColors = () => {
    setPrimaryColor(tempPrimaryColor || '#3B82F6');
    setSecondaryColor(tempSecondaryColor || '#8B5CF6');
    setAccentColor(tempAccentColor || '#10B981');
  };

  const handleResetColors = () => {
    const defaultPrimary = '#3B82F6';
    const defaultSecondary = '#8B5CF6';
    const defaultAccent = '#10B981';
    
    setTempPrimaryColor(defaultPrimary);
    setTempSecondaryColor(defaultSecondary);
    setTempAccentColor(defaultAccent);
    setPrimaryColor(defaultPrimary);
    setSecondaryColor(defaultSecondary);
    setAccentColor(defaultAccent);
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3 style={{ marginBottom: '16px' }}>{t('theme.customize')}</h3>

      {/* Theme Mode Selection */}
      <div style={{ marginBottom: '24px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Theme Mode
        </label>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => setTheme('light')}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: theme === 'light' ? '#3B82F6' : '#f3f4f6',
              color: theme === 'light' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: theme === 'light' ? '600' : '400',
            }}
          >
            ☀️ {t('theme.light')}
          </button>
          <button
            onClick={() => setTheme('dark')}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: theme === 'dark' ? '#3B82F6' : '#f3f4f6',
              color: theme === 'dark' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: theme === 'dark' ? '600' : '400',
            }}
          >
            🌙 {t('theme.dark')}
          </button>
          <button
            onClick={() => setTheme('auto')}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: theme === 'auto' ? '#3B82F6' : '#f3f4f6',
              color: theme === 'auto' ? 'white' : '#374151',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: theme === 'auto' ? '600' : '400',
            }}
          >
            🔄 {t('theme.auto')}
          </button>
        </div>
      </div>

      {/* Color Customization */}
      <div style={{ marginBottom: '24px' }}>
        <h4 style={{ marginBottom: '12px' }}>Custom Colors</h4>

        <div style={{ marginBottom: '12px' }}>
          <label style={{ display: 'block', marginBottom: '4px' }}>
            Primary Color
          </label>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <input
              type="color"
              value={tempPrimaryColor}
              onChange={(e) => setTempPrimaryColor(e.target.value)}
              style={{ width: '60px', height: '40px', border: 'none', borderRadius: '6px' }}
            />
            <input
              type="text"
              value={tempPrimaryColor}
              onChange={(e) => setTempPrimaryColor(e.target.value)}
              style={{
                flex: 1,
                padding: '8px',
                border: '1px solid #ddd',
                borderRadius: '6px',
              }}
            />
          </div>
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label style={{ display: 'block', marginBottom: '4px' }}>
            Secondary Color
          </label>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <input
              type="color"
              value={tempSecondaryColor}
              onChange={(e) => setTempSecondaryColor(e.target.value)}
              style={{ width: '60px', height: '40px', border: 'none', borderRadius: '6px' }}
            />
            <input
              type="text"
              value={tempSecondaryColor}
              onChange={(e) => setTempSecondaryColor(e.target.value)}
              style={{
                flex: 1,
                padding: '8px',
                border: '1px solid #ddd',
                borderRadius: '6px',
              }}
            />
          </div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '4px' }}>
            Accent Color
          </label>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <input
              type="color"
              value={tempAccentColor}
              onChange={(e) => setTempAccentColor(e.target.value)}
              style={{ width: '60px', height: '40px', border: 'none', borderRadius: '6px' }}
            />
            <input
              type="text"
              value={tempAccentColor}
              onChange={(e) => setTempAccentColor(e.target.value)}
              style={{
                flex: 1,
                padding: '8px',
                border: '1px solid #ddd',
                borderRadius: '6px',
              }}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={handleApplyColors}
            style={{
              flex: 1,
              padding: '10px 20px',
              backgroundColor: primaryColor,
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '500',
            }}
          >
            Apply Colors
          </button>
          <button
            onClick={handleResetColors}
            style={{
              padding: '10px 20px',
              backgroundColor: '#6b7280',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
            }}
          >
            Reset
          </button>
        </div>
      </div>

      {/* Preview */}
      <div
        style={{
          padding: '16px',
          backgroundColor: '#f9fafb',
          borderRadius: '8px',
          border: '1px solid #e5e7eb',
        }}
      >
        <h4 style={{ marginBottom: '12px' }}>Preview</h4>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <div
            style={{
              width: '80px',
              height: '80px',
              backgroundColor: tempPrimaryColor,
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '12px',
              fontWeight: '500',
            }}
          >
            Primary
          </div>
          <div
            style={{
              width: '80px',
              height: '80px',
              backgroundColor: tempSecondaryColor,
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '12px',
              fontWeight: '500',
            }}
          >
            Secondary
          </div>
          <div
            style={{
              width: '80px',
              height: '80px',
              backgroundColor: tempAccentColor,
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '12px',
              fontWeight: '500',
            }}
          >
            Accent
          </div>
        </div>
      </div>
    </div>
  );
}
