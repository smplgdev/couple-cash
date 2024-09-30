import { createBrowserRouter } from "react-router-dom"

/* 
    COMPONENTS IMPORTS
*/
import Home from "./home/Main"


/* 
    ROUTES
*/
const routes = Object.freeze({
    home: "/",
    test: "/test",
})

export { routes }

/* 
    ROUTER
*/
const router = createBrowserRouter([
    {
        path: routes.home,
        element: <Home />,
    },
])

export default router