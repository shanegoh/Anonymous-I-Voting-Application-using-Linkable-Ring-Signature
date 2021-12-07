import react from "react";
import LoginButton from "../components/LoginButton.js";
import { Card } from "react-bootstrap";
import logo from "../img/MiMi.png";

const Main = () => {
  return (
    <div className="App-header">
      <Card style={{ width: "30rem", height: "10rem" }}>
        <Card.Body className="cardBody">
          <Card.Title>Welcome to Mimi</Card.Title>
          <Card.Text style={{ fontSize: "1.5rem" }}>
            Please sign in to continue
          </Card.Text>
          <LoginButton />
        </Card.Body>
      </Card>
    </div>
  );
};

export default Main;
