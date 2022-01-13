import React, { useState, useEffect } from "react";
import {
  Button,
  Form,
  Container,
  Modal,
  OverlayTrigger,
  Tooltip,
} from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import { BiMinus } from "react-icons/bi";
import { isDefined, imageType, imageHeader } from "../util";
import { nanoid } from "nanoid";
import axios from "axios";
import "../App.scss";

const EMPTYSTRING = "";
export default function Candidate({
  event_id,
  event_candidate,
  submitCandidateToParent, // candidate list to be send back to parent component(EventForm)
  submitResponseToParent, // error message to be send back to parent component(EventForm)
  history,
}) {
  const [show, setShow] = useState(false); // For storing the state of Modal
  const handleClose = () => setShow(false); // For dismissing Modal
  const handleShow = () => setShow(true); // For displaying Modal
  const [inputList, updateList] = useState([]); // Initial state of array of candidate

  useEffect(() => {
    // If it's defined means that the action is editing and not creating,
    // need to set retrieve data
    // Skip if user is creating
    console.log(event_candidate);
    if (isDefined(event_candidate)) updateCandidateList(event_candidate);
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
    candidateList.forEach((candidate) => {
      updateList((inputList) => [
        ...inputList,
        [
          nanoid(),
          nanoid(),
          nanoid(),
          imageHeader + candidate.candidate_image,
          candidate.candidate_name,
        ], // might need to fix
      ]);
    });
  };

  // delete the candidate object
  const removeCandidate = (object) => {
    updateList((inputList) => inputList.filter((obj) => obj !== object));
  };

  // On change update name using dom id
  const updateName = (e) => {
    const key = e.target.id;
    inputList.forEach((object) => {
      // object[1] is candidate name field
      if (object[1] === key) {
        object[4] = e.target.value;
      }
    });
  };

  // On change update image file using dom id
  const updateImage = (e) => {
    const key = e.target.id;
    // Check image type
    if (e.target.files[0].type === imageType) {
      inputList.forEach((object) => {
        // object[1] is candidate name field
        if (object[1] === key) {
          getBase64(e.target.files[0], (result) => {
            console.log(e.target.files[0].name);
            console.log(result);
            object[3] = result;
          });
        }
      });
    } else {
      submitResponseToParent("Image type must be .png");
    }
  };

  const getBase64 = (file, cb) => {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      cb(reader.result);
    };
    reader.onerror = function (error) {
      console.log("Error: ", error);
    };
  };

  const deleteEvent = () => {
    handleClose(); // Close the confirmation dialog
    // const event_id_payload = { event_id: event_id };
    axios
      .delete(`https://api.mimis.social/deleteEventById/${event_id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          IdToken: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          history.push("/admin/home");
        }
      })
      .catch((err) => {
        console.log(err.response.data);
        submitResponseToParent(err.response.data.message);
      });
  };

  return (
    <>
      <div className="w-75">
        <Container className="d-flex gap-3 align-items-center flex-column ">
          <Form.Label className="fs-5 color-nav text-light w-100 text-center table-radius ">
            Candidates
          </Form.Label>
          {inputList.map((object) => (
            <div className="d-flex flex-row align-items-center gap-2">
              <OverlayTrigger
                key={nanoid()}
                placement={"left"}
                overlay={
                  <Tooltip id={nanoid()} style={{ margin: 0 }}>
                    <strong>Only .png file are allowed.</strong>
                  </Tooltip>
                }
              >
                <Form.Control
                  style={isDefined(event_id) ? { display: "none" } : {}}
                  key={object[0]}
                  id={object[1]}
                  type="file"
                  accept=".png"
                  onChange={(e) => updateImage(e)}
                />
              </OverlayTrigger>
              <OverlayTrigger
                key={nanoid()}
                placement={"left"}
                overlay={
                  <Tooltip id={nanoid()} style={{ margin: 0 }}>
                    <strong>Upload again to replace image.</strong>
                  </Tooltip>
                }
              >
                <Form.Label
                  style={!isDefined(event_id) ? { display: "none" } : {}}
                  for={object[1]}
                  className="bg-secondary btn-hover-red text-light text-center w-100 btn-radius "
                >
                  Upload New Image
                </Form.Label>
              </OverlayTrigger>
              <Form.Control
                key={object[1]}
                id={object[1]}
                style={{ width: "75%" }}
                type="text"
                placeholder="Candidate Name"
                defaultValue={
                  typeof event_candidate === "undefined" ? "" : object[4]
                }
                onChange={(e) => updateName(e)}
              />
              <Button
                className="color-nav border-0"
                key={object[2]}
                onClick={() => removeCandidate(object)}
              >
                <BiMinus className="fs-3" />
              </Button>
            </div>
          ))}
          <Button
            className="btn-circle color-nav border-0 btn-hover-green"
            id={inputList.length}
            onClick={addCandidate}
          >
            <BsPlusLg className="fs-3" />
          </Button>
        </Container>
      </div>
      <div className="d-flex gap-3">
        <Button
          variant="success"
          onClick={() => submitCandidateToParent(inputList)}
        >
          {typeof event_id === "undefined" ? "Create" : "Update"}
        </Button>
        {typeof event_candidate === "undefined" ? (
          <></>
        ) : (
          <Button
            className="text-light color-red"
            variant="danger"
            onClick={handleShow}
          >
            Delete
          </Button>
        )}
      </div>
      {/* re structure the delete code here to eventform */}
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Are you absolutely sure?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          This action cannot be undone. This will permanently delete the event.
        </Modal.Body>
        <Modal.Footer>
          <Button className="color-nav border-0" onClick={handleClose}>
            Nevermind, bring me back
          </Button>
          <Button className="color-red border-0" onClick={deleteEvent}>
            Yes, I'm sure
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
