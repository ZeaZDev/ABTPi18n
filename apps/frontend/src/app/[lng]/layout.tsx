// ZeaZDev [Frontend Language Layout] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import { ThemeProvider } from '../../contexts/ThemeContext';
import { LanguageSelector } from '../../components/LanguageSelector';
import { Navigation } from '../../components/Navigation';

export default function LangLayout({
  children,
  params,
}: {
  children: React.ReactNode
  params: { lng: string }
}) {
  return (
    <ThemeProvider>
      <div lang={params.lng}>
        <Navigation lng={params.lng} />
        <div style={{ 
          position: 'fixed', 
          top: '20px', 
          right: '20px', 
          zIndex: 1000,
          display: 'flex',
          gap: '12px',
          alignItems: 'center'
        }}>
          <LanguageSelector />
        </div>
        <div style={{ paddingTop: '64px' }}>
          {children}
        </div>
      </div>
    </ThemeProvider>
  )
}
