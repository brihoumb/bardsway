import React, { useState } from "react";

import { checkEmail, checkPassword } from "../utils/auth";

import Form from "../components/Form";

const LoginContainer = (props) => {
  const { onLogin } = props;
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");

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

  const canSubmit = () => checkEmail(email) && checkPassword(password);

  const handleSubmit = (event) => {
    event.preventDefault();
    onLogin({ email, password });
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
  ];

  return <Form fields={formFields} submit="Login" onSubmit={handleSubmit} canSubmit={canSubmit()} />;
};

export default LoginContainer;
