import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "../App.css";
import LogoutButton from "../components/LogoutButton.js";
import axios from "axios";
import { setAccessToken, setIDToken, getIDToken } from "../util";

const VoterHome = () => {
  const { user, isAuthenticated, getAccessTokenSilently, getIdTokenClaims } =
    useAuth0();

  useEffect(() => {
    const getUserMetadata = async () => {
      try {
        const accessToken = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUTH0_API,
          scope: "read:current_user",
        });
        setAccessToken(accessToken);
        getIdTokenClaims()
          .then((claims) => {
            setIDToken(claims.__raw);
          })
          .catch((err) => {
            console.debug("ID Token: No Claims Found", err);
          });

        axios
          .get("/api/private", {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              id_token: `Bearer ${getIDToken()}`,
            },
          })
          .then((res) => {
            if (res.status === 200) {
              console.log(res);
            }
          })
          .catch((err) => {});
      } catch (e) {
        console.log(e.message);
      }
    };
    getUserMetadata();
  }, [getAccessTokenSilently, user?.sub]);

  return (
    isAuthenticated && (
      <div className="App-header">
        <img src={user.picture} alt={user.name} />
        <h2>{user.name}</h2>
        <p>{user.email}</p>
        <LogoutButton />
      </div>
    )
  );
};

export default VoterHome;
