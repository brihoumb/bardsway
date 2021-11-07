import React, { useContext } from "react";
import { useToasts } from "react-toast-notifications";
import { Context } from "../store/Store";

import Container from "react-bootstrap/Container";
import Image from "react-bootstrap/Image";
import Column from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";
import Badge from "react-bootstrap/Badge";
import NavContainer from "../containers/NavContainer";

import Antoine from "../assets/faces/Antoine.jpg";
import Aurel from "../assets/faces/Aurel.jpg";
import Benjamin from "../assets/faces/Benjamin.jpg";
import Cedric from "../assets/faces/Cedric.jpg";
import Jacques from "../assets/faces/Jacques.jpg";
import Nicolas from "../assets/faces/Nicolas.jpg";
import Victor from "../assets/faces/Victor.jpg";
import Logo from "../assets/LogoBardsWay.svg";
import SoftHome from "../assets/soft-home.png";
import SoftResult from "../assets/soft-result.png";

import { Link } from "react-router-dom";
import routes from "../constants/routes";

const LandingPage = () => {
  const [state] = useContext(Context);
  const { addToast } = useToasts();

  const checkAndDownload = (url) => {
    const { user } = state;
    if (!user || !user.email)
      addToast(`You must be logged in to download Bardsway.`, {
        appearance: "warning",
      });
    else if (!user.licenseKey)
      addToast(`Please purchase a license to download Bardsway.`, {
        appearance: "warning",
      });
    else window.location.href = url;
  };

  const windowsDownload = (e) => {
    e.preventDefault();
    checkAndDownload("https://github.com/brihoumb/bardsway/releases/download/1.0.0/installer_windows.zip");
  };

  const linuxDownload = (e) => {
    e.preventDefault();
    checkAndDownload("https://github.com/brihoumb/bardsway/releases/download/1.0.0/installer_linux.zip");
  };

  function faq() {
    addToast(
      `FAQ are not available right now, please contact us with this email: "bardswaycorp@gmail.com".`,
      {
        appearance: "warning",
      }
    );
  }

  function contact() {
    addToast(`If you want to contact us, use this email : "bardswaycorp@gmail.com".`, {
      appearance: "warning",
    });
  }

  return (
    <NavContainer>
      <style type="text/css">
        {`
          h2, h3, p {
            font-family: Lato;
          }

          .top {
            background: #FFFFFF;
            height:100vh;
            padding: 5vh 5vw;
            display: flex;
            align-items: center;
            justify-content: center;
          }

          .top .row {
            margin-bottom: 20vh;
          }

          .top .row .logo {
            margin-right: 6vw;
          }

          .top .download {
            border: 1px solid #000000;
            border-radius: 1rem;
            padding: 0;
          }

          .top .download .first {
            border: 0 !important;
            flex-direction: column;
          }

          .top .download .option {
            margin: 0;
            width: 100%;
            height: 33%;
            border-top: 1px solid #000000;
            display: flex;
            justify-content: center;
            align-content: center;
          }

          .top .download .option .option-text {
            font-family: Lato;
            font-style: normal;
            font-weight: bold;
            font-size: 1.5em;
            color: #2B2B2B;
          }

          .top .download .option .os {
            margin-right: 4vw;
          }

          .top .download .option .box {
            min-width: 2rem;
            height: 8vh;
            width: 5vw;
            background-color: #2B2B2B;
            border-radius: 20px;
          }

          .top .download .option .box .helper {
            display: inline-block;
            height: 100%;
            vertical-align: middle;
          }

          .top .hook {
            font-family: Lato;
            font-style: normal;
            font-weight: 300;
            font-size: 2.25em;
            line-height: 43px;
            color: #2B2B2B;
          }

          .middle {
            background: #F9F8F8;
            margin: 0;
            padding: 0 5vw;
            display: flex;
            align-items: center;
          }

          .middle .left {
            margin-right: 5vw;
          }

          .middle p {
            font-family: Lato;
            font-style: normal;
            font-weight: normal;
            font-size: 1.5em;
            line-height: 34px;
            display: flex;
            align-items: center;
            text-align: center;
            text-transform: uppercase;
          }

          .bottom {
            background: #F0EFEF;
            padding: 2vw 2vw 2vh;
            margin: 0;
            position: relative;
          }

          .bottom .footer {
            position: absolute;
            bottom: 2vh;
            left: 0;
          }

          .bottom h2 {
            font-family: Lato;
            font-style: normal;
            font-weight: bold;
            font-size: 2.5em;
            line-height: 48px;
          }

          .bottom .footer .foot-bouton {
            margin-left: 2vw;
          }

          .bottom .footer .foot-bouton {
            border: none;
          }

          .bottom .footer h3 {
            font-family: Lato;
            font-style: normal;
            font-weight: bold;
            color: #2B2B2B;
            font-size: 1.5em;
            line-height: 29px;
          }

          .bottom .profil {
            max-height: 20vh;
            border-radius: 10%;
          }

          .landing-container {
            width:100vw;
            height:95vh;
          }

          @media only screen and (min-height : 700px) and (orientation : landscape) {
            p {
              font-size: calc(0.40em + 0.5vw + 0.5vh) !important;
              line-height: calc(0.70em + 0.5vw + 0.5vh) !important;
            }

            h3 {
              font-size: calc(0.70em + 0.5vw + 0.5vh) !important;
              line-height: calc(1em + 0.5vw + 0.5vh) !important;
            }

            .bottom .profil {
              max-height: 12vh;
              border-radius: 10%;
            }

            .bottom .images {
              margin-top: 10px !important;
            }
            .middle img {
              max-width: 60%;
            }
          }

          @media only screen and (max-height : 700px) and (orientation : landscape) {
            .main-page {
              padding-top: 25vh !important;
            }
            
            p {
              font-size: calc(0.40em + 0.5vw + 0.5vh) !important;
              line-height: calc(0.70em + 0.5vw + 0.5vh) !important;
            }

            h3 {
              font-size: calc(0.70em + 0.5vw + 0.5vh) !important;
              line-height: calc(1em + 0.5vw + 0.5vh) !important;
            }

            .bottom .profil {
              max-height: 12vh;
              border-radius: 10%;
            }

            .bottom .images {
              margin-top: 10px !important;
            }
            .middle img {
              max-width: 60%;
            }
          }

          @media only screen and (min-width : 400px) and (max-width : 1000px) and (orientation:portrait){
            p {
              font-size: calc(0.40em + 2vw) !important;
              line-height: calc(0.70em + 2vw) !important;
            }

            h3 {
              font-size: 1.5em !important;
            }

            .bottom .profil {
              max-height: 10vh;
            }

            .footer h3 {
              font-size: 1.4em !important;
            }
          }

          @media only screen and (max-width: 400px) {
            p {
              font-size: calc(0.4em + 2vw) !important;
              line-height: calc(0.70em + 2vw) !important;
            }

            h3 {
              font-size: 1em !important;
            }

            h2 {
              font-size: 2em !important;
            }

            .bottom .profil {
              max-height: 8vh !important;
            }

            .bottom .images {
              flex-basis: inherit !important;
              margin: 0 !important;
              padding: 0 !important;
            }

            .bottom .bottom-box {
              margin: 20px 0 0 0 !important;
              padding: 0 !important;
            }
          }
        `}
      </style>
      <Container className={`top landing-container`}>
        <Column fluid>
          <Row className={`row`}>
            <Image src={Logo} className={`logo`} style={{ maxWidth: "40%", height: "auto" }} />
            <Column className={`download`} auto style={{ maxWidth: "390px", minHeight: "35vh" }}>
              <Container className={`option first`}>
                <Container>
                  <p style={{ margin: 0 }} className={`option-text`}>
                    Latest release: <Badge variant="secondary">1.0.0</Badge>
                  </p>
                </Container>
              </Container>
              <Row className={`option`} fluid>
                <p className={`option-text os`}>Windows</p>
                <Button variant="dark" onClick={windowsDownload}>
                  <i class="fas fa-download"></i>
                </Button>
              </Row>
              <Row className={`option`} fluid>
                <p className={`option-text os`}>Linux</p>
                <Button variant="dark" onClick={linuxDownload}>
                  <i class="fas fa-download"></i>
                </Button>
              </Row>
            </Column>
          </Row>
          <Container>
            <h3 className={`hook`}>
              The most advanced music separation and transcription toolkit on the internet.
            </h3>
          </Container>
        </Column>
      </Container>
      <Container className={`middle landing-container`} fluid>
        <Row fluid>
          <Column className={`left`}>
            <p>
              It is very expensive to afford musicians or sound engineers to recreate or isolate specific
              instrumental parts of a music, and even then, the result might not be the one you wished for.
              Furthermore, what if you wanted to learn this piano improvisation recorded with your phone last
              week ? Impossible ? This time is over now. Bardsway is a software that enables musicians, DJs
              and sound engineers to isolate the instruments of an audio file and generate sheet music.
            </p>
          </Column>
          <Image className={`right`} src={SoftResult} fluid style={{ maxHeight: "50vh" }} />
        </Row>
      </Container>
      <Container className={`middle landing-container`} fluid>
        <Row>
          <Image className={`left`} src={SoftHome} fluid style={{ maxHeight: "50vh", marginBottom: "2vh" }} />
          <Column className={`right`}>
            <p>
              Under the hood, Bardsway is a two-stage machine learning algorithm. The first stage uses deep
              learning to separate each instrument from the source file. Each instrument is then available to
              listen individually. The next step is a state-of-the-art convolutional model that generate midi
              files based on an audio source. Combining the two enables Bardsway to provide an end-to-end
              solution that can isolate and transcribe audio files.
            </p>
          </Column>
        </Row>
      </Container>
      <Container className={`bottom landing-container`} fluid>
        <Container className={`bottom-box`}>
          <Container style={{ height: "10vh" }}>
            <h2>ABOUT US</h2>
          </Container>
          <Column className={`images`}>
            <Row>
              <Column>
                <Image src={Antoine} className={`profil`} />
                <p>Antoine Cauquil</p>
              </Column>
              <Column>
                <Image src={Aurel} className={`profil`} />
                <p>Aurel Ghirenghelli</p>
              </Column>
              <Column>
                <Image src={Benjamin} className={`profil`} />
                <p>Benjamin Brihoum</p>
              </Column>
            </Row>
            <Row>
              <Column>
                <Image src={Cedric} className={`profil`} />
                <p>Cedric Karaoglanian</p>
              </Column>
            </Row>
            <Row>
              <Column>
                <Image src={Jacques} className={`profil`} />
                <p>Jacques Alzate</p>
              </Column>
              <Column>
                <Image src={Nicolas} className={`profil`} />
                <p>Nicolas Deviers</p>
              </Column>
              <Column>
                <Image src={Victor} className={`profil`} />
                <p>Victor Hazard</p>
              </Column>
            </Row>
          </Column>
        </Container>
        <Container className={`footer`} fluid>
          <Row className="justify-content-md-center">
            <div className={`foot-bouton`}>
              <Link to={routes.TERMS.path}>
                <h3>TERMS OF USE</h3>
              </Link>
            </div>
            <button className={`foot-bouton`}>
              <h3 onClick={faq}>FAQ</h3>
            </button>
            <button className={`foot-bouton`}>
              <h3 onClick={contact}>CONTACT US</h3>
            </button>
          </Row>
        </Container>
      </Container>
    </NavContainer>
  );
};
export default LandingPage;
