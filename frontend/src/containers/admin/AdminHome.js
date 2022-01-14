import React, { useEffect, useState } from "react";
import { isAdmin, dateFormat } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Button, Alert, Spinner } from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import axios from "axios";
import "../../App.scss";

export default function Admin({ history }) {
  const [recordList, setList] = useState([]);
  const [isLoading, setLoadingStatus] = useState(true);

  const createEvent = () => {
    let path = "/admin/create";
    history.push(path);
  };

  const editEvent = (e) => {
    const event_id = e.currentTarget.id;
    console.log(event_id);
    let path = `/admin/edit/${event_id}`;
    history.push(path);
  };

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_PATH + "/findAllEvent", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res);
          setList((recordList) => res.data);
          setLoadingStatus((isLoading) => false);
        }
      })
      .catch((err) => {
        console.log(err);
        setLoadingStatus((isLoading) => false);
      });
  }, []);

  return isAdmin() ? (
    <div>
      <NavBar />

      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        <Alert className="btn-lg w-100 text-center text-light bg-black">
          Current/Upcoming Events
        </Alert>

        {recordList.map(function (record) {
          return (
            <Button
              key={record.event_id}
              id={record.event_id}
              className="btn-lg color-nav border-0 btn-hover-red admin-home-btn fs-6"
              active
              onClick={(e) => editEvent(e)}
              disabled={new Date() > new Date(record.start_date_time)}
            >
              {record.area_name}
              <br />
              <small> {dateFormat(new Date(record.start_date_time))}</small> -
              <small> {dateFormat(new Date(record.end_date_time))}</small>
            </Button>
          );
        })}
        {!isLoading ? (
          <Button
            className="btn-circle color-nav border-0 btn-hover-green"
            to={"/admin/create"}
            onClick={createEvent}
          >
            <BsPlusLg className="fs-3" />
          </Button>
        ) : (
          <>
            <Spinner animation="border" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
          </>
        )}
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
