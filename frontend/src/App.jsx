import './assets/css/index.css'
import { useTranslation } from 'react-i18next'
import { RouterProvider } from "react-router-dom"
import WebApp from '@twa-dev/sdk'
import router from './router'

function App() {
  const { i18n } = useTranslation()

  WebApp.showAlert('Hey there!')

  i18n.changeLanguage("ru")

  console.log(t("Hello world"))

  return <RouterProvider router={router} />
}

export default App
