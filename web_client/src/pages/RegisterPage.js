import React, { useEffect, useContext } from "react";
import { useHistory, Link } from "react-router-dom";
import { useToasts } from "react-toast-notifications";

import routes from "../constants/routes";
import { register } from "../utils/auth";
import { Context } from "../store/Store";
import { types } from "../store/Reducer";

import Button from "react-bootstrap/Button";

import NavContainer from "../containers/NavContainer";
import RegisterContainer from "../containers/RegisterContainer";
import Image from "react-bootstrap/Image";
import Logo from "../assets/LogoBardsWay.svg";
import Footer from "../assets/Rectangle.png";

const RegisterPage = () => {
  const [state, dispatch] = useContext(Context);
  const history = useHistory();
  const { addToast } = useToasts();

  const onRegister = async ({ email, password }) => {
    dispatch({ type: types.fetchStart });
    const { user, error } = await register({ email, password });
    dispatch({ type: types.fetchEnd, payload: { user } });
    if (user) {
      addToast(
        "Thanks for joining us! You're just an email confirmation away from being able to buy a license 📡.",
        { appearance: "success" }
      );
      history.push(routes.LICENSE.path);
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
      <h3 className="title">Enter your information to create an account</h3>
      <br />
      <RegisterContainer onRegister={onRegister} />
      <Link to={routes.LOGIN.path}>
        <Button className={`switch`} variant="link">
          Go to Login page
        </Button>
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

export default RegisterPage;
