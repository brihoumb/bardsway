import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import firebase from "firebase/app";
import "firebase/auth";
import "firebase/firestore";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { ToastProvider } from "react-toast-notifications";

import firebaseConfig from "./constants/firebaseConfig";
import Store from "./store/Store";
import "./index.css";
import App from "./App";

firebase.initializeApp(firebaseConfig);

const stripePromise = loadStripe(
  "pk_test_51HjC2FLWDqabJ2rnpD2nfbGZ1MnmQKZvCabjfWAT1g3l2ibCibHrFlFjO13BRMOOhGZfTU2FL6luBGAj70lXOKfI00Lzrl6ZKx"
);

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <Elements stripe={stripePromise}>
        <ToastProvider autoDismiss={true}>
          <Store>
            <App />
          </Store>
        </ToastProvider>
      </Elements>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById("root")
);
