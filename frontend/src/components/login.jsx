import React from 'react';
import styled from 'styled-components';

import TokenAuth from '../lib/token-auth';

const RegisterLink = styled.button`
`;


export default class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = { username: '', password: '', message: '' };

    this.handleChange = this.handleChange.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
    this.handleRegisterClick = this.handleRegisterClick.bind(this);
  }

  handleChange(e) {
    this.setState({[e.target.name]: e.target.value});
  }

  handleLogin() {
    const username = this.state.username;
    const password = this.state.password;

    const loginRedirect = () => this.props.setView('undecided');
    const loginFail = (error) => {
      if (error.response) {
        if (error.response.status === 400) {
          this.setState({message: 'Username or password are incorrect.'});
        } else {
          this.setState({message: error.message});
        }
      }
    };

    TokenAuth.login(username, password, loginRedirect, loginFail);
  }

  handleRegisterClick(e) {
    this.props.setView('registration');
  }

  disabled() {
    return this.state.username === '' || this.state.password === '';
  }

  render() {
    return (
      <div>
        <p className="text-centered">{this.state.message}</p>
        <input
          type='text'
          name='username'
          placeholder='Username'
          value={this.state.username}
          onChange={this.handleChange}
        />
        <input
          type='password'
          name='password'
          placeholder='Password'
          value={this.state.password}
          onChange={this.handleChange}
        />
        <button onClick={this.handleLogin} disabled={this.disabled()}>Login</button>
        <RegisterLink as="a" onClick={this.handleRegisterClick}>Register</RegisterLink>
        {/*<a onClick={this.handleRegisterClick}>Register</a>*/}
      </div>
    );
  }
}