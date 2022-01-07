import React, { useEffect, useState } from "react";
import { isAdmin, axiosConfig } from "../../util";
import { Redirect, useParams } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import EventForm from "../../components/EventForm.js";
import axios from "axios";
import "../../App.scss";

export default function EditElection({ history }) {
  // Event id
  const { id } = useParams();

  const [electionType, setElectionType] = useState();
  const [areaId, setAreaId] = useState();
  const [startDateTime, setStartDateTime] = useState();
  const [endDateTime, setEndDateTime] = useState();
  const [candidate, setCandidate] = useState([]);
  const [isLoaded, setLoadStatus] = useState(false);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/findEventById/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          setElectionType((electionType) => res.data[0].election_type);
          setAreaId((areaId) => res.data[0].area_id);
          setStartDateTime((startDateTime) => res.data[0].start_date_time);
          setEndDateTime((endDateTime) => res.data[0].end_date_time);
          setCandidate((candidate) => res.data[0].candidates);
          setLoadStatus((isLoaded) => true);
        }
      })
      .catch((err) => {
        console.log(err.response.data.message);
        history.push("/admin/home");
      });
  }, []);

  return isAdmin() ? (
    <div>
      <NavBar />
      {isLoaded ? (
        <EventForm
          event_id={id}
          event_electionType={electionType}
          event_areaId={areaId}
          event_startDateTime={startDateTime}
          event_endDateTime={endDateTime}
          event_candidate={candidate}
          history={history}
        />
      ) : (
        <></>
      )}
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
