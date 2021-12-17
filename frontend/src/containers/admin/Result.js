import React, { useState } from "react";
import { isAdmin } from "../../util";
import { Redirect } from "react-router-dom";
import NavBar from "../../components/NavBar.js";
import { Pie } from "react-chartjs-2";
import { MDBContainer } from "mdbreact";
import { Chart, ArcElement, Tooltip, Legend } from "chart.js";
import { Button } from "react-bootstrap";
import { BsDownload } from "react-icons/bs";
import "../../App.scss";

Chart.register(ArcElement, Tooltip, Legend);

export default function Result() {
  const data = {
    labels: ["Candidate 1", "Candidate 2"],
    datasets: [
      {
        label: "My First Dataset",
        data: [789, 711],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 205, 86)",
        ],
        hoverOffset: 4,
      },
    ],
  };
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
            console.log(toolTipItem[0].parsed);
            //Calculate and display the percentage of votes for each candidate
            let percentage =
              ((toolTipItem[0].parsed / sum) * 100).toFixed(2) + "%";
            return `Vote Percentage: ${percentage}`;
          },
        },
      },
    },
  };
  return isAdmin() ? (
    <div>
      <NavBar />
      <div className="d-flex flex-column gap-2 pt-4 align-items-center ">
        Name of Election
        <MDBContainer className="pt-5" style={{ width: "25rem" }}>
          <Pie data={data} options={option} />
        </MDBContainer>
        <Button variant="outline-primary fs-4">
          <BsDownload />
          &nbsp; Download
        </Button>
      </div>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
