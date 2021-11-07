import React from "react";

import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";

const LicenseCard = (props) => (
  <Card className="text-center">
    <Card.Header>{props.title}</Card.Header>
    <Card.Body>
      <Card.Text>{props.description}</Card.Text>
    </Card.Body>
    <Card.Body>
      <Button variant={props.variant} style={{ backgroundColor: "#2B2B2B" }} onClick={props.onBuy}>
        {props.price}
      </Button>
    </Card.Body>
  </Card>
);

export default LicenseCard;
