import axios from "axios";

import { SERVER_ROUTES } from "../constants/external";
import { ServerOffline } from "../constants/errors";

export const pay = async (accessToken, paymentMethod) => {
  try {
    const res = await axios.post(SERVER_ROUTES.PAY, {
      accessToken,
      paymentMethod,
    });
    console.log(res);
    return res.status === 200
      ? { licenseKey: res.data.licenseKey }
      : { error: { type: res.data.errorType, msg: "Unknown error" } };
  } catch (e) {
    if (!e.response) return { error: ServerOffline };
    const { data } = e.response;
    console.log(data);
    return {
      error: {
        type: data.errorType,
        msg: data.emailVerified
          ? "User not logged in"
          : "You must verify your email address before purchasing a license !",
      },
    };
  }
};

export const getLicense = async (accessToken) => {
  try {
    const res = await axios.post(SERVER_ROUTES.LICENSE, { accessToken });
    return res.status === 200
      ? { licenseKey: res.data.licenseKey }
      : { error: { type: res.data.errorType, msg: "Unknown error" } };
  } catch (e) {
    if (!e.response) return { error: ServerOffline };
    const { data } = e.response;
    return {
      error: {
        type: data.errorType,
        msg: data.emailVerified
          ? "User not logged in"
          : "You must verify your email address before purchasing a license !",
      },
    };
  }
};

export const getProduct = async () => {
  try {
    const res = await axios.get(SERVER_ROUTES.PRODUCT);
    return res.status === 200
      ? { price: res.data.price }
      : { error: { type: res.data.errorType, msg: "Unknown error" } };
  } catch (e) {
    if (!e.response) return { error: ServerOffline };
    const { data } = e.response;
    return {
      error: {
        type: data.errorType,
        msg: "Can't get the license price.",
      },
    };
  }
};
