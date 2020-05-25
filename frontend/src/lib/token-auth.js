import axios from 'axios';

export default class TokenAuth {
  static getAuthString() {
    return sessionStorage.getItem('authString');
  }

  static setAuthString(authString) {
    sessionStorage.setItem('authString', authString);
  }

  static clearAuthString() {
    sessionStorage.removeItem('authString');
  }

  static getAuthHeader() {
    return { Authorization: 'Token ' + this.getAuthString() };
  }

  static getUsername() {
    const username = localStorage.getItem('username');
    if (username) {
      return username;
    }
    return null;
  }

  static setUsername(username) {
    localStorage.setItem('username', username);
  }

  static login(username, password, successCallback, failCallback) {
    if (this.loggedIn()) {
      successCallback();
      return;
    }
    const url = '/api/user/login/';
    const data = {username: username, password: password};

    axios.post(url, data)
      .then(response => {
        this.setUsername(username);
        this.setAuthString(response.data.token);
        successCallback();
      })
      .catch(error => {
        this.clearAuthString();
        failCallback(error);
      });
  }

  static logout(callback) {
    this.clearAuthString();
    callback();
  }

  static loggedIn() {
    return !!this.getAuthString();
  }

  static register(username, password, successCallback, failCallback) {
    const url = '/api/user/';
    const data = {username: username, password: password};

    axios.post(url, data)
      .then(response => {
        this.setUsername(username);
        successCallback();
      })
      .catch(error => {
        if (error.response) {
          failCallback(error.response.data['username']);
        } else {
          failCallback(error.message);
        }
      });
  }
}