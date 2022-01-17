import React, { useEffect, useState } from "react";
import { isAdmin, DANGER } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Table, Spinner } from "react-bootstrap";
import AlertBox from "../../components/AlertBox.js";
import axios from "axios";
import "../../App.scss";

export default function MyVoteStatus() {
  const [show, setShow] = useState(false); // Logic for displaying alert
  const handleShow = () => setShow(true); // Logic for displaying alert
  const [errMsg, setErrMsg] = useState(); // Logic setting error msg
  const [area, setArea] = useState();
  const [status, setStatus] = useState();
  const [isLoaded, setLoadStatus] = useState(false);
  const [isLoading, setLoadingStatus] = useState(true);

  useEffect(() => {
    axios
      .get(process.env.REACT_APP_PATH + "/findVoteStatus", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setArea((area) => res.data.area);
          setStatus((status) => res.data.status);
          setLoadStatus((isLoaded) => true);
          setLoadingStatus((isLoading) => false);
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err.response.message);
        setErrMsg((errMsg) => err.response.message);
        setLoadingStatus((isLoading) => false);
        handleShow();
      });
  }, []);
  return !isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center ">
        {show ? (
          <AlertBox
            err={[]}
            setShow={setShow}
            errMsg={errMsg}
            variant={DANGER}
          />
        ) : (
          <></>
        )}
        {isLoaded ? (
          <Table
            className="color-nav text-light table-radius result-table-width"
            striped
          >
            <thead>
              <tr>
                <th>Election</th>
                <th>Vote Status</th>
              </tr>
            </thead>
            <tbody className="bg-light">
              <tr>
                <td style={{ width: "60%" }}>{area}</td>
                <td>{status}</td>
              </tr>
            </tbody>
          </Table>
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
  ) : (
    <Redirect to="/redirect" />
  );
}
