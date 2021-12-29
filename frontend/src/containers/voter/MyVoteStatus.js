import React, { useEffect, useState } from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Table } from "react-bootstrap";
import axios from "axios";
import "../../App.scss";

export default function MyVoteStatus() {
  const [area, setArea] = useState();
  useEffect(() => {
    axios
      .get(`http://localhost:5000/findVoteStatus`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data.area);
          setArea((area) => res.data.area);
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err.response.message);
      });
  }, []);
  return !isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        <Table
          className="w-50 text-center color-nav text-light table-radius"
          striped
          bordered
          hover
        >
          <thead>
            <tr>
              <th>My Vote</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody className="bg-light">
            <tr>
              <td>{area}</td>
              <td>?</td>
            </tr>
          </tbody>
        </Table>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
