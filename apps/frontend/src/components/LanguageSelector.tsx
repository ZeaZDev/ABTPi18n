// ZeaZDev [Language Selector Component] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import React from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useTranslation } from 'react-i18next';

const languages = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'th', name: 'ไทย', flag: '🇹🇭' },
  { code: 'zh', name: '简体中文', flag: '🇨🇳' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
];

export function LanguageSelector() {
  const router = useRouter();
  const pathname = usePathname();
  const { i18n } = useTranslation();

  const currentLang = i18n.language || 'en';

  const handleLanguageChange = (langCode: string) => {
    // Extract the current path without language prefix
    const pathParts = pathname.split('/');
    const isLangPath = languages.some(lang => lang.code === pathParts[1]);
    
    let newPath;
    if (isLangPath) {
      pathParts[1] = langCode;
      newPath = pathParts.join('/');
    } else {
      newPath = `/${langCode}${pathname}`;
    }

    // Navigate to the new path
    router.push(newPath);
  };

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <select
        value={currentLang}
        onChange={(e) => handleLanguageChange(e.target.value)}
        style={{
          padding: '8px 32px 8px 12px',
          fontSize: '14px',
          border: '1px solid #ddd',
          borderRadius: '6px',
          backgroundColor: 'white',
          cursor: 'pointer',
          appearance: 'none',
          backgroundImage: `url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e")`,
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'right 8px center',
          backgroundSize: '16px',
        }}
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
}
