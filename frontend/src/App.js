import React from "react";
import "./App.scss";
import Main from "./containers/Main.js";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { createBrowserHistory } from "history";
import { Auth0Provider, withAuthenticationRequired } from "@auth0/auth0-react";
import Redirect from "./containers/Redirect.js";
import AdminHome from "./containers/admin/AdminHome.js";
import VoterHome from "./containers/voter/VoterHome.js";
import UpcomingElections from "./containers/voter/UpcomingElections.js";
import MyVoteStatus from "./containers/voter/MyVoteStatus.js";
import Poll from "./containers/voter/Poll.js";
import PastElection from "./containers/admin/PastElection.js";
import Result from "./containers/admin/Result.js";
import Upload from "./containers/admin/Upload.js";
import EditElection from "./containers/admin/EditElection.js";
import CreateElection from "./containers/admin/CreateElection.js";

export const history = createBrowserHistory();

const ProtectedRoute = ({ component, ...args }) => (
  <Route component={withAuthenticationRequired(component)} {...args} />
);

export default function App() {
  return (
    <div>
      <Auth0Provider
        domain={process.env.REACT_APP_AUTH0_DOMAIN}
        clientId={process.env.REACT_APP_AUTH0_CLIENTID}
        redirectUri={window.location.origin + "/redirect"}
        audience={process.env.REACT_APP_AUTH0_AUDIENCE}
        scope="read:current_user"
      >
        <Router history={history}>
          <Switch>
            <Route path="/" exact component={Main} />
            <ProtectedRoute path="/redirect" exact component={Redirect} />
            <ProtectedRoute path="/admin/home" exact component={AdminHome} />
            <ProtectedRoute
              path="/admin/pastevent"
              exact
              component={PastElection}
            />
            <ProtectedRoute
              path="/admin/edit/:id"
              exact
              component={EditElection}
            />
            <ProtectedRoute path="/admin/result/:id" exact component={Result} />
            <ProtectedRoute path="/admin/upload" exact component={Upload} />
            <ProtectedRoute
              path="/admin/create"
              exact
              component={CreateElection}
            />

            <ProtectedRoute path="/voter/home" exact component={VoterHome} />
            <ProtectedRoute
              path="/voter/upcomingelections"
              exact
              component={UpcomingElections}
            />
            <ProtectedRoute
              path="/voter/myvotestatus"
              exact
              component={MyVoteStatus}
            />
            <ProtectedRoute path="/voter/poll/:id" exact component={Poll} />
          </Switch>
        </Router>
      </Auth0Provider>
    </div>
  );
}
