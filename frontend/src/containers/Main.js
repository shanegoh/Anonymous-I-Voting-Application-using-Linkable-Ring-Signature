import LoginButton from "../components/LoginButton.js";
import { Card } from "react-bootstrap";

export default function Main() {
  return (
    <div className="App-header">
      <Card className="cardHead">
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
}
