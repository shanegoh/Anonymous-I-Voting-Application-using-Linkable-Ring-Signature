import React from "react";
import "./App.css";
import LoginButton from "./components/LoginButton";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { createBrowserHistory } from "history";
import { Auth0Provider, withAuthenticationRequired } from "@auth0/auth0-react";
import VoterHome from "./containers/VoterHome.js";

export const history = createBrowserHistory();

const ProtectedRoute = ({ component, ...args }) => (
  <Route component={withAuthenticationRequired(component)} {...args} />
);

// const onRedirectCallback = (appState) => {
//   // Use the router's history module to replace the url
//   history.replace(appState?.returnTo || window.location.origin + "/voterhome");
// };

export default function App() {
  return (
    <div className="App-header">
      <Auth0Provider
        domain={process.env.REACT_APP_AUTH0_DOMAIN}
        clientId={process.env.REACT_APP_AUTH0_CLIENTID}
        redirectUri={window.location.origin + "/voterhome"}
        audience="https://dev-rkub2ofp.us.auth0.com/api/v2/"
        scope="read:current_user"
      >
        <Router history={history}>
          <Switch>
            <Route path="/" exact component={LoginButton} />
            <ProtectedRoute path="/voterhome" exact component={VoterHome} />
          </Switch>
        </Router>
      </Auth0Provider>
    </div>
  );
}
