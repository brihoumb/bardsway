import React, { useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";
import { useToasts } from "react-toast-notifications";

import routes from "../constants/routes";
import { signOut } from "../utils/auth";
import { Context } from "../store/Store";
import { types } from "../store/Reducer";

import NavContainer from "../containers/NavContainer";
import Image from "react-bootstrap/Image";
import Logo from "../assets/LogoBardsWay.svg";
import Footer from "../assets/Rectangle.png";

const LogoutPage = () => {
  const [state, dispatch] = useContext(Context);
  const { addToast } = useToasts();
  const history = useHistory();

  const onLogout = async () => {
    dispatch({ type: types.fetchStart });
    const { user, error } = await signOut();
    dispatch({ type: types.fetchEnd, payload: { user } });
    if (user) {
      addToast(`Couldn't sign you out : ${error}`, { appearance: "error" });
    }
  };

  useEffect(() => {
    if (!state.user) history.push(routes.LOGIN.path);
    else onLogout();
  });

  return (
    <NavContainer>
      <style type="text/css">
        {`
          h2, h3, p, label {
            font-family: Lato;
        `}
      </style>
      <Image src={Logo} fluid />
      <h1>Merci de votre passage sur BardsWay et bonne continuation</h1>
      <Image
        src={Footer}
        className={`footer-img`}
        style={{ position: "fixed", width: "100vw", left: 0, bottom: 0, zIndex: "-1" }}
      />
    </NavContainer>
  );
};

export default LogoutPage;
