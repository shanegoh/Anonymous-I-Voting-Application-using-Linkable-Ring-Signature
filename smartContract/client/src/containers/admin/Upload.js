import React from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import "../../App.scss";

export default function Upload() {
  return isAdmin() ? (
    <div>
      <NavBar />
      Building
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
