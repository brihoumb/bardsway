import React from "react";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

const BardsForm = (props) => {
  const { fields, submit, onSubmit, canSubmit } = props;
  const formFields = fields.map((field) => {
    const { label, type, placeholder, onChange, value, error } = field;
    return (
      <Form.Group key={label}>
        <Form.Label style={{ display: "flex" }}>{label}</Form.Label>
        <Form.Control type={type} placeholder={placeholder} onChange={onChange} value={value} />
        {error && <Form.Text style={{ textAlign: "start", color: "red" }}>{error}</Form.Text>}
      </Form.Group>
    );
  });

  return (
    <Form style={{ margin: "auto", maxWidth: "30rem" }}>
      {formFields}
      <Button variant="primary" type="submit" onClick={onSubmit} disabled={!canSubmit}>
        {submit}
      </Button>
    </Form>
  );
};

export default BardsForm;
