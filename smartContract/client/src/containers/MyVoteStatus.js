import React from "react";
import { isAdmin } from "../util";
import { Redirect } from "react-router-dom";
import NavBar from "../components/NavBar.js";
import { Table } from "react-bootstrap";
import "../App.scss";

const MyVoteStatus = () => {
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
              <td>Aljunied GRC</td>
              <td>Submitted</td>
            </tr>
          </tbody>
        </Table>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
};

export default MyVoteStatus;
