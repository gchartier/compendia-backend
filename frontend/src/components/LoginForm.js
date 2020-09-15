import React from "react";
import axios from "axios";

class LoginForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: "",
    };
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleEmailChange(event) {
    this.setState({ email: event.target.value });
  }

  handlePasswordChange(event) {
    this.setState({ password: event.target.value });
  }

  handleSubmit(event) {
    const loginURL = "https://compendia-app.com/api/accounts/login";
    const data = new FormData();
    data.append("username", this.state.email);
    data.append("password", this.state.password);

    event.preventDefault();

    axios
      .post(loginURL, data)
      .then(function (res) {
        if (res.data.token) {
          alert("Logged in. Here is your token: " + res.data.token);
          //TODO set app token
        } else if (res.data.error_message)
          alert("Error: " + res.data.error_message);
        else alert("Something went wrong...");
      })
      .catch(function (error) {
        alert("ERROR: " + error);
      });
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Email:
          <input
            type="email"
            value={this.state.value}
            onChange={this.handleEmailChange}
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={this.state.value}
            onChange={this.handlePasswordChange}
          />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default LoginForm;
