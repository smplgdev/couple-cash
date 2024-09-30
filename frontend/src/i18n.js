import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import ruResources from "./lang/ru.json";
import enResources from "./lang/en.json";

const resources = {
  en: {
    translation: enResources,
  },
  ru: {
    translation: ruResources,
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: "en",
    debug: true,
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;