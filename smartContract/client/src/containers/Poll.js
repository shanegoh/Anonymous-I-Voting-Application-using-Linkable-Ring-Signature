import React, { useState } from "react";
import NavBar from "../components/NavBar.js";
import { Table, Form, Button } from "react-bootstrap";
import { BsFillPersonFill } from "react-icons/bs";
import { ImBoxAdd } from "react-icons/im";
import "../App.scss";

export default function Poll() {
  const [selected, setSelected] = useState();

  const onSelectedChange = (index) => {
    setSelected(index);
    console.log(index);
  };

  return (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center">
        <Table className="w-25 text-center table-bordered table-radius">
          <thead className="color-nav text-light">
            <tr>
              <th colSpan="2">Alunied GRC 2021</th>
            </tr>
          </thead>
          <tbody style={{ height: "10rem" }}>
            <tr>
              <td className="w-50">
                <BsFillPersonFill style={{ width: "5rem", height: "5rem" }} />
              </td>

              <td className="w-50 ">
                <Form.Check
                  style={{ color: "red" }}
                  type="checkbox"
                  onChange={() => onSelectedChange(0)}
                  checked={selected === 0 ? true : false}
                />
              </td>
            </tr>
            <tr>
              <td className="w-50">
                <BsFillPersonFill style={{ width: "5rem", height: "5rem" }} />
              </td>
              <td>
                <Form.Check
                  type="checkbox"
                  id="0"
                  onChange={() => onSelectedChange(1)}
                  checked={selected === 1 ? true : false}
                />
              </td>
            </tr>
          </tbody>
        </Table>
        <Button className="text-light" size="lg" variant="danger">
          <ImBoxAdd />
          &nbsp; Vote
        </Button>
      </div>
    </div>
  );
}
