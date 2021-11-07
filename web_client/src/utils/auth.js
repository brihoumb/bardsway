import axios from "axios";
import firebase from "firebase";

import { backToFrontMsg } from "../utils/errors";
import { ServerOffline } from "../constants/errors";
import { SERVER_ROUTES } from "../constants/external";

export const checkEmail = (value) => /[A-Z\d._%+-]+@[A-Z\d.-]+\.[A-Z]{2,6}/gi.test(value);

export const checkPassword = (value) =>
  /(?=(.*[0-9]))(?=.*[!@#$%^&*()\\[\]{}\-_+=~`|:;"'<>,./?])(?=.*[a-z])(?=(.*[A-Z]))(?=(.*)).{8,}/.test(value);

// export const login = async ({ email, password }) => {
//   try {
//     const res = await axios.post(SERVER_ROUTES.LOGIN, {
//       email,
//       password,
//     });
//     const { user, error, errorType } = res.data;
//     return user ? { user } : { error: { type: errorType, msg: error } };
//   } catch (e) {
//     if (!e.response) return { error: ServerOffline };
//     const { data } = e.response;
//     return { user: null, error: { type: data.errorType, msg: backToFrontMsg(data.error) } };
//   }
// };

// export const register = async ({ email, password }) => {
//   try {
//     const res = await axios.post(SERVER_ROUTES.REGISTER, {
//       email,
//       password: password,
//     });
//     const { user, error, errorType } = res.data;
//     return user ? { user } : { error: { type: errorType, msg: error } };
//   } catch (e) {
//     if (!e.response) return { error: ServerOffline };
//     const { data } = e.response;
//     return { user: null, error: { type: data.errorType, msg: backToFrontMsg(data.error) } };
//   }
// };

// export const user = async () => {
//   try {
//     const res = await axios.get(SERVER_ROUTES.USER);
//     const { user } = res.data;
//     console.log(user);
//     return { user };
//   } catch (e) {
//     if (!e.response) return { error: ServerOffline };
//     const { data } = e.response;
//     return { user: null, error: { type: data.errorType, msg: "Not logged in" } };
//   }
// };

// export const signOut = async () => {
//   try {
//     const res = await axios.get(SERVER_ROUTES.SIGNOUT);
//     const { user, error } = res.data;
//     return { user, error };
//   } catch (e) {
//     if (!e.response) return { error: ServerOffline };
//     const { data } = e.response;
//     return { user: null, error: { type: data.errorType, msg: "Not logged in" } };
//   }
// };

export const register = async ({ email, password }) => {
  try {
    const userHandle = await firebase.auth().createUserWithEmailAndPassword(email, password);
    const { user } = JSON.parse(JSON.stringify(userHandle));

    console.log("register");
    console.log(user);
    const { accessToken } = user.stsTokenManager;
    const res = await axios.post(SERVER_ROUTES.POSTSIGNUP, {
      accessToken,
    });
    if (res.status !== 200) return { user: null, error: ServerOffline };
    await userHandle.user.sendEmailVerification();
    return { user };
  } catch (e) {
    return { user: null, error: { type: e.code, msg: backToFrontMsg(e.message) } };
  }
};

export const login = async ({ email, password }) => {
  console.log("login");
  try {
    const { user } = JSON.parse(
      JSON.stringify(await firebase.auth().signInWithEmailAndPassword(email, password))
    );

    console.log(user);
    return { user };
  } catch (e) {
    return { user: null, error: { type: e.code, msg: backToFrontMsg(e.message) } };
  }
};

export const signOut = async () => {
  try {
    await firebase.auth().signOut();
    return { user: null, error: null };
  } catch (e) {
    return { error: { type: e.code, msg: backToFrontMsg(e.message) } };
  }
};
