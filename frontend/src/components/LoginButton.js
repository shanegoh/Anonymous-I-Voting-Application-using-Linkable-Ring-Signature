import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <div>
      <Button size="lg" variant="danger" onClick={() => loginWithRedirect()}>
        Log In
      </Button>
    </div>
  );
};

export default LoginButton;
