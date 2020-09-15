import React from "react";
import Navigation from "./Navigation";

function Header() {
  return (
    <header className="box">
      <div id="brand">
        <img src="/Assets/compendiaIcon.png" alt="Compendia Logo" />
        <h1>ompendia</h1>
      </div>
      <Navigation />
    </header>
  );
}

export default Header;
