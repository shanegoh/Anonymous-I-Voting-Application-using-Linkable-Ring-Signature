import React, { useState, useEffect } from "react";
import { Button, Form, Container, Modal } from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import { BiMinus } from "react-icons/bi";
import { isDefined } from "../util";
import { nanoid } from "nanoid";
import axios from "axios";
import "../App.scss";

const EMPTYSTRING = () => "";
export default function Candidate({
  event_id,
  event_candidate,
  submitCandidateToParent, // candidate list to be send back to parent component(EventForm)
}) {
  const [show, setShow] = useState(false); // For storing the state of Modal
  const handleClose = () => setShow(false); // For dismissing Modal
  const handleShow = () => setShow(true); // For displaying Modal
  const [inputList, updateList] = useState([]); // Initial state of array of candidate

  useEffect(() => {
    // If it's defined means that the action is editing and not creating,
    // need to set retrieve data
    // Skip if user is creating
    if (isDefined(event_candidate))
      updateCandidateList(JSON.parse(event_candidate));
  }, []);

  const addCandidate = () => {
    updateList((inputList) => [
      ...inputList,
      [nanoid(), nanoid(), nanoid(), EMPTYSTRING, EMPTYSTRING],
    ]);
    // Array object consist of 3 unique id for react to idenfity object '
    //and last 2 attributes for image and name
  };

  const updateCandidateList = (candidateList) => {
    //{"candidates": [{"name": "PAP", "image": "../../imgMiMi.png"}, {"name": "WP", "image": "../../imgMiMi.png"}]}
    Object.values(candidateList).map((candidate) => {
      candidate.map((object) => {
        updateList((inputList) => [
          ...inputList,
          [nanoid(), nanoid(), nanoid(), object.image_location, object.name],
        ]);
      });
    });
  };

  // delete the candidate object
  const removeCandidate = (object) => {
    updateList((inputList) => inputList.filter((obj) => obj !== object));
  };

  // On change update name using dom id
  const updateName = (e) => {
    const key = e.target.id;
    const name = e.target.value;
    inputList.forEach((object) => {
      // object[1] is candidate name field
      if (object[1] === key) {
        object[4] = name;
        object[3] = "MiMi.png";
      }
    });
  };

  const deleteEvent = () => {
    const event_id_payload = { event_id: event_id };
    axios
      .post("/deleteEventById", event_id_payload, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <>
      <div className="w-75">
        <Container className="d-flex gap-3 align-items-center flex-column">
          <Form.Label className="fs-5 color-nav text-light w-100 text-center table-radius ">
            Candidates
          </Form.Label>
          {inputList.map((object) => (
            <div className="d-flex flex-row align-items-center gap-2">
              <Form.Control key={object[0]} type="file" />
              <Form.Control
                key={object[1]}
                className="btn-success"
                id={object[1]}
                style={{ width: "75%" }}
                type="text"
                placeholder="Candidate Name"
                defaultValue={
                  typeof event_candidate === "undefined" ? "" : object[4]
                }
                onChange={(e) => updateName(e)}
              />
              <Button key={object[2]} onClick={() => removeCandidate(object)}>
                <BiMinus className="fs-3" />
              </Button>
            </div>
          ))}
          <Button
            className="btn-circle btn-success"
            id={inputList.length}
            onClick={addCandidate}
          >
            <BsPlusLg className="fs-3" />
          </Button>
        </Container>
      </div>
      <div className="d-flex gap-3">
        <Button
          className="text-light"
          variant="primary"
          onClick={() => submitCandidateToParent(inputList)}
        >
          Create
        </Button>
        {typeof event_candidate === "undefined" ? (
          <></>
        ) : (
          <Button className="text-light" variant="danger" onClick={handleShow}>
            Delete
          </Button>
        )}
      </div>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Are you absolutely sure?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          This action cannot be undone. This will permanently delete the event.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleClose}>
            Nevermind, bring me back
          </Button>
          <Button variant="danger text-light" onClick={deleteEvent}>
            Yes, I'm sure
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
