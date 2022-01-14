import React, { useEffect, useState } from "react";
import { isAdmin, DANGER, fileType, fileExtension } from "../../util";
import { Redirect, useParams } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Pie } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";
import { Chart, ArcElement, Tooltip, Legend } from "chart.js";
import { Button } from "react-bootstrap";
import axios from "axios";
import { BsDownload } from "react-icons/bs";
import AlertBox from "../../components/AlertBox.js";
import "../../App.scss";
import * as FileSaver from "file-saver";
import * as XLSX from "xlsx";

Chart.register(ArcElement, Tooltip, Legend);

export default function Result() {
  const [show, setShow] = useState(false); // Logic for displaying alert
  const handleShow = () => setShow(true); // Logic for displaying alert
  const [errMsg, setErrMsg] = useState();
  const [variant, setVariant] = useState();
  const [isLoaded, setLoadStatus] = useState(false);
  const [label, setLabel] = useState([]);
  const [candidateImage, setCandidateImage] = useState([]);
  const [voteCount, setVoteCount] = useState([]);
  const [candidateList, setCandidateList] = useState([]);

  // Event id
  const { id } = useParams();

  useEffect(() => {
    axios
      .get(`https://api.mimis.social/findResultById/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("ACCESS_TOKEN")}`,
        },
      })
      .then((res) => {
        if (res.status === 200) {
          console.log(res.data);
          setCandidateList((candidateList) => res.data);
          setLoadStatus((isLoaded) => true);
          res.data.forEach((object) => {
            setLabel((label) => [
              ...label,
              object.candidate_name + " (" + object.vote_count + ")",
            ]);
            setCandidateImage((candidateImage) => [
              ...candidateImage,
              object.candidate_image,
            ]);
            setVoteCount((voteCount) => [...voteCount, object.vote_count]);
          });
        }
      })
      .catch((err) => {
        // Set error message
        console.log(err);
        console.log(err.response.data.message);
        setErrMsg((errMsg) => err.response.data.message);
        setVariant((variant) => DANGER);
        handleShow(); // Display alert
      });
  }, []);

  // Set data for displaying the pie chart
  const data = {
    labels: label,
    datasets: [
      {
        data: voteCount,
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 205, 86)",
        ],
        hoverOffset: 4,
      },
    ],
  };

  // Options to override the plugin tooltip over function.
  // User are able to hover over and see the percentage.
  const option = {
    plugins: {
      tooltip: {
        callbacks: {
          title: (toolTipItem) => {
            let sum = 0;
            let dataArr = toolTipItem[0].dataset.data;
            dataArr.map((data) => {
              // Find the total value of all candidate votes
              sum += Number(data);
            });
            //Calculate and display the percentage of votes for each candidate
            let percentage =
              ((toolTipItem[0].parsed / sum) * 100).toFixed(2) + "%";
            return `Vote Percentage: ${percentage} `;
          },
        },
      },
    },
  };

  // function to export the data in xlsx format
  const exportToCSV = (apiData, fileName) => {
    // Logic for finding the total votes
    const sum = voteCount.reduce((t, e) => (t = t + e), 0);
    // Logic for appending new json data for statistics
    voteCount.forEach((object, i) => {
      apiData[i]["vote_percentage"] = ((object / sum) * 100).toFixed(2) + "%";
      // Logic for finding the highest votes thus being elected
    });
    const ws = XLSX.utils.json_to_sheet(apiData);
    const wb = { Sheets: { data: ws }, SheetNames: ["data"] };
    var excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const data = new Blob([excelBuffer], { type: fileType });
    FileSaver.saveAs(data, fileName + fileExtension);
  };

  return isAdmin() ? (
    <div>
      <NavBar />

      <div className="d-flex flex-column gap-2 pt-4 align-items-center ">
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
        {isLoaded ? (
          <div className="d-flex flex-column gap-3">
            <MDBContainer className="pt-5">
              <Pie data={data} options={option} />
            </MDBContainer>
            <Button
              variant="success fs-4"
              onClick={() =>
                exportToCSV(candidateList, candidateList[0].area_name)
              }
            >
              <BsDownload />
              &nbsp; Download
            </Button>
          </div>
        ) : (
          <></>
        )}
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
