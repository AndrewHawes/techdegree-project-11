import React from 'react';
import axios from 'axios';
import TokenAuth from '../lib/token-auth';

import CheckboxGroup from './checkboxGroup';


export default class Preferences extends React.Component {
  constructor(props) {
    super(props);

    this.state = {data: {}, loaded: false};

    this.handleCheckboxGroupDataChanged = this.handleCheckboxGroupDataChanged.bind(this);
    this.save = this.save.bind(this);
  }

  componentDidMount() {
    axios.get('api/user/preferences/', {headers: TokenAuth.getAuthHeader()})
      .then(response => {
        const data = {
          age: new Set(response.data.age.split(',')),
          gender: new Set(response.data.gender.split(",")),
          size: new Set(response.data.size.split(",")),
          type: new Set(response.data.type.split(",")),
        };
        this.setState({data: data, loaded: true});
      });
  }

  componentWillUnmount() {
    // this.serverRequest.abort();
  }

  handleCheckboxGroupDataChanged(property, data) {
    this.setState({[property]: data});
  }

  save() {
    const json = JSON.stringify({
      age: Array.from(this.state.data.age).join(','),
      gender: Array.from(this.state.data.gender).join(','),
      size: Array.from(this.state.data.size).join(','),
      type: Array.from(this.state.data.type).join(',')
    });
    const url = 'api/user/preferences/';

    axios.put(url, json, {
      headers: {
        'Content-type': 'application/json',
        ...TokenAuth.getAuthHeader()
      }
    })
      .then(response => this.props.setView('undecided'))
      .catch(error => console.log(error.message));
  }

  render() {
    if (!this.state.loaded) {
      return null;
    }

    return (
      <div>
        <h4>Set Preferences</h4>
        <CheckboxGroup
          title="Gender"
          checkboxes={[
            {label: "Male", value: "m"},
            {label: "Female", value: "f"},
          ]}
          data={this.state.data.gender}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'gender')}
          atLeastOne={true}
        />
        <CheckboxGroup
          title="Age"
          checkboxes={[
            {label: "Baby", value: "b"},
            {label: "Young", value: "y"},
            {label: "Adult", value: "a"},
            {label: "Senior", value: "s"}
          ]}
          data={this.state.data.age}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'age')}
          atLeastOne={true}
        />
        <CheckboxGroup
          title="Size"
          checkboxes={[
            {label: "Small", value: "s"},
            {label: "Medium", value: "m"},
            {label: "Large", value: "l"},
            {label: "Extra Large", value: "xl"}
          ]}
          data={this.state.data.size}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'size')}
          atLeastOne={true}
        />
        <CheckboxGroup
          title="Type"
          checkboxes={[
            {label: "Mammal", value: "m"},
            {label: "Robot", value: "r"},
          ]}
          data={this.state.data.type}
          onChange={this.handleCheckboxGroupDataChanged.bind(this, 'type')}
          atLeastOne={true}
        />
        <hr/>
        <button className="button" onClick={this.save}>Save</button>
      </div>
    );
  }
}
