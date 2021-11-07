import React, { useState } from "react";

import { checkEmail, checkPassword } from "../utils/auth";

import Form from "../components/Form";

const RegisterContainer = (props) => {
  const { onRegister } = props;
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [password2, setPassword2] = useState("");
  const [password2Error, setPassword2Error] = useState("");

  const checkPassword2 = (value) => value === password;

  const onEmailChange = (value) => {
    setEmail(value);
    setEmailError(checkEmail(value) ? "" : "Please enter a valid email address.");
  };

  const onPasswordChange = (value) => {
    setPassword(value);
    setPasswordError(
      checkPassword(value)
        ? ""
        : "Password must be at least 8 characters (lowercase + uppercase + number + special character)"
    );
  };

  const onPassword2Change = (value) => {
    setPassword2(value);
    setPassword2Error(checkPassword2(value) ? "" : "Passwords don't match");
  };

  const canSubmit = () => checkPassword(password) && checkEmail(email) && password === password2;

  const handleSubmit = (event) => {
    event.preventDefault();
    onRegister({ email, password });
  };

  const formFields = [
    {
      label: "Email address",
      type: "email",
      placeholder: "john@doe.co",
      onChange: (e) => onEmailChange(e.target.value),
      value: email,
      error: emailError,
    },
    {
      label: "Password",
      type: "password",
      placeholder: "sTr0nGP4ssw0rd!",
      onChange: (e) => onPasswordChange(e.target.value),
      value: password,
      error: passwordError,
    },
    {
      label: "Confirm Password",
      type: "password",
      placeholder: "",
      onChange: (e) => onPassword2Change(e.target.value),
      value: password2,
      error: password2Error,
    },
  ];

  return <Form fields={formFields} submit="Register" onSubmit={handleSubmit} canSubmit={canSubmit()} />;
};

export default RegisterContainer;
