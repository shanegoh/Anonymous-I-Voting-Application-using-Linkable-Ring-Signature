import React from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Button } from "react-bootstrap";
import "../../App.scss";

export default function Results() {
  return isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        <Button className="btn-origin btn-lg color-nav btn-success" active>
          Tampines GRC election on 12 December 2021 4pm
        </Button>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
