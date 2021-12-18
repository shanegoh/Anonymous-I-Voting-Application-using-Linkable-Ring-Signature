import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar.js";
import { DateTimePicker } from "react-rainbow-components";
import { Button, Form, Container } from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import { BiMinus } from "react-icons/bi";
import { nanoid } from "nanoid";
import axios from "axios";
import "../App.scss";

const initialStartDate = () => {
  var date = new Date();
  date.setSeconds(0);
  date.setMilliseconds(0);
  return date;
};

const initialEndDate = () => {
  var date = new Date();
  date.setHours(date.getHours() + 4);
  date.setSeconds(0);
  date.setMilliseconds(0);
  return date;
};

export default function EventForm({
  event_electionType,
  event_areaId,
  event_startDateTime,
  event_endDateTime,
  event_candidate,
}) {
  const [startDateTime, setStartDateTime] = useState(initialStartDate);
  const [endDateTime, setEndDateTime] = useState(initialEndDate);
  const [inputList, updateList] = useState([]); // Initial state of array

  const validateDateTime = () => {
    let result = endDateTime - startDateTime;

    if (result < 14400000) {
      console.log("Start and end date wrong");
      return false;
    } else return true;
  };

  const addCandidate = () => {
    updateList((inputList) => [
      ...inputList,
      [nanoid(), nanoid(), nanoid(), nanoid()],
    ]);
    // Array object consist of 3 unique id
  };

  const removeCandidate = (object) => {
    updateList((inputList) => inputList.filter((obj) => obj !== object));
    // delete the object
  };

  const [electionTypeList, setElectionTypeList] = useState([]);
  const [areaList, setAreaList] = useState([]);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/findAllElectionType`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setElectionTypeList((electionTypeList) => res.data[0]);
          setAreaList((areaList) => res.data[1]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <div className="d-flex gap-5 pt-4 align-items-center flex-column">
      <div className="d-flex gap-5 w-75">
        <Form.Select defaultValue={0} id="election_type">
          <option value="0" disabled>
            Select Parliamentary / Presidential
          </option>
          {electionTypeList.map(function (record) {
            return (
              <option key={record.election_id} value={record.election_id}>
                {record.election_name}
              </option>
            );
          })}
        </Form.Select>
        <Form.Select defaultValue={0} id="area">
          <option value="0" disabled>
            Select Area
          </option>
          {areaList.map(function (record) {
            return (
              <option key={record.area_id} value={record.area_id}>
                {record.area_name}
              </option>
            );
          })}
        </Form.Select>
      </div>
      <div className="d-flex gap-5 w-75">
        <DateTimePicker
          required
          value={startDateTime}
          id="datetimepicker-1"
          label="Start Date Time"
          formatStyle="large"
          onChange={(value) => setStartDateTime(value)}
          error={
            validateDateTime() === false ? "Start time should be earlier." : ""
          }
        />
        <DateTimePicker
          required
          value={endDateTime} // Default 4 hrs vote
          id="datetimepicker-1"
          label="End Date Time"
          formatStyle="large"
          onChange={(value) => setEndDateTime(value)}
          error={
            validateDateTime() === false ? "Start time should be earlier." : ""
          }
        />
      </div>
      <div className="w-75">
        <Container className="d-flex gap-3 align-items-center flex-column">
          <Form.Label className="fs-5 color-nav text-light w-100 text-center table-radius ">
            Candidates
          </Form.Label>
          {inputList.map((object) => (
            <div
              className="d-flex flex-row align-items-center gap-2"
              key={object[0]}
            >
              <Form.Control key={object[1]} type="file" />
              <Form.Control
                className="btn-success"
                style={{ width: "75%" }}
                key={object[2]}
                type="text"
                placeholder="Candidate Name"
              />
              <Button key={object[3]} onClick={() => removeCandidate(object)}>
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
      <Button disabled className="text-light" variant="danger">
        Create
      </Button>
    </div>
  );
}
