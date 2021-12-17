import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import { removeAccessToken, removeIDToken, removeRoleID } from "../util";
import "../App.scss";
import { BsArrowBarRight } from "react-icons/bs";

export default function LogoutButton() {
  const { logout } = useAuth0();

  const attemptLogout = () => {
    removeIDToken();
    removeAccessToken();
    removeRoleID();
    logout({ returnTo: window.location.origin + "/main" });
  };

  return (
    <Button
      className="text-light"
      size="xxl"
      variant="danger"
      onClick={() => attemptLogout()}
    >
      <BsArrowBarRight />
      Logout
    </Button>
  );
}
