import React, { useState, useContext, useEffect } from "react";
import { useToasts } from "react-toast-notifications";

import { Context } from "../store/Store";
import licenses from "../constants/licenses";
import { getProduct } from "../utils/license";

import NavContainer from "../containers/NavContainer";
import StripeContainer from "../containers/StripeContainer";
import LicenseCard from "../components/LicenseCard";
import LicenseKey from "../components/LicenseKey";
import Image from "react-bootstrap/Image";
import CardDeck from "react-bootstrap/CardDeck";
import Modal from "react-bootstrap/Modal";
import Logo from "../assets/LogoBardsWay.svg";
import Footer from "../assets/Rectangle.png";

import { Link } from "react-router-dom";
import routes from "../constants/routes";

const LicensePage = () => {
  const [showModal, setShowModal] = useState(false);
  const [price, setPrice] = useState(null);
  const [state] = useContext(Context);
  const { addToast } = useToasts();

  useEffect(() => {
    getProduct().then(({ price, error }) => {
      if (price) setPrice(price);
    });
  });

  const handleShow = () => {
    if (!state.user) {
      addToast("You need to be logged in to buy a license", {
        appearance: "error",
      });
    } else setShowModal(true);
  };
  const handleClose = () => setShowModal(false);
  const handleSuccess = () => setShowModal();

  const licenseCards = licenses.map((license) => (
    <LicenseCard key={license.title} onBuy={price && handleShow} {...license} price={price || "Loading..."} />
  ));

  return (
    <NavContainer>
      <br />
      <Image src={Logo} fluid />
      <br />
      <br />
      <h1 style={{ fontFamily: "Lato" }}>Buy your license right here</h1>
      <br />
      {state.user && <LicenseKey licenseKey={state.user.licenseKey} />}
      <CardDeck style={{ margin: "auto", maxWidth: "30rem" }}>{licenseCards}</CardDeck>

      <Modal centered show={showModal} onHide={handleClose}>
        <Modal.Header>
          <Modal.Title>Buy a Bard's Way license here</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <StripeContainer amount={price} onSuccess={handleSuccess} />
        </Modal.Body>
      </Modal>
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
      <br />
      <br />
      <br />
      <br />
      <Link to={routes.TERMS.path} style={{ color: "#2B2B2B" }}>
        <p>TERMS OF USE</p>
      </Link>
    </NavContainer>
  );
};

export default LicensePage;
