import React from 'react';
import TokenAuth from '../lib/token-auth';
import axios from 'axios';

import Dog from '../components/dog';
import DogControls from '../components/dogControls';
import { MessageBox } from '../components/messageBox';


export default class DogContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {loaded: false};
    this.axios = axios.create({ headers: TokenAuth.getAuthHeader()});

    this.getPrev = this.getPrev.bind(this);
    this.getNext = this.getNext.bind(this);
    this.changeStatus = this.changeStatus.bind(this);
    this.handlePreferencesClick = this.handlePreferencesClick.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
    this.handleHideDog = this.handleHideDog.bind(this);
  }

  componentDidMount() {
    this.getNext(this.props.id);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.filter !== this.props.filter) {
      this.setState({details: undefined, message: undefined, loaded: false}, this.getNext);
    }
  }

  getPrev() {
    if (this.state.details.first) {
      return false;
    }

    const dogId = this.state.details ? this.state.details.id : 1;
    const url = `/api/dog/${dogId}/${this.props.filter}/prev/`;

    this.getDog(url);
  }

  getNext(id) {
    let dogId = (typeof id === 'number') ? id : undefined;
    if (dogId === undefined) {
      dogId = this.state.details ? this.state.details.id : -1;
    }

    const url = `/api/dog/${dogId}/${this.props.filter}/next/`;

    this.getDog(url);
  }

  getDog(url) {
    this.axios.get(url)
      .then(response => this.setState({
        details: response.data,
        message: undefined,
        loaded: true
      }))
      .catch(error => {
        let message = undefined;
        let details = undefined;

        if (error.response) {
          message = error.response.data.detail;

          if (error.response.status === 404) {
            if (message === 'No Results') {
              message = this.props.filter === 'undecided' ?
                'No dogs matched your preferences.' :
                `You don't have any ${this.props.filter} dogs.`;
            } else if (error.response.data.detail === 'Last Entry') {
              message = 'There are no more dogs to view. Come back later.';
              details = null;
            }
          }

          this.setState({
            message: message,
            details: details,
            loaded: true
          });
        } else if (error.request) {
          console.log(error.request);
        } else {
          console.log(error.message);
        }

      });
  }

  changeStatus(newStatus) {
    const url = `api/dog/${ this.state.details.id }/${ newStatus }/`;

    this.axios.put(url)
      .then(response => this.getNext())
      .catch(error => this.setState({ message: error.response.data.detail}));
  }

  handleHideDog(e) {
    const url = `api/dog/${ this.state.details.id }/hide/`;

    this.axios.put(url)
      .then(response => this.getNext())
      .catch(error => this.setState({ message: error.response.data.detail}));
  }

  handlePreferencesClick(e) {
    this.props.setView('preferences');
  }

  handleDelete(e) {
    const url = `api/dog/${ this.state.details.id }/delete/`;
    const successMsg = `${this.state.details.name} successfully deleted.`;

    this.axios.delete(url)
      .then(response => this.setState({ message: successMsg }), this.getNext())
      .catch(error => this.setState({ message: error.response.data.detail }));
  }



  contents() {
    if (!this.state.loaded) {
      return null;
    }

    if (this.state.message !== undefined) {
      return <MessageBox
        details={this.state.details}
        message={this.state.message}
        getNext={this.getNext}
      />;
    }

    const deleteButton = (
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <button className="button" onClick={this.handleDelete}>Delete Dog</button>
      </div>
    );

    const hideDogButton = (
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <button className="button" onClick={this.handleHideDog}>Don't Show Again</button>
      </div>
    );

    const dogControls = (
        <DogControls
          getPrev={this.getPrev}
          changeStatus={this.changeStatus}
          getNext={this.getNext}
          filter={this.props.filter}
        />
    );

    return (
      <div>
        <Dog details={this.state.details} dogControls={dogControls} />
        {this.state.details && this.state.details.can_delete && deleteButton}
        {this.state.details && hideDogButton}
      </div>
  );

  }

  render() {

    return (
      <div>
        {this.contents()}
        <p className="text-centered"><a onClick={this.handlePreferencesClick}>Set Preferences</a></p>
        {/*<p className="text-centered"><button onClick={this.handlePreferencesClick}>Set Preferences</button></p>*/}
      </div>
    );
  }
}

