import React from "react";
import { isAdmin, hasToken } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import EventForm from "../../components/EventForm.js";
import "../../App.scss";

export default function CreateElection() {
  return isAdmin() && hasToken() ? (
    <div>
      <NavBar />
      <EventForm />
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
