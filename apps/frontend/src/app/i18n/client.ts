// ZeaZDev [Frontend i18n Configuration] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Omega Scaffolding) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //
"use client";

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import enTranslation from '../../../public/locales/en/translation.json';
import thTranslation from '../../../public/locales/th/translation.json';

let initialized = false;

export function initI18n(locale: string) {
  if (!initialized) {
    i18n
      .use(LanguageDetector)
      .use(initReactI18next)
      .init({
        lng: locale,
        fallbackLng: 'en',
        supportedLngs: ['en', 'th'],
        defaultNS: 'translation',
        ns: ['translation'],
        detection: {
          order: ['path', 'querystring', 'navigator'],
          caches: []
        },
        resources: {
          en: {
            translation: enTranslation
          },
          th: {
            translation: thTranslation
          }
        }
      });
    initialized = true;
  } else {
    i18n.changeLanguage(locale);
  }
  return i18n;
}

export { i18n };