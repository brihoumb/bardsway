import React, { useContext } from "react";

import { Context } from "../store/Store";
import { signOut } from "../utils/auth";

import Navbar from "../components/Navbar";
import Container from "react-bootstrap/Container";

const NavContainer = (props) => {
  const [state] = useContext(Context);

  return (
    <>
      <style type="text/css">
        {`
        .main-page {
          margin: 0;
          padding: 0;
          padding-top: 6vh;
        }
        `}
      </style>
      <Navbar user={state.user} onSignOut={signOut} />
      <Container className={`main-page`} fluid>
        <div style={{ textAlign: "center" }}>{props.children}</div>
      </Container>
    </>
  );
};

export default NavContainer;
