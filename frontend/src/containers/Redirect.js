import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "../App.scss";
import axios from "axios";
import {
  setAccessToken,
  setIDToken,
  getIDToken,
  setRoleID,
  admin_role,
  voter_role,
} from "../util";

const Redirect = ({ history }) => {
  const { user, isAuthenticated, getAccessTokenSilently, getIdTokenClaims } =
    useAuth0();

  useEffect(() => {
    const getUserMetadata = async () => {
      try {
        getIdTokenClaims()
          .then((claims) => {
            setIDToken(claims.__raw);
          })
          .catch((err) => {
            console.debug("ID Token: No Claims Found", err);
          });

        const accessToken = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUTH0_API,
          scope: "read:current_user",
        });
        setAccessToken(accessToken);

        axios
          .get("/api/private", {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              id_token: `Bearer ${getIDToken()}`,
            },
          })
          .then((res) => {
            if (res.status === 200) {
              setRoleID(res.data.role_id);
              if (res.data.role_id === admin_role) {
                history.push("/admin/home");
              } else if (res.data.role_id === voter_role) {
                history.push("/voter/home");
              } else {
                console.log("Error: No roles found");
              }
            }
          })
          .catch((err) => {});
      } catch (e) {
        console.log(e.message);
      }
    };
    getUserMetadata();
  }, [getAccessTokenSilently, user?.sub]);

  return isAuthenticated ? <div /> : <Redirect to="/main" />;
};

export default Redirect;
