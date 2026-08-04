import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            nav: {
                tagline: "Osun 2026 Fact Check",
                debunks: "Live Fact-Checks",
                report: "Report Incident",
                situationRoom: "Situation Room"
            }
        }
    },
    yo: {
        translation: {
            nav: {
                tagline: "Ayẹwo Otitọ Osun 2026",
                debunks: "Awọn Otitọ TI a Amọ",
                report: "Sọ Nipa Isẹlẹ",
                situationRoom: "Yara Ipo (Situation Room)"
            }
        }
    },
    pcm: {
        translation: {
            nav: {
                tagline: "Osun 2026 Fact Check",
                debunks: "Live Fact-Checks",
                report: "Report Wetin Happen",
                situationRoom: "Situation Room"
            }
        }
    }
};

i18n.use(initReactI18next).init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: { escapeValue: false }
});

export default i18n;