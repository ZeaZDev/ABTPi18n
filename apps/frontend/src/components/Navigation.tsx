// ZeaZDev [Frontend Navigation Menu] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Menu Enhancement) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavigationProps {
  lng: string;
}

// Translation mappings for menu items
const menuTranslations: Record<string, { dashboard: string; settings: string }> = {
  en: { dashboard: 'Dashboard', settings: 'Settings' },
  th: { dashboard: 'แดชบอร์ด', settings: 'ตั้งค่า' },
  zh: { dashboard: '仪表板', settings: '设置' },
  ja: { dashboard: 'ダッシュボード', settings: '設定' },
};

export function Navigation({ lng }: NavigationProps) {
  const pathname = usePathname();
  const labels = menuTranslations[lng] || menuTranslations.en;

  const menuItems = [
    { key: 'dashboard', href: `/${lng}/dashboard`, label: labels.dashboard },
    { key: 'settings', href: `/${lng}/settings`, label: labels.settings },
  ];

  const isActive = (href: string) => {
    return pathname === href;
  };

  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      backgroundColor: '#ffffff',
      borderBottom: '1px solid #e5e7eb',
      zIndex: 999,
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '0 20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '64px',
      }}>
        {/* Logo/Brand */}
        <div style={{
          fontSize: '20px',
          fontWeight: '700',
          color: '#1f2937',
        }}>
          ABTPro
        </div>

        {/* Menu Items */}
        <div style={{
          display: 'flex',
          gap: '8px',
          alignItems: 'center',
        }}>
          {menuItems.map((item) => (
            <Link
              key={item.key}
              href={item.href}
              style={{
                padding: '8px 16px',
                borderRadius: '6px',
                textDecoration: 'none',
                color: isActive(item.href) ? '#3B82F6' : '#4b5563',
                backgroundColor: isActive(item.href) ? '#eff6ff' : 'transparent',
                fontWeight: isActive(item.href) ? '600' : '500',
                transition: 'all 0.2s',
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
