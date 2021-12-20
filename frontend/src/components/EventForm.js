import React, { useState, useEffect } from "react";
import { DateTimePicker } from "react-rainbow-components";
import { Form } from "react-bootstrap";
import axios from "axios";
import "../App.scss";
import Candidate from "./Candidate.js";
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

const DEFAULTSELECTOR = () => {
  return "DEFAULT";
};

export default function EventForm({
  event_id,
  event_electionType,
  event_areaId,
  event_startDateTime,
  event_endDateTime,
  event_candidate,
}) {
  const [startDateTime, setStartDateTime] = useState(initialStartDate); //Initial Start Date
  const [endDateTime, setEndDateTime] = useState(initialEndDate); //Initial End Date
  const [electionType, setElectionType] = useState(DEFAULTSELECTOR); //Initial electionType
  const [areaId, setAreaId] = useState(DEFAULTSELECTOR); //Initial Area
  const [electionTypeList, setElectionTypeList] = useState([]); //Initial state of election type list
  const [areaList, setAreaList] = useState([]); //Initial state of area list

  const validateDateTime = () => {
    let result = endDateTime - startDateTime;

    if (result < 14400000) {
      console.log("Start and end date wrong");
      return false;
    } else return true;
  };

  useEffect(() => {
    axios
      .get("/findAllElectionType", {
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

    // Need to specific undefined then dont load.
    // If it's not undefined means that the action is editing and not creating
    if (
      typeof event_startDateTime !== "undefined" &&
      typeof event_endDateTime !== "undefined"
    ) {
      setStartDateTime((startDateTime) => new Date(event_startDateTime));
      setEndDateTime((endDateTime) => new Date(event_endDateTime));
      setElectionType((electionType) => event_electionType);
      setAreaId((areaId) => event_areaId);
    }
  }, []);

  const updateElectionType = (e) => {
    console.log(e.currentTarget.value);
    var value = e.currentTarget.value;
    setElectionType((electionType) => value);
  };

  const updateAreaId = (e) => {
    console.log(e.currentTarget.value);
    var value = e.currentTarget.value;
    setAreaId((areaId) => value);
  };

  return (
    <div className="d-flex gap-5 pt-4 align-items-center flex-column">
      <div className="d-flex gap-5 w-75">
        <Form.Select
          value={electionType}
          id="election_type"
          onChange={(e) => updateElectionType(e)}
        >
          <option value="DEFAULT" disabled>
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
        <Form.Select value={areaId} id="area" onChange={(e) => updateAreaId(e)}>
          <option value="DEFAULT" disabled>
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
          id="start"
          label="Start Date Time"
          formatStyle="large"
          onChange={(value) => setStartDateTime((startDateTime) => value)}
          error={
            validateDateTime() === false ? "Start time should be earlier." : ""
          }
        />
        <DateTimePicker
          required
          value={endDateTime} // Default 4 hrs vote
          id="end"
          label="End Date Time"
          formatStyle="large"
          onChange={(value) => setEndDateTime((setEndDateTime) => value)}
          error={
            validateDateTime() === false ? "End time should be later." : ""
          }
        />
      </div>
      <Candidate event_candidate={event_candidate} event_id={event_id} />
    </div>
  );
}
