import React, { useEffect, useState } from "react";
import NavBar from "../../components/NavBar.js";
import { isAdmin, dateFormatForVoter } from "../../util";
import { Redirect } from "react-router-dom";
import { Button } from "react-bootstrap";
import axios from "axios";
import "../../App.scss";

export default function UpcomingElections({ history }) {
  const [recordJson, setRecordJson] = useState();
  const [isLoaded, setLoadStatus] = useState(false);
  useEffect(() => {
    axios
      .get(`http://localhost:5000/findElectionForVoter`, {
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
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err.response.message);
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
      {isLoaded ? (
        <div className="d-flex flex-column gap-2 pt-4 align-items-center">
          <Button
            key={recordJson.event_id}
            id={recordJson.event_id}
            className="btn-lg color-nav border-0 btn-hover-red admin-home-btn"
            active
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
        </div>
      ) : (
        <></>
      )}
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
