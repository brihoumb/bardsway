export const BACK_URL = process.env.REACT_APP_BACK_URL || "http://localhost:8080";

export const SERVER_ROUTES = {
  LOGIN: `${BACK_URL}/login`,
  REGISTER: `${BACK_URL}/signup`,
  SIGNOUT: `${BACK_URL}/signout`,
  PAY: `${BACK_URL}/pay`,
  USER: `${BACK_URL}/user`,
  POSTSIGNUP: `${BACK_URL}/postSignup`,
  LICENSE: `${BACK_URL}/license`,
  PRODUCT: `${BACK_URL}/product`,
};
