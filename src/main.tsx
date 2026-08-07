import React from 'react';
import ReactDOM from 'react-dom/client';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import App from './App';
import './index.css';

// Configure i18n directly inside main.tsx
i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          nav: {
            tagline: 'Osun 2026 Fact Check',
            debunks: 'Live Fact-Checks',
            report: 'Report Incident',
            situationRoom: 'Situation Room'
          },
          home: {
            heroTitle: 'Live Election Fact-Checks',
            heroSubtitle: 'Real-time verified claims, debunked rumors, and official statements for Osun 2026.',
            searchPlaceholder: 'Search verified claims, candidates, or rumors...',
            filterAll: 'All Debunks',
            filterElectionDay: 'Election Day',
            filterCandidates: 'Candidates',
            filterINEC: 'INEC / Voting',
            filterSecurity: 'Security',
            readFull: 'Read Full Analysis',
            shareReport: 'Share Fact-Check',
            statusFalse: 'FALSE',
            statusMisleading: 'MISLEADING',
            statusVerified: 'VERIFIED TRUE'
          }
        }
      },
      yo: {
        translation: {
          nav: {
            tagline: 'Osun 2026 Fact Check',
            debunks: 'Àwọn Fact-Check',
            report: 'Sọ̀jásí Ìṣẹ̀lẹ̀',
            situationRoom: 'Agbègbè Situation Room'
          },
          home: {
            heroTitle: 'Àwọn Fact-Check Ìbo Tí Ọ́ Ń Lọ',
            heroSubtitle: 'Àwọn ìròyìn tí a ti fìdí rẹ̀ múlẹ̀ fún ìbo Osun 2026.',
            searchPlaceholder: 'Ṣàwárí àwọn ìròyìn, àwọn olùdíje, tàbí ìró...',
            filterAll: 'Gbogbo Fact-Check',
            filterElectionDay: 'Ọjọ́ Ìbo',
            filterCandidates: 'Àwọn Olùdíje',
            filterINEC: 'INEC / Ìbo',
            filterSecurity: 'Ààbò',
            readFull: 'Kà Á Kíkún',
            shareReport: 'Pín Fact-Check Yìí',
            statusFalse: 'EKE NI',
            statusMisleading: 'Ó Ń SI NI LỌ̀NA',
            statusVerified: 'LÓÒTỌ́ NI'
          }
        }
      },
      pcm: {
        translation: {
          nav: {
            tagline: 'Osun 2026 Fact Check',
            debunks: 'Check Am',
            report: 'Report Mata',
            situationRoom: 'Situation Room'
          },
          home: {
            heroTitle: 'Live Election Fact-Checks',
            heroSubtitle: 'Real-time news check, fake story debunk, and official info for Osun 2026.',
            searchPlaceholder: 'Search news, candidate name, or fake story...',
            filterAll: 'All Check-Am',
            filterElectionDay: 'Voting Day',
            filterCandidates: 'Candidates',
            filterINEC: 'INEC / Voting',
            filterSecurity: 'Security Mata',
            readFull: 'Read Full Story',
            shareReport: 'Share This Check',
            statusFalse: 'TOTAL LIE',
            statusMisleading: 'WAYO STORY',
            statusVerified: 'CONFIRM TRUE'
          }
        }
      }
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);