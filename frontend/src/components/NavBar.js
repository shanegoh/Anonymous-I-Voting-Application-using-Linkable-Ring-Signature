import React from "react";
import LogoutButton from "../components/LogoutButton.js";
import { Navbar, Container, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
import "../App.scss";

const NavBar = () => {
  return (
    <div>
      <Navbar className="color-nav" variant="dark" expand="lg">
        <Container fluid>
          <Navbar.Brand>Mimi</Navbar.Brand>
          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="justify-content-center"
              className="me-auto my-2 my-lg-0"
              navbarScroll
            >
              <Nav.Link as={Link} to="/voter/home">
                Home
              </Nav.Link>
              <Nav.Link as={Link} to="/voter/upcomingelections">
                Upcoming Elections
              </Nav.Link>
              <Nav.Link as={Link} to="/voter/myvotestatus">
                My Vote Status
              </Nav.Link>
            </Nav>
            <Nav>
              <LogoutButton />
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
};

export default NavBar;
