import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import AlertBox from "../components/AlertBox.js";
import { Spinner } from "react-bootstrap";
import { DANGER } from "../util";
import "../App.scss";
import axios from "axios";
import {
  setAccessToken,
  setRoleID,
  ADMIN_ROLE,
  VOTER_ROLE,
  setAreaID,
} from "../util";

export default function Redirect({ history }) {
  const [show, setShow] = useState(false); // Logic for displaying alert
  const handleShow = () => setShow(true); // Logic for displaying alert
  const [errMsg, setErrMsg] = useState(); // Logic setting error msg
  const [variant, setVariant] = useState();
  const [isRedirecting, setRedirectingStatus] = useState(true);
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    const getUserMetadata = async () => {
      try {
        const accessToken = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUTH0_API,
          scope: "read:current_user",
        });
        setAccessToken(accessToken);

        axios
          .get(process.env.REACT_APP_PATH + "/findUserInformation", {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          })
          .then((res) => {
            if (res.status === 200) {
              console.log(res.data);
              setRoleID(res.data.role);
              setRedirectingStatus((isRedirecting) => false);
              if (res.data.role === ADMIN_ROLE) {
                history.push("/admin/home");
              } else if (res.data.role === VOTER_ROLE) {
                setAreaID(res.data.area_id);
                history.push("/voter/home");
              } else {
                throw new Error("No roles found.");
              }
            }
          })
          .catch((err) => {
            // Set error message
            console.log(err.response.data.message);
            setRedirectingStatus((isRedirecting) => false);
            setErrMsg((errMsg) => err.response.data.message);
            setVariant((variant) => DANGER);
            handleShow(); // Display alert
          });
      } catch (e) {
        setErrMsg((errMsg) => e.message);
        setVariant((variant) => DANGER);
        handleShow(); // Display alert
      }
    };
    getUserMetadata();
  }, [getAccessTokenSilently]);

  return isAuthenticated ? (
    <div className="d-flex flex-column pt-4 align-items-center ">
      {show ? (
        <AlertBox
          err={[]}
          setShow={setShow}
          errMsg={errMsg}
          variant={variant}
        />
      ) : (
        <></>
      )}
      {isRedirecting ? (
        <div className="d-flex justify-content-center align-items-center flex-column mainLoader ">
          <Spinner
            animation="border"
            role="status"
            variant="dark"
            className=".loader"
          ></Spinner>
          <span className="">Logging in...</span>
        </div>
      ) : (
        <></>
      )}
    </div>
  ) : (
    <Redirect to="/" />
  );
}
