import React, { useState, useEffect } from "react";
import NavBar from "../../components/NavBar.js";
import {
  Table,
  Form,
  Button,
  Modal,
  Accordion,
  Spinner,
} from "react-bootstrap";
import { Redirect, useParams } from "react-router-dom";
import AlertBox from "../../components/AlertBox.js";
import { ImBoxAdd } from "react-icons/im";
import { isAdmin, DANGER, isDefined } from "../../util";
import { FiCheck, FiX } from "react-icons/fi";
import { FcHighPriority } from "react-icons/fc";
import axios from "axios";
import "../../App.scss";

export default function Poll({ history }) {
  const { id } = useParams();
  const [selected, setSelected] = useState();
  const [candidateList, setCandidateList] = useState([]);
  const [privateKey, setPrivateKey] = useState();
  const [isLoaded, setLoadStatus] = useState(false);
  const [show, setShow] = useState(false); // Logic for displaying alert
  const handleShow = () => setShow(true); // Logic for displaying alert
  const handleDismiss = () => setShow(false); // Logic for closing alert
  const [errMsg, setErrMsg] = useState(); // Logic setting error msg
  const [err, setErr] = useState([]); // Logic for storing all error messages
  const [showModal, setShowModal] = useState(false);
  const handleCloseModal = () => setShowModal(false);
  const handleShowModal = () => setShowModal(true);
  const [btnStatus, setBtnStatus] = useState(false);

  const onSelectedChange = (e) => {
    console.log(e.target.id);
    setSelected((selected) => e.target.id);
  };

  const submitVote = () => {
    //clear error msg
    console.log(privateKey);
    setErr((err) => []);
    setErrMsg((errMsg) => "");
    handleDismiss();
    setBtnStatus((btnStatus) => true);
    handleCloseModal();
    var errors = [];

    // Check if candidate selected
    if (!isDefined(selected)) {
      errors.push("Please select a candidate.");
    }

    // Check if private key is not empty
    if (!isDefined(privateKey) || privateKey === "") {
      errors.push("Private Key cannot be empty.");
    }

    // Check if it is only digits
    if (!Number(privateKey)) {
      errors.push("Private Key contains only digits.");
    }
    // If there is error, display error
    if (errors.length > 0) {
      setErr((err) => errors);
      setBtnStatus((btnStatus) => false);
      handleShow();
    } else {
      const payload = {
        candidate_name: selected,
        event_id: id,
        private_key: privateKey,
      };
      console.log(payload);
      axios
        .put("/voteCandidate", payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
            id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
          },
        })
        .then((res) => {
          if (res.status === 200) {
            handleDismiss();
            console.log(res.data.message);
            let path = "/voter/myvotestatus";
            history.push(path);
          }
        })
        .catch((err) => {
          // Set error message
          console.log(err.response.data.message);
          setErrMsg((errMsg) => err.response.data.message);
          setBtnStatus((btnStatus) => false);
          handleShow();
        });
    }
  };

  useEffect(() => {
    axios
      .get(`/findCandidateByEventId/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setCandidateList((candidateList) => res.data);
          setLoadStatus((isLoaded) => true);
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err.response.data.message);
        // redirect user if candidate is not found( which means that event id is not found too)
        history.push("/voter/upcomingelections");
      });
  }, []);

  const updateKey = (e) => {
    setPrivateKey((privateKey) => e.target.value);
  };

  return !isAdmin() ? (
    <div>
      <NavBar />
      {showModal ? (
        <>
          <Modal show={showModal} onHide={handleCloseModal}>
            <Modal.Header>
              <Modal.Title>Vote Confirmation</Modal.Title>
            </Modal.Header>
            <Modal.Body>Are you sure?</Modal.Body>
            <Modal.Footer>
              <Button color="red" onClick={() => handleCloseModal()}>
                No, bring me back
              </Button>
              &nbsp;
              <Button variant="success" onClick={() => submitVote()}>
                Yes I am sure
              </Button>
            </Modal.Footer>
          </Modal>
        </>
      ) : (
        <></>
      )}
      {isLoaded ? (
        <div className="d-flex flex-column gap-2 pt-4 align-items-center">
          {show ? (
            <AlertBox
              err={err}
              setShow={setShow}
              errMsg={errMsg}
              variant={DANGER}
            />
          ) : (
            <></>
          )}
          <Accordion defaultActiveKey="0" className="w-50">
            <Accordion.Item eventKey="0">
              <Accordion.Header>
                <div className="text-success fs-3">
                  <FiCheck size={32} /> Do
                </div>
              </Accordion.Header>
              <Accordion.Body className="ajust-fs">
                <blockquote>
                  <li>
                    You are allowed to use your <b>smart phones or computers</b>
                    &nbsp;to vote.
                  </li>
                </blockquote>
                <blockquote>
                  <li>
                    Please select your choice by <b>tapping</b> or{" "}
                    <b>clicking</b> on the check box.
                  </li>
                </blockquote>
                <blockquote>
                  <li>
                    <b>Your vote is secret.</b> Please attempt your vote in a
                    secluded environment.
                  </li>
                </blockquote>
              </Accordion.Body>
            </Accordion.Item>
            <Accordion.Item eventKey="1">
              <Accordion.Header>
                <div className="text-danger fs-3">
                  <FiX size={32} /> Do NOT
                </div>
              </Accordion.Header>
              <Accordion.Body>
                <blockquote>
                  <li>
                    <b>Do not vote for any other person</b>. Impersonating
                    another voter is an offence.
                  </li>
                </blockquote>
                <blockquote>
                  <li>
                    <b>Do not avoid voting</b>. It is against the law for not
                    voting.
                  </li>
                </blockquote>
                <blockquote>
                  <li>
                    <b>Do not</b> try to find out how any other voter has voted
                    or intends to vote
                  </li>
                </blockquote>
              </Accordion.Body>
            </Accordion.Item>
            <Accordion.Item eventKey="2">
              <Accordion.Header>
                <div className="text-info fs-3">
                  <FcHighPriority /> &nbsp;PDPA Consent Clause
                </div>
              </Accordion.Header>
              <Accordion.Body>
                <blockquote>
                  The purpose of the collection of your vote are for election
                  purposes only. MiMi only uses the vote for vote tabulation and
                  will not disclose any vote information and personal data.
                </blockquote>
                <blockquote>
                  All information collected from voters will be kept protected.
                  MiMi shall not disclose any information without voter's
                  consent.
                </blockquote>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
          <Table className="w-25 text-center table-bordered table-radius">
            <thead className="color-nav text-light">
              <tr>
                <th colSpan="2">{Object.values(candidateList)[0].area_name}</th>
              </tr>
            </thead>
            <tbody style={{ height: "10rem" }}>
              {Object.values(candidateList).map((candidate) => {
                return (
                  <tr>
                    <td className="w-50">
                      <img
                        src={`data:image/png;base64,${candidate.candidate_image}`}
                        style={{ width: "5rem", height: "5rem" }}
                      />
                      <p>{candidate.candidate_name}</p>
                    </td>
                    <td className="w-50 ">
                      <Form.Check
                        id={candidate.candidate_name}
                        style={{ color: "red" }}
                        type="checkbox"
                        onChange={(e) => onSelectedChange(e)}
                        checked={
                          selected === candidate.candidate_name ? true : false
                        }
                      />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </Table>
          <Form.Control
            className="w-25"
            type="text"
            placeholder="Private Key"
            onChange={(e) => updateKey(e)}
          />
          <Button
            className="text-light"
            size="lg"
            variant="success"
            onClick={() => handleShowModal()}
            disabled={btnStatus ? true : false}
          >
            {btnStatus ? (
              <>
                <Spinner
                  as="span"
                  animation="grow"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />
                Loading...
              </>
            ) : (
              <>
                <ImBoxAdd />
                &nbsp; Vote
              </>
            )}
          </Button>
        </div>
      ) : (
        <div className="d-flex pt-4 justify-content-center">
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </div>
      )}
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
