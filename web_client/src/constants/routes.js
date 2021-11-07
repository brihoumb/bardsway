import LandingPage from "../pages/LandingPage";
import RegisterPage from "../pages/RegisterPage";
import LoginPage from "../pages/LoginPage";
import LogoutPage from "../pages/LogoutPage";
import LicensePage from "../pages/LicensePage";
import TermsPage from "../pages/TermsPage";

const ROUTES = {
  LANDING: {
    path: "/",
    component: LandingPage,
  },
  REGISTER: {
    path: "/register",
    component: RegisterPage,
  },
  LOGIN: {
    path: "/login",
    component: LoginPage,
  },
  LOGOUT: {
    path: "/logout",
    component: LogoutPage,
  },
  LICENSE: {
    path: "/license",
    component: LicensePage,
  },
  TERMS: {
    path: "/terms",
    component: TermsPage,
  },
};

export default ROUTES;
