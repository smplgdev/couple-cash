import './assets/css/index.css'
import { useTranslation } from 'react-i18next'
import WebApp from '@twa-dev/sdk'

function App() {
  const { t, i18n } = useTranslation()

  WebApp.showAlert('Hey there!')

  i18n.changeLanguage("ru")

  console.log(t("Hello world"))

  return (
    <div className="text-red-500">
      {t("Hello world")}
    </div>
  );
}

export default App;
