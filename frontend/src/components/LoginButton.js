import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import "../App.scss";
import { BsArrowBarRight } from "react-icons/bs";

export default function LoginButton() {
  const { loginWithRedirect } = useAuth0();

  return (
    <div>
      <Button
        className="text-light"
        size="lg"
        variant="danger"
        onClick={() => loginWithRedirect()}
      >
        <BsArrowBarRight />
        Log In
      </Button>
    </div>
  );
}
