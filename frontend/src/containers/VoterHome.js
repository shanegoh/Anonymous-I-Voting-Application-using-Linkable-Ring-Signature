import React, { useState, useEffect } from "react";
import Media from "../components/Media.js";
import NavBar from "../components/NavBar.js";
import UpcomingElections from "./UpcomingElections.js";
import MyVoteStatus from "./MyVoteStatus.js";
import { isAdmin } from "../util";
import { Redirect } from "react-router-dom";
import "../App.scss";

const Voter = () => {
  // const home_page = 0;
  // const upcoming_election_page = 1;
  // const my_vote_status_page = 2;
  // const [pageIndex, setIndex] = useState();

  // const load_page = (index) => {
  //   setIndex(index);
  // };

  // const renderPage = (pageIndex) => {
  //   if (pageIndex === home_page) {
  //     return <Media />;
  //   } else if (pageIndex === upcoming_election_page) {
  //     return <UpcomingElections />;
  //   } else if (pageIndex === my_vote_status_page) {
  //     return <MyVoteStatus />;
  //   } else return <Media />;
  // };

  // useEffect(() => {
  //   renderPage(pageIndex);
  // });

  return !isAdmin() ? (
    <div>
      <NavBar />
      <Media />
    </div>
  ) : (
    <Redirect to="/redirect" />
  );
};

export default Voter;
