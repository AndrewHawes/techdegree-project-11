import React from 'react';

import TokenAuth from '../lib/token-auth';


export default class Registration extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      password: '',
      password2: '',
      message: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleRegistration = this.handleRegistration.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleRegistration() {
    const username = this.state.username;
    const password = this.state.password;

    const loginRedirect = () => this.props.setView('preferences');
    const setFailMessage = (message) => this.setState({message: message});
    const login = () => TokenAuth.login(username, password, loginRedirect);

    TokenAuth.register(username, password, login, setFailMessage);
  }

  disabled() {
    return this.state.username === ''
      || this.state.password === ''
      || this.state.password2 === ''
      || this.state.password !== this.state.password2;
  }

  render() {
    return (
      <div>
        <p className="text-centered">{this.state.message}</p>
        <input type="text"
               name="username"
               placeholder="Username"
               value={this.state.username}
               onChange={this.handleChange}
        />
        <input type="password"
               name="password"
               placeholder="Password"
               value={this.state.password}
               onChange={this.handleChange}
        />
        <input type="password"
               name="password2"
               placeholder="Verify Password"
               value={this.state.password2}
               onChange={this.handleChange}
        />
        <button className="button"
                onClick={this.handleRegistration}
                disabled={this.disabled()}>
          Register
        </button>
      </div>
    );
  }
}
