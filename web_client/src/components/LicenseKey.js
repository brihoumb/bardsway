import React, { useState } from "react";

import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";

const LicenseKey = (props) => {
  const { licenseKey } = props;
  console.log(`rendered with license ${licenseKey}`);
  const [copied, setCopied] = useState(false);

  const onCopy = async (e) => {
    e.preventDefault();
    await navigator.clipboard.writeText(licenseKey);
    setCopied(true);
  };

  return licenseKey ? (
    <Container style={{ margin: "auto", marginBottom: "1rem", maxWidth: "30rem" }}>
      <Form>
        <Form.Label>Your license key</Form.Label>
        <Form.Row>
          <Col>
            <Form.Control readOnly value={licenseKey} style={{ textAlign: "center", background: "white" }} />
          </Col>
          <Col md="auto">
            <OverlayTrigger placement="right" overlay={<Tooltip>{copied ? "Copied!" : "Copy"}</Tooltip>}>
              <Button variant="light" onClick={onCopy}>
                <i class="fa fa-copy" />
              </Button>
            </OverlayTrigger>
          </Col>
        </Form.Row>
      </Form>
    </Container>
  ) : (
    <p>No license found for your account!</p>
  );
};

export default LicenseKey;
