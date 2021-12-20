import React from "react";
import Media from "../../components/Media.js";
import NavBar from "../../components/NavBar.js";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import "../../App.scss";

export default function Voter() {
  return !isAdmin() ? (
    <div>
      <NavBar />
      <Media />
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}