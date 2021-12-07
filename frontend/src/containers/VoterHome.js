import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import LogoutButton from "../components/LogoutButton.js";
import axios from "axios";
import { isAdmin } from "../util";
import { Redirect } from "react-router-dom";
import { Navbar, Container, Nav } from "react-bootstrap";
import "../App.scss";

const VoterHome = () => {
  const { user, isAuthenticated, getAccessTokenSilently, getIdTokenClaims } =
    useAuth0();

  return isAuthenticated && !isAdmin() ? (
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
              defaultActiveKey="/voter/home"
            >
              <Nav.Link href="/voter/home">Home</Nav.Link>
              <Nav.Link>Upcoming Elections</Nav.Link>
              <Nav.Link>My Vote Status</Nav.Link>
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

export default VoterHome;

//   <Navbar className="color-nav" variant="dark">
//   <Container fluid>
//     <Navbar.Brand>Mimi</Navbar.Brand>
//     <Nav>
//       <Nav.Link className="nav-links">Home</Nav.Link>
//       <Nav.Link className="nav-links">Features</Nav.Link>
//       <Nav.Link className="nav-links">Pricing</Nav.Link>
//     </Nav>
//     <Nav>
//       <LogoutButton />
//     </Nav>
//   </Container>
// </Navbar>;
