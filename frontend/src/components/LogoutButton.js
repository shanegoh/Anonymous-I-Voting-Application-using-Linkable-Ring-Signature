import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <div class="App-header">
      <Button
        size="lg"
        variant="danger"
        onClick={() => logout({ returnTo: window.location.origin })}
      >
        Log Out
      </Button>
    </div>
  );
};

export default LogoutButton;
