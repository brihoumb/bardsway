import React, { useContext, useEffect } from "react";
import { Route, Switch } from "react-router-dom";
import firebase from "firebase";

import { Context } from "./store/Store";
import { types } from "./store/Reducer";
import routes from "./constants/routes";
import { getLicense } from "./utils/license";

const App = () => {
  const [, dispatch] = useContext(Context);

  useEffect(() => {
    const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
      // detaching the listener
      const userDoc = JSON.parse(JSON.stringify(user));
      dispatch({ type: types.updateUser, payload: { user: userDoc } });
      if (userDoc && userDoc.stsTokenManager) {
        const { accessToken } = userDoc.stsTokenManager;
        getLicense(accessToken).then(({ licenseKey }) => {
          dispatch({ type: types.updateLicense, payload: { licenseKey } });
        });
      }
    });
    return () => unsubscribe(); // unsubscribing from the listener when the component is unmounting.
  }, [dispatch]);

  return (
    <Switch>
      <Route exact {...routes.LANDING} />
      <Route exact {...routes.REGISTER} />
      <Route exact {...routes.LOGIN} />
      <Route exact {...routes.LOGOUT} />
      <Route exact {...routes.LICENSE} />
      <Route exact {...routes.TERMS} />
    </Switch>
  );
};

export default App;
