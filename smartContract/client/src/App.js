import React, { Component } from "react";
import SimpleStorageContract from "./contracts/SimpleStorage.json";
// import getWeb3 from "./getWeb3";
import "./App.scss";
import Main from "./containers/Main.js";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { createBrowserHistory } from "history";
import { Auth0Provider, withAuthenticationRequired } from "@auth0/auth0-react";
import Redirect from "./containers/Redirect.js";
import Admin from "./containers/Admin.js";
import VoterHome from "./containers/VoterHome.js";
import UpcomingElections from "./containers/UpcomingElections.js";
import MyVoteStatus from "./containers/MyVoteStatus.js";
import Poll from "./containers/Poll.js";

export const history = createBrowserHistory();

const ProtectedRoute = ({ component, ...args }) => (
  <Route component={withAuthenticationRequired(component)} {...args} />
);

export default function App() {
  // state = { storageValue: 0, web3: null, accounts: null, contract: null };

  // componentDidMount = async () => {
  //   try {
  //     // Get network provider and web3 instance.
  //     const web3 = await getWeb3();

  //     // Use web3 to get the user's accounts.
  //     const accounts = await web3.eth.getAccounts();

  //     // Get the contract instance.
  //     const networkId = await web3.eth.net.getId();
  //     const deployedNetwork = SimpleStorageContract.networks[networkId];
  //     const instance = new web3.eth.Contract(
  //       SimpleStorageContract.abi,
  //       deployedNetwork && deployedNetwork.address
  //     );

  //     // Set web3, accounts, and contract to the state, and then proceed with an
  //     // example of interacting with the contract's methods.
  //     this.setState({ web3, accounts, contract: instance }, this.runExample);
  //   } catch (error) {
  //     // Catch any errors for any of the above operations.
  //     alert(
  //       `Failed to load web3, accounts, or contract. Check console for details.`
  //     );
  //     console.error(error);
  //   }
  // };

  // runExample = async () => {
  //   const { accounts, contract } = this.state;

  //   // Stores a given value, 5 by default.
  //   await contract.methods.set(5).send({ from: accounts[0] });

  //   // Get the value from the contract to prove it worked.
  //   const response = await contract.methods.get().call();

  //   // Update state with the result.
  //   this.setState({ storageValue: response });
  // };

  // render() {
  //   if (!this.state.web3) {
  //     return <div>Loading Web3, accounts, and contract...</div>;
  //   }
  //   return (
  //     <div className="App">
  //       <h1>Good to Go!</h1>
  //       <p>Your Truffle Box is installed and ready.</p>
  //       <h2>Smart Contract Example</h2>
  //       <p>
  //         If your contracts compiled and migrated successfully, below will show
  //         a stored value of 5 (by default).
  //       </p>
  //       <p>
  //         Try changing the value stored on <strong>line 42</strong> of App.js.
  //       </p>
  //       <div>The stored value is: {this.state.storageValue}</div>
  //     </div>
  //   );
  // }
  return (
    <div>
      <Auth0Provider
        domain={process.env.REACT_APP_AUTH0_DOMAIN}
        clientId={process.env.REACT_APP_AUTH0_CLIENTID}
        redirectUri={window.location.origin + "/redirect"}
        audience="https://dev-rkub2ofp.us.auth0.com/api/v2/"
        scope="read:current_user"
      >
        <Router history={history}>
          <Switch>
            <Route path="/main" exact component={Main} />
            <ProtectedRoute path="/redirect" exact component={Redirect} />
            <ProtectedRoute path="/admin" exact component={Admin} />
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
            <ProtectedRoute path="/voter/poll" exact component={Poll} />
          </Switch>
        </Router>
      </Auth0Provider>
    </div>
  );
}
