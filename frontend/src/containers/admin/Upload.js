import React, { useState } from "react";
import { isAdmin, fileType } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import "../../App.scss";
import { ToastContainer, toast } from "react-toastify";
import { Progress } from "reactstrap";
import { Form } from "react-bootstrap";
import { Button, Container, Row } from "react-bootstrap";
import { AiOutlineFileExcel } from "react-icons/ai";
import axios from "axios";

export default function Upload() {
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);

  const changeHandler = (e) => {
    console.log(e.target.files[0]);
    setSelectedFile(e.target.files[0]);
    setIsFilePicked(true);
  };

  function s2ab(s) {
    var buf = new ArrayBuffer(s.length);
    var view = new Uint8Array(buf);
    for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
    return buf;
  }

  const onUpload = () => {
    const data = new FormData();
    data.append("file", selectedFile);
    axios
      .post(`http://localhost:5000/upload`, data, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data.excel_file);
          var blob = new Blob([s2ab(atob(res.data.excel_file))], {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;",
          });
          var url = URL.createObjectURL(blob);
          window.open(url);
        }
      })
      .catch((err) => {
        // Set error message
        //console.log(err);
        // setErrMsg((errMsg) => err.response.data.message);
        // setVariant((variant) => DANGER);
        // handleShow(); // Display alert
      });
  };

  return isAdmin() ? (
    <div>
      <NavBar />
      <Container>
        <Row>
          <div className="offset-md-3 col-md-6">
            <Form>
              <div className="d-flex flex-column files gap-3">
                <label>Upload Your Excel File</label>
                <Form.Control type="file" onChange={changeHandler} />
                <Button
                  type="button"
                  className="btn-success text-light"
                  variant="danger"
                  onClick={() => onUpload()}
                >
                  <AiOutlineFileExcel /> &nbsp;Upload
                </Button>
              </div>
              <div className="form-group">
                <ToastContainer />
              </div>
            </Form>
          </div>
        </Row>
      </Container>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
