import React, { useState } from "react";
import {
  isAdmin,
  fileType,
  DANGER,
  SUCCESS,
  INVALID_FILE_TYPE,
  fileExtension,
  SAMPLE_EXCEL_DATA,
} from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import "../../App.scss";
import { Button, Accordion, Spinner, Form } from "react-bootstrap";
import { AiOutlineFileExcel } from "react-icons/ai";
import AlertBox from "../../components/AlertBox.js";
import * as FileSaver from "file-saver";
import * as XLSX from "xlsx";
import axios from "axios";
import { BsWindowSidebar } from "react-icons/bs";

export default function Upload() {
  const [show, setShow] = useState(false); // Logic for displaying alert
  const handleShow = () => setShow(true); // Logic for displaying alert
  const handleDismiss = () => setShow(false); // Logic for closing alert
  const [errMsg, setErrMsg] = useState(); // Logic setting error msg
  const [variant, setVariant] = useState();
  const [selectedFile, setSelectedFile] = useState();
  const [btnStatus, setBtnStatus] = useState(true);
  const [isLoading, setIsLoadingStatus] = useState(false);
  const [excelFile, setExcelFile] = useState([]);

  const changeHandler = (e) => {
    console.log(e.target.files[0]);
    if (e.target.files[0].type === fileType) {
      setSelectedFile(e.target.files[0]);
      setBtnStatus(false); // put false to set button disabled to false
      handleDismiss();
    } else {
      setErrMsg((errMsg) => INVALID_FILE_TYPE);
      setVariant((variant) => DANGER);
      setBtnStatus(true); // true  to set button disabled to true
      handleShow(); // Display alert
    }
  };

  function s2ab(s) {
    var buf = new ArrayBuffer(s.length);
    var view = new Uint8Array(buf);
    for (var i = 0; i !== s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
    return buf;
  }

  const onUpload = () => {
    setIsLoadingStatus(true);
    setBtnStatus(true); // disable upload button
    // If file is correctly selected
    const data = new FormData();
    data.append("file", selectedFile);
    axios
      .post("https://api.mimis.social/upload", data, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
          id_token: `Bearer ${localStorage.getItem("ID_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setIsLoadingStatus(false);
          setBtnStatus(false);
          console.log(res.data.excel_file);
          var first = true;
          res.data.excel_file.forEach((file) => {
            var blob = new Blob([s2ab(atob(file))], {
              type: fileType,
            });
            var url = URL.createObjectURL(blob);
            //window.open(url);
            var a = document.createElement("a");
            a.download = "Confidential_Credential.xlsx";
            a.href = url;
            document.body.appendChild(a);
            a.click();
            a.remove();
          });
          console.log(res);
          setErrMsg((errMsg) => res.data.message);
          setVariant((variant) => SUCCESS);
          handleShow(); // Display alert
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err);
        setErrMsg((errMsg) => err.response.data.message);
        setVariant((variant) => DANGER);
        handleShow(); // Display alert
        setIsLoadingStatus(false);
        setBtnStatus(false);
      });
  };

  // Sample excel data format
  const downloadSample = () => {
    const ws = XLSX.utils.json_to_sheet(SAMPLE_EXCEL_DATA);
    const wb = { Sheets: { data: ws }, SheetNames: ["data"] };
    var excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const data = new Blob([excelBuffer], { type: fileType });
    FileSaver.saveAs(data, "Sample" + fileExtension);
  };

  return isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex gap-5 pt-4 align-items-center flex-column">
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
        <Form className="d-flex flex-column gap-3 w-75">
          <Accordion defaultActiveKey="0">
            <Accordion.Item eventKey="0">
              <Accordion.Header>How to Upload</Accordion.Header>
              <Accordion.Body>
                This uploader only accept a single file format <b>'.xlsx'</b>.
                The purpose of this uploader is to{" "}
                <b>generate passwords, private keys and public keys</b> tagged
                to each login identifier provided. Please upload each set of
                voters based on their <b>area identification</b>. You will
                receive excel file(s) in short while. Please wait patiently
                after submitting. <br />
                <br />
                Below is a sample format you need to follow:
                <br />
                <Button
                  className="btn-sm color-nav border-0"
                  onClick={() => downloadSample()}
                >
                  Download Sample
                </Button>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
          <Form.Control type="file" accept=".xlsx" onChange={changeHandler} />
          <Button
            type="button"
            className="btn-success text-light"
            variant="danger"
            onClick={() => onUpload()}
            disabled={btnStatus ? true : false}
          >
            {isLoading ? (
              <>
                <Spinner
                  as="span"
                  animation="grow"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />
                Loading..
              </>
            ) : (
              <>
                <AiOutlineFileExcel /> &nbsp;Upload
              </>
            )}
          </Button>
        </Form>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
