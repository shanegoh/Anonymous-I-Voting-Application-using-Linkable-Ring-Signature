import React, { useEffect, useState } from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Button } from "react-bootstrap";
import { BsPlusLg } from "react-icons/bs";
import { axiosConfig } from "../../util";
import axios from "axios";
import "../../App.scss";

export default function Admin({ history }) {
  const [recordList, setList] = useState([]);

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
      .get("http://localhost:5000/events", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setList((recordList) => res.data);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        {recordList.map(function (record) {
          return (
            <Button
              key={record.event_id}
              id={record.event_id}
              className="btn-origin btn-lg color-nav"
              active
              onClick={(e) => editEvent(e)}
            >
              {record.area_name}
              <br />
              {new Date(record.start_date_time).toString()}
            </Button>
          );
        })}

        <Button
          className="btn-circle btn-success"
          to={"/admin/create"}
          onClick={createEvent}
        >
          <BsPlusLg className="fs-3" />
        </Button>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}