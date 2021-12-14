import React from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Button } from "react-bootstrap";
import "../../App.scss";
import { BsPlusLg } from "react-icons/bs";

export default function Admin({ history }) {
  const routeChange = () => {
    let path = "/admin/create";
    history.push(path);
  };

  return isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        <Button className="btn-origin btn-lg color-nav" active>
          Tampines GRC election on 12 December 2021 4pm
        </Button>
        <Button className="btn-origin btn-lg color-nav" active>
          Tampines GRC election on 12 December 2021 4pm
        </Button>
        <Button
          className="btn-circle btn-success"
          to={"/admin/create"}
          onClick={routeChange}
        >
          <BsPlusLg className="fs-3" />
        </Button>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
