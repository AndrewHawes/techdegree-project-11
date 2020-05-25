import React from 'react';
import PropTypes from 'prop-types';


export default class CheckboxGroup extends React.Component {
  constructor(props) {
    super(props);

    this.checkboxClicked = this.checkboxClicked.bind(this);
  }
  checkboxClicked(value, event) {
    if (event.target.checked) {
      this.props.data.add(value);
    } else {
      if(this.props.atLeastOne && this.props.data.size <= 1) {
        return;
      }
      this.props.data.delete(value);
    }
    this.props.onChange(this.props.data);
  }

  render() {
    return (
      <div>
        <h5>{this.props.title}</h5>
        {this.props.checkboxes.map(function(p) {
          return (
            <label key={p.value}>
              <input
                type="checkbox"
                checked={this.props.data.has(p.value)}
                onChange={this.checkboxClicked.bind(this, p.value)}
              />
              <span className='label-body'>{p.label}</span>
            </label>
          );
        }, this)}
      </div>
    );
  }
}

CheckboxGroup.propTypes = {
  title: PropTypes.node.isRequired,
  checkboxes: PropTypes.arrayOf(function(propValue, key, componentName, location, propFullName) {
    if (!propValue[key].hasOwnProperty('label') || !propValue[key].hasOwnProperty('value')) {
      return new Error("'checkboxes' items are missing properties for 'label' or 'value'");
    }
  }).isRequired,
  data: PropTypes.instanceOf(Set).isRequired,
  onChange: PropTypes.func.isRequired,
  atLeastOne: PropTypes.bool,
};

CheckboxGroup.defaultProps = {
  atLeastOne: false
};