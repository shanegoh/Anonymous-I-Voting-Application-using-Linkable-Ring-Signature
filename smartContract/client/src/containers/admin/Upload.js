import React from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import "../../App.scss";
import { ToastContainer, toast } from "react-toastify";
import { Progress } from "reactstrap";
import { Form } from "react-bootstrap";
import { Button, Container, Row } from "react-bootstrap";
import { AiOutlineFileExcel } from "react-icons/ai";

export default function Upload() {
  return isAdmin() ? (
    <div>
      <NavBar />
      <Container>
        <Row>
          <div className="offset-md-3 col-md-6">
            <div className="form-group files">
              <label>Upload Your Excel File</label>
              <Form.Control type="file" />
            </div>
            <div className="form-group">
              <ToastContainer />
              <Progress max="100" color="success">
                {}%
              </Progress>
            </div>

            <Button
              type="button"
              className="btn-success text-light"
              variant="danger"
            >
              <AiOutlineFileExcel /> &nbsp;Upload
            </Button>
          </div>
        </Row>
      </Container>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
