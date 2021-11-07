import React, { useEffect, useContext } from "react";
import Button from "react-bootstrap/Button";
import { useHistory } from "react-router-dom";
import { useToasts } from "react-toast-notifications";

import { Link } from "react-router-dom";
import routes from "../constants/routes";
import { Context } from "../store/Store";
import { types } from "../store/Reducer";
import { login } from "../utils/auth";

import Logo from "../assets/LogoBardsWay.svg";
import Footer from "../assets/Rectangle.png";
import Image from "react-bootstrap/Image";
import NavContainer from "../containers/NavContainer";
import LoginContainer from "../containers/LoginContainer";

const LoginPage = () => {
  const [state, dispatch] = useContext(Context);
  const history = useHistory();
  const { addToast } = useToasts();

  const onLogin = async ({ email, password }) => {
    dispatch({ type: types.fetchStart });
    const { user, error } = await login({ email, password });
    dispatch({ type: types.fetchEnd, payload: { user } });
    if (user) {
      addToast("Welcome back!", { appearance: "success" });
    } else {
      addToast(error.msg, { appearance: "error" });
    }
  };

  useEffect(() => {
    if (state.user) history.push(routes.LICENSE.path);
  });

  return (
    <NavContainer>
      <style type="text/css">
        {`
          h2, h3, p, label {
            font-family: Lato;
          }

          .title {
            color: #2B2B2B;
            font-family: "Lato";
          }

          .switch {
            margin-top:10px;
            background-color: unset;
            color: #2B2B2B;
            border: none;
          }
        `}
      </style>
      <br />
      <Image src={Logo} fluid />
      <br />
      <br />
      <h3 className={`title`}>Enter your information to connect</h3>
      <br />
      <LoginContainer onLogin={onLogin} />
      <Link to={routes.REGISTER.path}>
        <Button className={`switch`} variant="link"> Go to Register page</Button>
      </Link>
      <Image
        src={Footer}
        className={`footer-img`}
        style={{
          position: "fixed",
          width: "100vw",
          left: 0,
          bottom: 0,
          zIndex: "-1",
        }}
      />
    </NavContainer>
  );
};

export default LoginPage;
