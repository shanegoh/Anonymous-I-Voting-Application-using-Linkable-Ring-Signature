import React from "react";
import Carousel from "react-bootstrap/Carousel";
import NavBar from "../../components/NavBar.js";
import { isAdmin, hasToken } from "../../util";
import { Redirect } from "react-router-dom";
import "../../App.scss";

export default function Voter() {
  const redirect = (e) => {
    var id = parseInt(e.target.id);
    console.log(id);
    if (id === 0) {
      window.open("https://www.eld.gov.sg/latestnews.html");
    } else if (id === 1) {
      window.open(
        "https://app.eservice.eld.gov.sg/voter/postalcodeenquiry.aspx"
      );
    } else if (id === 2) {
      window.open("https://www.eld.gov.sg/online.html");
    }
  };
  return !isAdmin() && hasToken() ? (
    <div>
      <NavBar />
      <Carousel variant="dark" style={{ zIndex: "0", paddingTop: "5rem" }}>
        <Carousel.Item>
          <img
            className="d-block w-100"
            src="https://i.postimg.cc/BbCpPghC/1388994.jpg"
            alt="LATEST NEWS"
            id="0"
            onClick={(e) => redirect(e)}
          />
          <Carousel.Caption>
            <div className="carousel-bg-color">
              <h1>Latest News</h1>
            </div>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <img
            className="d-block w-100"
            src="https://i.postimg.cc/SKtL6V0N/1000px-Electoral-boundaries-during-the-Singapore-general-elections-2020-svg.png"
            alt="Check electoral division"
            onClick={(e) => redirect(e)}
            id="1"
          />
          <Carousel.Caption>
            <div className="carousel-bg-color">
              <h1>Electoral Divisions</h1>
            </div>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <img
            className="d-block w-100"
            src="https://i.postimg.cc/4xYxK111/2-2.png"
            alt="Voter services"
            onClick={(e) => redirect(e)}
            id="2"
          />

          <Carousel.Caption>
            <div className="carousel-bg-color">
              <h1>Voter Services</h1>
            </div>
          </Carousel.Caption>
        </Carousel.Item>
      </Carousel>
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
}
