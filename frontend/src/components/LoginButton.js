import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import "../App.scss";
import { BsArrowBarRight } from "react-icons/bs";
import App from "../App";

export default function LoginButton() {
  const { loginWithRedirect } = useAuth0();

  // const attemptLogin = () => {
  //   axios
  //     .get("http://localhost:5000/login")
  //     .then((res) => {
  //       if (res.status === 200) {
  //         //navigate("/Dashboard");
  //         console.log(res);
  //       }
  //     })
  //     .catch((err) => {});
  // };

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
