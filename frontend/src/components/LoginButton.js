import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

const LoginButton = () => {
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
      <Button size="lg" variant="danger" onClick={() => loginWithRedirect()}>
        Log In
      </Button>
    </div>
  );
};

export default LoginButton;
