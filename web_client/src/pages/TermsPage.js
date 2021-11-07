import React from "react";

import NavContainer from "../containers/NavContainer";
import Container from "react-bootstrap/Container";
import Image from "react-bootstrap/Image";
import Footer from "../assets/Rectangle.png";
import Logo from "../assets/LogoBardsWay.svg";


const TermsPage = () => {
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

            .subtitle {
              font-size: 20px;
              margin-top: 8vh;
            }
          `}
        </style>
        <Container>
          <br />
          <Image src={Logo} fluid />
          <br />
          <br />
          <h3 className={`title`}>Terms of use</h3>
          <br />
          <Container>
            <p>Please read these terms of service carefully before using https://bardsway.herokuapp.com
            website operated by Bard's Way.</p>
            <p className={`subtitle`}>Conditions of use</p>
            <p>By using this website, you certify that you have read and reviewed this Agreement and that you
            agree to comply with its terms. If you do not want to be bound by the terms of this Agreement,
            you are advised to leave the website accordingly. Bard's Way only grants use and access of this
            website, its products, and its services to those who have accepted its terms.</p>
            <p className={`subtitle`}>Privacy policy</p>
            <p>Before you continue using our website, we advise you to read our privacy policy https://bardsway.herokuapp.com/terms regarding our user data collection.
            It will help you better understand our practices.</p>
            <p className={`subtitle`}>Age restriction</p>
            <p>You must be at least 18 (eighteen) years of age before you can use this website. By using this
            website, you warrant that you are at least 18 years of age and you may legally adhere to this
            Agreement. Bard's Way assumes no responsibility for liabilities related to age misrepresentation.
            Intellectual property</p>
            <p>You agree that all materials, products, and services provided on this website are the property of
            Bard's Way, its affiliates, directors, officers, employees, agents, suppliers, or licensors including all
            copyrights, trade secrets, trademarks, patents, and other intellectual property. You also agree
            that you will not reproduce or redistribute the Bard's Way’s intellectual property in any way,
            including electronic, digital, or new trademark registrations.</p>
            <p>You grant Bard's Way a royalty-free and non-exclusive license to display, use, copy, transmit, and
            broadcast the content you upload and publish. For issues regarding intellectual property claims,
            you should contact the company in order to come to an agreement.</p>
            <p className={`subtitle`}>User accounts</p>
            <p>As a user of this website, you may be asked to register with us and provide private information.
            You are responsible for ensuring the accuracy of this information, and you are responsible for
            maintaining the safety and security of your identifying information. You are also responsible for
            all activities that occur under your account or password.</p>
            <p>If you think there are any possible issues regarding the security of your account on the website,
            inform us immediately so we may address it accordingly.</p>
            <p>We reserve all rights to terminate accounts, edit or remove content and cancel orders in their
            sole discretion.</p>
            <p>Terms of service template by WebsitePolicies.com</p>
            <p className={`subtitle`}>Applicable law</p>
            <p>By visiting this website, you agree that the laws of the [location], without regard to principles of
            conflict laws, will govern these terms and conditions, or any dispute of any sort that might come
            between Bard's Way and you, or its business partners and associates.
            Disputes</p>
            <p>Any dispute related in any way to your visit to this website or to products you purchase from us
            shall be arbitrated by state or federal court [location] and you consent to exclusive jurisdiction
            and venue of such courts.</p>
            <p className={`subtitle`}>Indemnification</p>
            <p>You agree to indemnify Bard's Way and its affiliates and hold Bard's Way harmless against legal claims
            and demands that may arise from your use or misuse of our services. We reserve the right to
            select our own legal counsel.</p>
            <p className={`subtitle`}>Limitation on liability</p>
            <p>Bard's Way is not liable for any damages that may occur to you as a result of your misuse of our
            website.</p>
            <p>Bard's Way reserves the right to edit, modify, and change this Agreement any time. We shall let our
            users know of these changes through electronic mail. This Agreement is an understanding
            between Bard's Way and the user, and this supersedes and replaces all prior agreements regarding
            the use of this website.</p>
          </Container>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
        </Container>
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
export default TermsPage;
