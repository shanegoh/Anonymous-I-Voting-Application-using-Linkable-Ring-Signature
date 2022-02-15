import React from "react";
import { Card, Stack } from "react-bootstrap";
import "../App.scss";

export default function Media() {
  return (
    <div>
      <div className="div-nav">
        <Stack className="stack-align stackBody" direction="horizontal" gap={3}>
          <div>
            <Card className="cardMain border-0">
              <Card.Body className="cardNews text-light">
                <Card.Title className="cardTitle">GENERAL</Card.Title>
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
            <Card className="cardMain border-0">
              <Card.Body className="cardNews text-light">
                <Card.Title className="cardTitle">GENERAL</Card.Title>
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
            <Card className="cardMain border-0">
              <Card.Body className="cardNews text-light">
                <Card.Title className="cardTitle">GENERAL</Card.Title>
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
            <Card className="cardMain border-0">
              <Card.Body className="cardNews text-light">
                <Card.Title className="cardTitle">GENERAL</Card.Title>
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
  );
}
