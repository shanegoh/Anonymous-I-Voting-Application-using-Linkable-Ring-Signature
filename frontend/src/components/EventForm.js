import React, { useState } from "react";
import NavBar from "../components/NavBar.js";
import { DateTimePicker } from "react-rainbow-components";
import { Button, Form, Container } from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import { BiMinus } from "react-icons/bi";
import { nanoid } from "nanoid";
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

export default function EventForm() {
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
  return (
    <div className="d-flex gap-5 pt-4 align-items-center flex-column">
      <div className="d-flex gap-5 w-75">
        <Form.Select id="election_type">
          <option disabled>Select Parliamentary / Presidential</option>
          <option value="0">Group Representation Constituency(GRC)</option>
          <option value="1">Single Member Constituency(SMC)</option>
          <option value="2">Presidential Election(PE)</option>
        </Form.Select>
        <Form.Select id="area">
          <option disabled>Select</option>
          <option value="0">Seng Kang GRC</option>
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
