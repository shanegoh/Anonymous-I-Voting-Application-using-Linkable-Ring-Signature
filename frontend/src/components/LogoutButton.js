import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import { removeAccessToken, removeRoleID, removeAreaID } from "../util";
import "../App.scss";
import { BsArrowBarRight } from "react-icons/bs";

export default function LogoutButton() {
  const { logout } = useAuth0();

  const attemptLogout = () => {
    removeAccessToken();
    removeRoleID();
    removeAreaID();
    logout({ returnTo: window.location.origin });
  };

  return (
    <Button
      className="text-light color-red"
      size="xxl"
      variant="danger"
      onClick={() => attemptLogout()}
    >
      <BsArrowBarRight />
      Logout
    </Button>
  );
}
