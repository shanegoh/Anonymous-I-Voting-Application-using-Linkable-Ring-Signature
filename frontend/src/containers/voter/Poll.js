import React, { useState, useEffect } from "react";
import NavBar from "../../components/NavBar.js";
import { Table, Form, Button } from "react-bootstrap";
import { Redirect, useParams } from "react-router-dom";
import AlertBox from "../../components/AlertBox.js";
import { ImBoxAdd } from "react-icons/im";
import { isAdmin, DANGER, isDefined } from "../../util";
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

  const onSelectedChange = (e) => {
    console.log(e.target.id);
    setSelected((selected) => e.target.id);
  };

  const submitVote = () => {
    var errors = [];
    if (!isDefined(selected)) {
      errors.push("Please select a candidate.");
    }
    if (!isDefined(privateKey)) {
      errors.push("Private Key cannot be empty.");
    }
    // If there is error, display error
    if (errors.length > 0) {
      setErr((err) => errors);
      handleShow();
    } else {
      const payload = {
        candidate_name: selected,
        event_id: id,
        private_key: privateKey,
      };
      console.log(payload);
      axios
        .put(`http://localhost:5000/voteCandidate`, payload, {
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
          handleShow();
        });
    }
  };

  useEffect(() => {
    axios
      .get(`http://localhost:5000/findCandidateByEventId/${id}`, {
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
      });
  }, []);

  const updateKey = (e) => {
    setPrivateKey((privateKey) => e.target.value);
  };

  return !isAdmin() ? (
    <div>
      <NavBar />
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
            onClick={() => submitVote()}
          >
            <ImBoxAdd />
            &nbsp; Vote
          </Button>
        </div>
      ) : (
        <></>
      )}
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
