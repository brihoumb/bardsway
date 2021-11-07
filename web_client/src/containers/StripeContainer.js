import React, { useContext } from "react";
import { useToasts } from "react-toast-notifications";

import { pay } from "../utils/license";
import { Context } from "../store/Store";
import { types } from "../store/Reducer";


import {
  useStripe,
  useElements,
  CardNumberElement,
  CardExpiryElement,
  CardCvcElement,
} from "@stripe/react-stripe-js";

import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";

const StripeContainer = (props) => {
  const { amount, disabled, onSuccess } = props;
  const [state, dispatch] = useContext(Context);
  const stripe = useStripe();
  const elements = useElements();
  const { addToast } = useToasts();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const { user } = state;
    if (!user) {
      addToast("Please log in before buying a license", { appearance: "error" });
      return;
    }
    try {
      const cardElement = elements.getElement(CardNumberElement);
      const { error, paymentMethod } = await stripe.createPaymentMethod({
        type: "card",
        card: cardElement,
      });
      if (error) {
        addToast("Invalid card information", { appearance: "error" });
      } else {
        const { accessToken } = user.stsTokenManager;
        const { licenseKey, error } = await pay(accessToken, paymentMethod);
        if (!error && licenseKey) {
          addToast(`Thank you for your purchase. Happy mixing 🚀`, { appearance: "success" });
          dispatch({ type: types.updateLicense, payload: { licenseKey } });
          return onSuccess();
        }
        addToast(error.msg, { appearance: "error" });
      }
    } catch (error) {
      console.log({ error });
      addToast(error, { appearance: "error" });
    }
  };

  return (
    <Form>
      <Form.Group>
        <Form.Label style={{ display: "flex" }}>Card Number</Form.Label>
        <CardNumberElement />
      </Form.Group>
      <br />
      <Form.Row>
        <Form.Group as={Col}>
          <Form.Label style={{ display: "flex" }}>Expiration date</Form.Label>
          <CardExpiryElement />
        </Form.Group>

        <Form.Group as={Col}>
          <Form.Label style={{ display: "flex" }}>CVC</Form.Label>
          <CardCvcElement />
        </Form.Group>
      </Form.Row>

      <Form.Group>
        <Button disabled={!stripe || disabled} onClick={handleSubmit}>
          Pay {amount}
        </Button>
      </Form.Group>
    </Form>
  );
};

export default StripeContainer;
