import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "../App.css";
import Header from "./Header";
import Home from "../views/Home";
import NewReleases from "../views/NewReleases";
import Login from "../views/Login";

function App() {
  return (
    <div>
      <Login />
    </div>
  );

  // return (
  //     <div>
  //       <Router>
  //         <Header />

  //         <Switch>
  //           <Route exact path="/">
  //             <Home />
  //           </Route>

  //           <Route path="/new-releases">
  //             <NewReleases />
  //           </Route>
  //         </Switch>
  //       </Router>
  //     </div>
  //   );
}

export default App;
