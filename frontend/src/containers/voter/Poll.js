import React, { useState, useEffect } from "react";
import NavBar from "../../components/NavBar.js";
import {
  Table,
  Form,
  Button,
  Modal,
  Spinner,
  InputGroup,
} from "react-bootstrap";
import { Redirect, useParams } from "react-router-dom";
import AlertBox from "../../components/AlertBox.js";
import { ImBoxAdd } from "react-icons/im";
import { isAdmin, DANGER, isDefined, hasToken } from "../../util";
import { FiCheck, FiX } from "react-icons/fi";
import { FcHighPriority } from "react-icons/fc";
import ReCAPTCHA from "react-google-recaptcha";
import { FaPaste } from "react-icons/fa";
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
  const [btnStatus, setBtnStatus] = useState(true);
  const [submitStatus, setsubmitStatus] = useState(false);
  const [isKeyInValid, setIsKeyInValid] = useState(false);
  const [showInfo, setShowInfo] = useState(true);
  const handleCloseInfo = () => setShowInfo(false);

  const onSelectedChange = (e) => {
    console.log(e.target.id);
    setSelected((selected) => e.target.id);
  };

  const submitVote = () => {
    window.scrollTo(0, 0);
    setsubmitStatus((submitStatus) => true);
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
      errors.push("Required candidate.");
    }

    // Check if private key is not empty
    if (!isDefined(privateKey) || privateKey === "") {
      errors.push("Required private key");
      setIsKeyInValid((isKeyValid) => true);
    } else if (!Number(privateKey)) {
      // Check if it is only digits
      errors.push("Invalid private key");
      setIsKeyInValid((isKeyValid) => true);
    }

    // If there is error, display error
    if (errors.length > 0) {
      setErr((err) => errors);
      setBtnStatus((btnStatus) => false);
      setsubmitStatus((submitStatus) => false);
      handleShow();
    } else {
      const payload = {
        candidate_name: selected,
        event_id: id,
        private_key: privateKey,
      };
      console.log(payload);
      axios
        .put(process.env.REACT_APP_PATH + "/voteCandidate", payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
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
          setsubmitStatus((submitStatus) => false);
          handleShow();
        });
    }
  };

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_PATH + `/findCandidateByEventId/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
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
        // console.log(err.response.data.message);
        // redirect user if candidate is not found( which means that event id is not found too)
        window.history.back();
      });
  }, []);

  const updateKey = (e) => {
    setPrivateKey((privateKey) => e.target.value);
  };

  const verifiedCaptcha = () => {
    console.log("ok");
    setBtnStatus((btnStatus) => false);
  };

  const readText = () => {
    navigator.clipboard
      .readText()
      .then((text) => {
        setPrivateKey((privateKey) => text);
        console.log("Pasted content: ", text);
      })
      .catch((err) => {
        console.error("Failed to read clipboard contents: ", err);
      });
  };

  return !isAdmin() && hasToken() ? (
    <div className="pd pb-5">
      <NavBar />
      <Modal show={showInfo} closeOnOverlayClick={false}>
        <Modal.Header className="color-nav text-light">
          <Modal.Title>Instructions</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="dos ">
            <div className="fs-3 text-center">
              <FiCheck size={32} /> Do
            </div>
            <blockquote>
              <li>
                <small>
                  You are allowed to use your <b>smart phones or computers</b>
                  &nbsp;to vote.
                </small>
              </li>
            </blockquote>
            <blockquote>
              <li>
                <small>
                  Please select your choice by <b>tapping</b> or <b>clicking</b>{" "}
                  on the check box.
                </small>
              </li>
            </blockquote>
            <blockquote>
              <li>
                <small>
                  <b>Your vote is secret.</b> Attempt your vote in a secluded
                  environment.
                </small>
              </li>
            </blockquote>
          </div>
          <div className="donts">
            <div className="text-danger fs-3 text-center">
              <FiX size={32} /> Do Not
            </div>
            <blockquote>
              <li>
                <small>
                  <b>Do not vote for any other person</b>. Impersonating another
                  voter is an offence.
                </small>
              </li>
            </blockquote>
            <blockquote>
              <li>
                <small>
                  <b>Do not avoid voting</b>. It is against the law for not
                  voting.
                </small>
              </li>
            </blockquote>
            <blockquote>
              <li>
                <small>
                  <b>Do not</b> try to find out how any other voter has voted or
                  intends to vote.
                </small>
              </li>
            </blockquote>
          </div>
          <div className="pdpas">
            <div className="text-info fs-3 text-center">
              <FcHighPriority /> &nbsp;PDPA Consent Clause
            </div>
            <blockquote>
              The purpose of the collection of your vote are for election
              purposes only. MiMi only uses the vote for vote tabulation and
              will not disclose any vote information and personal data.
            </blockquote>
            <blockquote>
              All information collected from voters will be kept protected. MiMi
              will not disclose any information without voter's consent.
            </blockquote>
          </div>
        </Modal.Body>
        <Modal.Footer className="justify-content-center">
          <Button variant="success text-light" onClick={handleCloseInfo}>
            Yes, I understand and agree.
          </Button>
        </Modal.Footer>
      </Modal>
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
          <Table className="poll-width text-center table-radius">
            <thead className="color-nav text-light">
              <tr>
                <th colSpan="2">{Object.values(candidateList)[0].area_name}</th>
              </tr>
            </thead>
            <tbody style={{ height: "10rem" }}>
              {Object.values(candidateList).map((candidate) => {
                return (
                  <tr>
                    <td>
                      <img
                        src={`data:image/png;base64,${candidate.candidate_image}`}
                        style={{ width: "5rem", height: "5rem" }}
                      />
                      <p>{candidate.candidate_name}</p>
                    </td>
                    <td>
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
          <InputGroup hasValidation className="poll-width gap-1">
            <Form.Control
              value={privateKey}
              type="text"
              placeholder="Private Key"
              onChange={(e) => updateKey(e)}
              isInvalid={isKeyInValid}
            />
            <Button size="sm" onClick={() => readText()} className="color-nav">
              <FaPaste />
            </Button>
            <Form.Control.Feedback type="invalid" className="text-center">
              *Valid Key Required*
            </Form.Control.Feedback>
          </InputGroup>
          <ReCAPTCHA
            sitekey="6LfmOCYeAAAAAMUmQnR5ROcvnYv0Jcoh0FxgkDbU"
            className="g-recaptcha"
            onChange={() => verifiedCaptcha()}
          />
          <Button
            className="text-light poll-width"
            size="lg"
            variant="success"
            onClick={() => handleShowModal()}
            disabled={btnStatus ? true : false}
          >
            {submitStatus ? (
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
