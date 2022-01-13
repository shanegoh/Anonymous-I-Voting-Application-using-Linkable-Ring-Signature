import React, { useEffect, useState } from "react";
import NavBar from "../../components/NavBar.js";
import { isAdmin, dateFormatForVoter, isDefined, INFO } from "../../util";
import { Redirect } from "react-router-dom";
import { Button, Alert, Spinner } from "react-bootstrap";
import axios from "axios";
import "../../App.scss";

export default function UpcomingElections({ history }) {
  const [recordJson, setRecordJson] = useState();
  const [isLoaded, setLoadStatus] = useState(false);
  const [msg, setMsg] = useState();
  const [btnStatus, setBtnStatus] = useState();
  const [isLoading, setLoadingStatus] = useState(true);

  useEffect(() => {
    axios
      .get("https://api.mimis.social/findElectionForVoter", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setRecordJson((recordJson) => res.data);
          setLoadStatus((isLoaded) => true);
          setLoadingStatus((isLoading) => false);
          let currentDateTime = new Date();
          let startDateTime = new Date(res.data.start_date_time);
          //If event is not yet started, grey out the button.
          if (currentDateTime < startDateTime)
            setBtnStatus((btnStatus) => true);
          else setBtnStatus((btnStatus) => false);
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err.response.data.message);
        setMsg((msg) => err.response.data.message);
        setLoadingStatus((isLoading) => false);
      });
  }, []);

  const pollEvent = (e) => {
    const event_id = e.currentTarget.id;
    console.log(event_id);
    let path = `/voter/poll/${event_id}`;
    history.push(path);
  };
  return !isAdmin() ? (
    <div>
      <NavBar />
      <div>
        <div className="d-flex flex-column gap-2 pt-2 align-items-center">
          <Alert className="btn-lg w-100 text-center text-light bg-black">
            Upcoming Election
          </Alert>
          {isLoaded ? (
            <Button
              key={recordJson.event_id}
              id={recordJson.event_id}
              className="btn-lg color-nav border-0 btn-hover-red admin-home-btn"
              disabled={btnStatus}
              onClick={(e) => pollEvent(e)}
            >
              {recordJson.area_name}
              <br />
              <small>
                {dateFormatForVoter(new Date(recordJson.start_date_time))}
              </small>
              &nbsp;-&nbsp;
              <small>
                {dateFormatForVoter(new Date(recordJson.end_date_time))}
              </small>
            </Button>
          ) : (
            <></>
          )}
          {isDefined(msg) ? (
            <Alert
              className="d-flex flex-column align-items-center text-dark"
              variant="info"
            >
              <b>{msg}</b>
            </Alert>
          ) : (
            <></>
          )}
          {isLoading ? (
            <>
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </>
          ) : (
            <></>
          )}
        </div>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
