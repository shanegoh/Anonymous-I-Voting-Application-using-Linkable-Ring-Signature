import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import LogoutButton from "../components/LogoutButton.js";
import axios from "axios";
import { isAdmin } from "../util";
import { Redirect } from "react-router-dom";
import { Navbar, Container, Nav, Card, Table, Stack } from "react-bootstrap";
import "../App.scss";

const VoterHome = () => {
  const { user, isAuthenticated, getAccessTokenSilently, getIdTokenClaims } =
    useAuth0();

  return isAuthenticated && !isAdmin() ? (
    <div>
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
      <div style={{ paddingTop: "3rem" }}>
        <Stack className="stack-align" direction="horizontal" gap={3}>
          <div>
            <Card style={{ width: "20rem", height: "25rem", border: "none" }}>
              <Card.Body className="cardNews text-light">
                <Card.Title className="cardHeader">GENERAL</Card.Title>
                <Card.Text style={{ fontSize: "1.2rem" }}>
                  Foreign Interference (Countermeasures) Bill - Wrap-Up Speech
                  by Mr K Shanmugam, Minister for Home Affairs and Minister for
                  Law
                </Card.Text>
                <Card.Text style={{ fontSize: "1.2rem" }}>4 Oct 2021</Card.Text>
              </Card.Body>
            </Card>
          </div>
          <div>
            <Card style={{ width: "20rem", height: "25rem", border: "none" }}>
              <Card.Body className="cardNews text-light">
                <Card.Title className="cardHeader">GENERAL</Card.Title>
                <Card.Text style={{ fontSize: "1.2rem" }}>
                  Second Reading of Foreign Interence (Countermeasures) Bill -
                  Speech by Mr K Shanmugam, Minister for Home Affairs and
                  Minister for Law
                </Card.Text>
                <Card.Text style={{ fontSize: "1.2rem" }}>4 Oct 2021</Card.Text>
              </Card.Body>
            </Card>
          </div>
          <div>
            <Card style={{ width: "20rem", height: "25rem", border: "none" }}>
              <Card.Body className="cardNews text-light">
                <Card.Title>GENERAL</Card.Title>
                <Card.Text style={{ fontSize: "1.2rem" }}>
                  Written Reply to Question for Oral Answer Not Answered by the
                  End of Question Time for Parliamentary Question on the
                  Considerations to Lower Voting Age To 18 in Singapore
                </Card.Text>
                <Card.Text style={{ fontSize: "1.2rem" }}>4 Oct 2021</Card.Text>
              </Card.Body>
            </Card>
          </div>
          <div>
            <Card style={{ width: "20rem", height: "25rem", border: "none" }}>
              <Card.Body className="cardNews text-light">
                <Card.Title>GENERAL</Card.Title>
                <Card.Text style={{ fontSize: "1.2rem" }}>
                  Written Answers to Questions for Oral Answer Not Answered by
                  the End of Question Time for Parliamentary Question on the
                  Restoration of Names to Registers of Electors
                </Card.Text>
                <Card.Text style={{ fontSize: "1.2rem" }}>
                  11 May 2021
                </Card.Text>
              </Card.Body>
            </Card>
          </div>
        </Stack>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
};

export default VoterHome;

{
  /* <div className="bg-light border">
<Card style={{ width: "30rem", height: "10rem" }}>
  <Card.Body className="cardBody">
    <Card.Title>Welcome to Mimi</Card.Title>
    <Card.Text style={{ fontSize: "1.5rem" }}>
      Please sign in to continue
    </Card.Text>
  </Card.Body>
</Card> */
}

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
