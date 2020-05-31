import React from 'react';

import TokenAuth from '../lib/token-auth';

import DogContainer from '../containers/dogContainer';
import Preferences from './preferences';
import Registration from './registration';
import Login from './login';
import DogForm from './dogForm';

import logo from '../static/icons/logo.svg';

export default class PugOrUgh extends React.Component {
  constructor(props) {
    super(props);

    this.handleLogoutClick = this.handleLogoutClick.bind(this);
    this.hideLogout = this.hideLogout.bind(this);
    this.getViewComponent = this.getViewComponent.bind(this);
    this.setView = this.setView.bind(this);
  }

  componentWillMount() {
    this.setView(TokenAuth.loggedIn() ? 'undecided' : 'login');
  }

  getViewComponent(view, id) {
    switch (view) {
      case 'liked':
      case 'disliked':
      case 'undecided':
        return <DogContainer setView={this.setView} filter={view} id={id}/>;
      case 'preferences':
        return <Preferences setView={this.setView}/>;
      case 'registration':
        return <Registration setView={this.setView}/>;
      case 'login':
        return <Login setView={this.setView}/>;
      case 'new':
        return <DogForm setView={this.setView}/>;
      default:
        return new Error("Unrecognized view requested.")
    }
  }

  setView(view, id) {
    let component = this.getViewComponent(view, id);
    this.setState({view: component, viewName: view});
  }

  handleLogoutClick() {
    TokenAuth.logout(() => this.setView('login'));
  }

  hideLogout() {
    return this.state.viewName === 'login';
  }

  render() {
    return (
      <div>
        <header className='circle--header'>
          <div className='bounds'>
            <div className='circle--fluid'>
              <div className='circle--fluid--cell circle--fluid--primary'>
                <ul className='circle--inline'>
                  <li><img src={logo} alt='Logo' height='60px'/></li>
                </ul>
                {
                  TokenAuth.loggedIn() &&
                    // eslint-disable-next-line
                    <a href="# " onClick={this.handleLogoutClick}>Logout {TokenAuth.getUsername()}</a>
                }
              </div>
              <div className='circle--fluid--cell circle--fluid--secondary'>
                {TokenAuth.loggedIn() && <nav>
                  <ul className='circle--inline'>
                    <li key='0' className={this.state.viewName === 'liked' ? 'current-tab' : ''}>
                      <a onClick={this.setView.bind(this, 'liked')}>Liked</a>
                    </li>
                    <li key='1' className={this.state.viewName === 'undecided' ? 'current-tab' : ''}>
                      <a onClick={this.setView.bind(this, 'undecided')}>Undecided</a>
                    </li>
                    <li key='2' className={this.state.viewName === 'disliked' ? 'current-tab' : ''}>
                      <a onClick={this.setView.bind(this, 'disliked')}>Disliked</a>
                    </li>
                    <li key='3' className={this.state.viewName === 'new' ? 'current-tab' : ''}>
                      <a className={'button-link'} onClick={this.setView.bind(this, 'new')}>Add New Dog</a>
                    </li>
                  </ul>
                </nav>}
              </div>
            </div>
          </div>
        </header>
        <div className='bounds'>
          <div className='grid-60 centered'>{this.state.view}</div>
        </div>
      </div>
    );
  }
}