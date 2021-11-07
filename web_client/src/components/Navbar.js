import React from "react";
import { Link } from "react-router-dom";

import routes from "../constants/routes";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";

const AuthNav = (props) => {
  const { user } = props;

  return user ? (
    <Nav className="justify-content-end">
      <Navbar.Text className="bw-nav">
        Signed in as <b>{`${user.email}`}</b>
      </Navbar.Text>
      <Nav.Link as={Link} to={routes.LOGOUT.path} className="bw-nav">
        Logout
      </Nav.Link>
    </Nav>
  ) : (
    <Nav className="justify-content-end">
      <Nav.Link as={Link} to={routes.LOGIN.path} className="bw-nav" style={{ marginRight: "10px" }}>
        LOGIN
      </Nav.Link>
      <Nav.Link as={Link} to={routes.REGISTER.path} className="bw-nav">
        REGISTER
      </Nav.Link>
    </Nav>
  );
};

const BardsNavBar = (props) => (
  <Navbar expand="md" fixed="top" className="bw-nav" variant="dark">
    <Navbar.Toggle aria-controls="basic-navbar-nav" className="bw-nav" />
    <Navbar.Collapse id="basic-navbar-nav" className="bw-nav">
      <Nav className="mr-auto bw-nav">
        <Nav.Link as={Link} to={routes.LANDING.path} className="bw-nav" style={{ marginRight: "10px" }}>
          HOME
        </Nav.Link>
        <Nav.Link as={Link} to={routes.LICENSE.path} className="bw-nav" style={{ marginRight: "10px" }}>
          BUY NOW
        </Nav.Link>
        <Nav.Link as={Link} to={routes.LANDING.path} className="bw-nav">
          ABOUT US
        </Nav.Link>
      </Nav>
      <AuthNav {...props} />
    </Navbar.Collapse>
  </Navbar>
);

export default BardsNavBar;
