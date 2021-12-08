import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "../App.scss";
import LogoutButton from "../components/LogoutButton.js";
import axios from "axios";
import { isAdmin } from "../util";
import { Redirect } from "react-router-dom";
import { Navbar, Container, Nav } from "react-bootstrap";
import "../App.scss";

const Admin = () => {
  return isAdmin() ? (
    <div>
      <Navbar className="color-nav" variant="dark" expand="lg">
        <Container fluid>
          <Navbar.Brand>Mimi</Navbar.Brand>
          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="justify-content-center"
              className="me-auto my-2 my-lg-0"
              style={{ maxHeight: "100px" }}
              navbarScroll
              defaultActiveKey="/admin/home"
            >
              <Nav.Link href="/admin/home">Home</Nav.Link>
              <Nav.Link>Results</Nav.Link>
              <Nav.Link>Upload</Nav.Link>
            </Nav>
            <Nav>
              <LogoutButton />
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
};

export default Admin;
