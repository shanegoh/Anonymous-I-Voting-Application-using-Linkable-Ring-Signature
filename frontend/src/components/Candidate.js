import React, { useState, useEffect } from "react";
import { Button, Form, Container, Modal } from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import { BiMinus } from "react-icons/bi";
import { nanoid } from "nanoid";
import axios from "axios";
import "../App.scss";

export default function Candidate({ event_id, event_candidate }) {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [inputList, updateList] = useState([]); // Initial state of array of candidate
  const [candidate, setCandidate] = useState({});

  useEffect(() => {
    if (typeof event_candidate !== "undefined") {
      setCandidate((candidate) => JSON.parse(event_candidate));
      updateCandidateList(JSON.parse(event_candidate));
    }
  }, []);

  const addCandidate = () => {
    updateList((inputList) => [
      ...inputList,
      [nanoid(), nanoid(), nanoid(), "", ""],
    ]);
    // Array object consist of 3 unique id
  };

  const updateCandidateList = (candidateList) => {
    console.log("Working");
    Object.values(candidateList).map((candidate, i) => {
      candidate.map((object) => {
        updateList((inputList) => [
          ...inputList,
          [nanoid(), nanoid(), nanoid(), object.image_location, object.name],
        ]);
      });
    });
  };

  const removeCandidate = (object) => {
    updateList((inputList) => inputList.filter((obj) => obj !== object));
    // delete the object
  };

  //   const updateName = (e) => {
  //     var key = e.currentTarget.key;
  //     var name = e.currentTarget.name;
  //     inputList.forEach((object) => {
  //       if (object.key === key) {
  //         object.name = name;
  //       }
  //     });
  //   };
  const deleteEvent = () => {
    axios
      .post("/deleteEventById", {
        data: { event_id: event_id },
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
                className="btn-success"
                style={{ width: "75%" }}
                type="text"
                placeholder={"Candidate Name"}
                defaultValue={
                  typeof event_candidate === "undefined" ? "" : object[4]
                }
                key={object[1]}
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
        <Button className="text-light" variant="primary">
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
