import './assets/css/index.css'
import { useTranslation } from 'react-i18next';

function App() {
  const { t, i18n } = useTranslation();

  i18n.changeLanguage("ru");

  console.log(t("Hello world"));

  return (
    <div className="text-red-500">
      {t("Hello world")}
    </div>
  );
}

export default App;
