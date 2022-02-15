import React, { useState, useEffect } from "react";
import { DateTimePicker } from "react-rainbow-components";
import { Form } from "react-bootstrap";
import Candidate from "./Candidate.js";
import {
  isDefined,
  DEFAULTSELECTOR,
  DANGER,
  SUCCESS,
  addMinutes,
} from "../util";
import AlertBox from "./AlertBox.js";
import axios from "axios";
import "../App.scss";

// Initial start date is current date
const initialStartDate = () => {
  var date = new Date();
  date.setSeconds(0);
  date.setMilliseconds(0);
  date = addMinutes(date);
  return date;
};

// Initial end date is current date + 4 hours
const initialEndDate = () => {
  var date = new Date();
  date.setHours(date.getHours() + 4);
  date = addMinutes(date);
  date.setSeconds(0);
  date.setMilliseconds(0);
  return date;
};

export default function EventForm({
  event_id,
  event_electionType,
  event_areaId,
  event_startDateTime,
  event_endDateTime,
  event_candidate,
  history,
}) {
  // Constant value for default value
  const [startDateTime, setStartDateTime] = useState(initialStartDate); //Initial Start Date
  const [endDateTime, setEndDateTime] = useState(initialEndDate); //Initial End Date
  const [electionType, setElectionType] = useState(DEFAULTSELECTOR); //Initial default value electionType
  const [areaId, setAreaId] = useState(DEFAULTSELECTOR); //Initial default value Area
  const [electionTypeList, setElectionTypeList] = useState([]); //Initial state of election type list
  const [areaList, setAreaList] = useState([]); //Initial state of area list ( from server)
  const [filteredAreaList, setFilteredAreaList] = useState([]); // For filtering display of areas base on selection
  const [show, setShow] = useState(false); // Logic for displaying alert
  const handleShow = () => setShow(true); // Logic for displaying alert
  const handleDismiss = () => setShow(false); // Logic for closing alert
  const [err, setErr] = useState([]); // Logic for storing all error messages
  const [errMsg, setErrMsg] = useState();
  const [variant, setVariant] = useState();
  const [invalidSelectA, setInvalidSelectA] = useState(false);
  const [invalidSelectB, setInvalidSelectB] = useState(false);
  const format = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

  // Validate if the time difference is at least 4 hours
  const validateDateTime = () => {
    const result = endDateTime - startDateTime;
    return result >= 14400000 ? true : false;
  };

  // On change, update the election_type id
  const updateElectionType = (e) => {
    const value = e.currentTarget.value;
    setElectionType((electionType) => value);
    setAreaId((areaId) => "DEFAULT");
    // Filter the original area list to the filtered area list
    setFilteredAreaList((filteredAreaList) =>
      areaList.filter((object) => object.election_type == value)
    );
  };

  // On change, update the area id
  const updateAreaId = (e) => {
    const value = e.currentTarget.value;
    setAreaId((areaId) => value);
  };

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_PATH + "/findAllElectionTypeAndArea", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          // Set election type list and area list
          setElectionTypeList((electionTypeList) => res.data[0]);
          setAreaList((areaList) => res.data[1]);
          setFilteredAreaList((filteredAreaList) => res.data[1]);
        }
      })
      .catch((err) => {
        console.log(err);
      });

    // If it's defined means that the action is editing and not creating,
    // need to set retrieve data
    // Skip if user is creating
    if (isDefined(event_startDateTime) && isDefined(event_endDateTime)) {
      setStartDateTime((startDateTime) => new Date(event_startDateTime));
      setEndDateTime((endDateTime) => new Date(event_endDateTime));
      setElectionType((electionType) => event_electionType);
      setAreaId((areaId) => event_areaId);
    }
  }, []);

  // On click submit, validate input and post to server
  const submitEvent = (list) => {
    window.scrollTo(0, 0);
    var errors = [];
    setErrMsg((errMsg) => "");
    // Convert candidates to json data in array
    var jsonArray = [];
    list.map((object) => {
      let tmpData = { candidate_name: object[4], candidate_image: object[3] };
      jsonArray.push(tmpData);
    });
    console.log(jsonArray);

    // Validate if start date time is in future
    if (new Date(startDateTime) < new Date()) {
      errors.push("*Start date time must be in the future");
    }

    // Validate election type field
    if (electionType === DEFAULTSELECTOR) {
      errors.push("*Required election type");
      setInvalidSelectA((invalidSelectA) => true);
    }

    // Validate area field
    if (areaId === DEFAULTSELECTOR) {
      errors.push("*Required an Area");
      setInvalidSelectB((invalidSelectB) => true);
    }

    // Validate number of candidate
    if (jsonArray.length < 2) {
      errors.push("*Insufficient Candidate");
    }
    // Validate information of condidate
    for (let x = 0; x < jsonArray.length; x++) {
      if (
        jsonArray[x].candidate_name.length === 0 ||
        jsonArray[x].candidate_image.length === 0
      ) {
        console.log(jsonArray[x].candidate_image.length);
        errors.push("*Required Candidate image and name");
        break;
      }
      // Validate candidate name
      if (format.test(jsonArray[x].candidate_name)) {
        errors.push("*Invalid candidate name. No special characters allowed.");
        break;
      }
    }
    // Validate the duration of the time
    if (!validateDateTime()) {
      errors.push("*Duration of the event must be at least 4 hours");
    }
    console.log(err);
    // Show the Alert Box if there is error, else close and post data
    if (errors.length > 0) {
      setErr((err) => errors);

      setVariant((variant) => DANGER);
      handleShow(); // Display alert box
    } else {
      handleDismiss(); // Close alert box
      setErr((err) => []); // Clear error msg if ok
      // Craft json payload
      var event_payload = {
        election_type: electionType,
        area_id: areaId,
        start_date_time: startDateTime,
        end_date_time: endDateTime,
        candidates: jsonArray,
      };
      console.log(event_payload);

      // Update Event if event_id is defined, else create
      var url_update = process.env.REACT_APP_PATH + `/updateEvent/${event_id}`;
      var url_create = process.env.REACT_APP_PATH + "/createEvent";
      // If event_id is defined = update event
      var path = isDefined(event_id) ? url_update : url_create;
      axios
        .put(path, event_payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          },
        })
        .then((res) => {
          if (res.status === 200 || res.status === 201) {
            console.log(res);
            setErrMsg((errMsg) => res.data.message);
            setVariant((variant) => SUCCESS);
            handleShow(); // Display alert
          }
        })
        .catch((err) => {
          // Set error message
          console.log(err.response.data.message);
          if (new Date(event_startDateTime) < new Date()) {
            setTimeout(() => {
              setErrMsg((errMsg) => err.response.data.message);
              setVariant((variant) => DANGER);
              handleShow(); // Display alert
              history.push("/admin/home");
            }, 2000);
          } else {
            setErrMsg((errMsg) => err.response.data.message);
            setVariant((variant) => DANGER);
            handleShow(); // Display alert
          }
        });
    }
  };

  // Display alert box when fail to delete event
  const displayResponse = (message) => {
    setErrMsg((errMsg) => message);
    setVariant((variant) => DANGER);
    handleShow();
    setTimeout(() => {
      history.push("/admin/home");
    }, 2000);
  };

  return (
    <div
      className="d-flex gap-5 align-items-center flex-column mb-5"
      style={{ paddingTop: "6rem" }}
    >
      {show ? (
        <AlertBox
          err={err}
          setShow={setShow}
          errMsg={errMsg}
          variant={variant}
        />
      ) : (
        <></>
      )}
      <div className="d-flex gap-5 form-element-resize">
        <div className="d-flex flex-column form-element-resize">
          <Form.Select
            value={electionType}
            id="election_type"
            disabled={isDefined(event_id)}
            onChange={(e) => updateElectionType(e)}
            required
            isInvalid={invalidSelectA}
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
          <div
            class="invalid-feedback text-center"
            style={{ display: invalidSelectA == false ? "none" : "block" }}
          >
            *Please select
          </div>
        </div>
        <div className="d-flex flex-column form-element-resize">
          <Form.Select
            value={areaId}
            id="area"
            disabled={isDefined(event_id)}
            onChange={(e) => updateAreaId(e)}
            isInvalid={invalidSelectB}
          >
            <option value="DEFAULT" disabled>
              Select Area
            </option>
            {filteredAreaList.map(function (record) {
              return (
                <option key={record.area_id} value={record.area_id}>
                  {record.area_name}
                </option>
              );
            })}
          </Form.Select>
          <div
            class="invalid-feedback text-center"
            style={{ display: invalidSelectB == false ? "none" : "block" }}
          >
            *Please select
          </div>
        </div>
      </div>
      <div className="d-flex gap-5 form-element-resize">
        <DateTimePicker
          required
          value={startDateTime}
          id="start"
          label="Start Date Time"
          formatStyle="large"
          minDate={initialStartDate()}
          onChange={(value) => setStartDateTime((startDateTime) => value)}
          error={
            validateDateTime() === false
              ? "*Start time should be at least 4 hours earlier."
              : ""
          }
        />
        <DateTimePicker
          required
          value={endDateTime} // Default 4 hrs vote
          id="end"
          label="End Date Time"
          formatStyle="large"
          minDate={initialStartDate()}
          onChange={(value) => setEndDateTime((setEndDateTime) => value)}
          error={
            validateDateTime() === false
              ? "*End time should be at least 4 hours later."
              : ""
          }
        />
      </div>
      <Candidate
        event_candidate={event_candidate}
        event_id={event_id}
        submitCandidateToParent={submitEvent}
        submitResponseToParent={displayResponse}
        history={history}
      />
    </div>
  );
}
