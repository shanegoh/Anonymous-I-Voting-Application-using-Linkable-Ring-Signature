import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "./App.css";
import LogoutButton from "./components/LogoutButton.js";
function VoterHome() {
  const { isAuthenticated } = useAuth0();

  if (isAuthenticated) {
    return (
      <div class="App-header">
        <LogoutButton />
      </div>
    );
  }
}

export default VoterHome;
