import React, { useEffect, useState } from "react";
import { isAdmin, dateFormat } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Button } from "react-bootstrap";
import { DEFAULTSELECTOR, DANGER, SUCCESS } from "../../util";
import AlertBox from "../../components/AlertBox.js";
import axios from "axios";
import "../../App.scss";

export default function PastEvent({ history }) {
  const [show, setShow] = useState(false); // For storing the state of Modal
  const handleClose = () => setShow(false); // For dismissing Modal
  const handleShow = () => setShow(true); // For displaying Modal
  const [recordList, setList] = useState([]);
  const [errMsg, setErrMsg] = useState();
  const [variant, setVariant] = useState();

  useEffect(() => {
    axios
      .get("http://localhost:5000/findPastEvent", {
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
        // Set error message
        console.log(err.response.data.message);
        setErrMsg((errMsg) => err.response.data.message);
        setVariant((variant) => DANGER);
        handleShow(); // Display alert
      });
  }, []);

  const redirectToResult = (e) => {
    const event_id = e.currentTarget.id;
    let path = `/admin/result/${event_id}`;
    history.push(path);
  };

  return isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        {show ? (
          <AlertBox
            err={[]}
            setShow={setShow}
            errMsg={errMsg}
            variant={variant}
          />
        ) : (
          <></>
        )}
        {recordList.map(function (record) {
          return (
            <Button
              key={record.event_id}
              id={record.event_id}
              className="btn-lg color-nav border-0 btn-hover-red admin-home-btn"
              active
              onClick={(e) => redirectToResult(e)}
            >
              {record.area_name}
              <br />
              <small> {dateFormat(new Date(record.start_date_time))}</small>
            </Button>
          );
        })}
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
