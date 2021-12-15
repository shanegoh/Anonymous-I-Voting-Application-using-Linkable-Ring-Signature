import React from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import EventForm from "../../components/EventForm.js";
import "../../App.scss";

export default function EditElection() {
  return isAdmin() ? (
    <div>
      <NavBar />
      <EventForm />
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
