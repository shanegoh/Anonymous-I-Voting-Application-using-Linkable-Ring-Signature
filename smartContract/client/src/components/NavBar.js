import React from "react";
import LogoutButton from "../components/LogoutButton.js";
import { Navbar, Container, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
import "../App.scss";
import { ImHome } from "react-icons/im";
import {
  BsFillCalendar2WeekFill,
  BsThreeDots,
  BsBookmarkCheckFill,
  BsCloudUploadFill,
} from "react-icons/bs";
import { isAdmin } from "../util";

export default function NavBar() {
  return (
    <div>
      <Navbar className="color-nav" variant="dark" expand="lg">
        <Container fluid>
          <Navbar.Brand className="fw-bold">Mimi</Navbar.Brand>
          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="me-auto my-2 my-lg-0 justify-content-center"
              navbarScroll
            >
              <Nav.Link
                as={Link}
                to={isAdmin() ? "/admin/home" : "/voter/home"}
                className="text-center fw-bold"
              >
                <ImHome />
                <br />
                Home
              </Nav.Link>
              <Nav.Link
                as={Link}
                to={isAdmin() ? "/admin/result" : "/voter/upcomingelections"}
                className="text-center fw-bold"
              >
                {isAdmin() ? (
                  <div>
                    <BsBookmarkCheckFill />
                    <br /> Results
                  </div>
                ) : (
                  <div>
                    <BsFillCalendar2WeekFill />
                    <br /> Elections
                  </div>
                )}
              </Nav.Link>
              <Nav.Link
                as={Link}
                to={isAdmin() ? "/admin/upload" : "/voter/myvotestatus"}
                className="text-center fw-bold"
              >
                {isAdmin() ? (
                  <div>
                    <BsCloudUploadFill />
                    <br />
                    Upload
                  </div>
                ) : (
                  <div>
                    <BsThreeDots />
                    <br /> Vote Status
                  </div>
                )}
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
}
