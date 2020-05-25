import React from 'react';
import axios from 'axios';
import styled from 'styled-components'

import TokenAuth from '../lib/token-auth';

// TODO: check this
const Err = styled.p`
  font-family: 'Josefin Sans', sans-serif;
  font-size: 1em;
  margin-bottom: 0.9em;
  margin-left: 0.5em;
  color: red;
`;


export default class DogForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      message: '',
      errors: {},
      name: 'test',
      image_filename: '',
      image: null,
      breed: 'test',
      age: '-1',
      gender: 'u',
      size: 'u',
      type: 'm',
      favorite_cat_food: '',
      french_films: false,
      chicken_noises: false,
      is_robot: false,
      is_carl_sagan: false,
    };

    this.inputChangeHandler = this.inputChangeHandler.bind(this);
    this.fileSelectedHandler = this.fileSelectedHandler.bind(this);
    this.submitHandler = this.submitHandler.bind(this);
  }

  submitHandler(event) {
    const url = 'api/dog/new/';
    let formData = new FormData();
    formData.append('image_filename', this.state.image_filename);
    formData.append('image', this.state.image, this.state.image.name);

    formData.append('name', this.state.name);
    formData.append('breed', this.state.breed);
    formData.append('age', this.state.age);
    formData.append('gender', this.state.gender);
    formData.append('size', this.state.size);
    formData.append('type', this.getType());
    formData.append('favorite_cat_food', this.state.favorite_cat_food);
    formData.append('french_films', this.state.french_films);
    formData.append('chicken_noises', this.state.chicken_noises);
    formData.append('is_robot', this.state.is_robot);
    formData.append('is_carl_sagan', this.state.is_carl_sagan);

    axios.post(url, formData, {
      // headers: {'content-type': 'multipart/form-data'}
      headers: TokenAuth.getAuthHeader()
    }).then(response => {
      // sets view with id - 1 to get new dog with getNext
      this.props.setView('undecided', response.data.id - 1);
    }).catch(error => {
      if (error.response) {
        const messages = Object.values(error.response.data);
        for (const errorMessage of messages) {
          console.log(errorMessage);
        }
        this.setState({errors: error.response.data});
      } else {
        console.log(error);
      }
    });
  }

  inputChangeHandler(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  fileSelectedHandler(event) {
    this.setState({
      image: event.target.files[0],
      image_filename: event.target.files[0].name
    });
  }

  getType() {
    if (this.state.is_robot) {
      return 'r';
    }
    else {
      return 'm';
    }
  }

  disabled() {
    return (
      !this.state.name ||
      !this.state.breed ||
      !this.state.age ||
      !this.state.gender ||
      !this.state.size ||
      !this.state.image
    );
  }

  render() {
    return (
      <div>
        <h4>New Dog Registration</h4>
        <p className="text-centered">{this.state.message}</p>
        <h5>Please upload a photo of the dog:</h5>
        <input
          type="file"
          name="image"
          accept="image/*"
          onChange={this.fileSelectedHandler}
          required/>
        {this.state.errors['image'] && <Err>{this.state.errors['image']}</Err>}
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={this.state.name}
          onChange={this.inputChangeHandler}
        />
        {this.state.errors['name'] && <Err>{this.state.errors['name']}</Err>}
        <input
          type="text"
          name="breed"
          placeholder="Breed"
          value={this.state.breed}
          onChange={this.inputChangeHandler}
        />
        {this.state.errors['breed'] && <Err>{this.state.errors['breed']}</Err>}
        <input
          type="number"
          name="age"
          placeholder="Age (in months)"
          min="0"
          value={this.state.age}
          onChange={this.inputChangeHandler}
        />
        {this.state.errors && <Err>{this.state.errors['age']}</Err>}
        <div>
          <h5>Gender:</h5>
          <input
            type="radio"
            name="gender"
            value="m"
            checked={this.state.gender === "m"}
            onChange={this.inputChangeHandler}
          /> Male<br/>
          <input
            type="radio"
            name="gender"
            value="f"
            checked={this.state.gender === "f"}
            onChange={this.inputChangeHandler}
          /> Female<br/>
          <input
            type="radio"
            name="gender"
            value="u"
            checked={this.state.gender === "u"}
            onChange={this.inputChangeHandler}
          /> Unknown
        </div>
        <div>
          <h5>Size:</h5>
          <input
            type="radio"
            name="size"
            value="s"
            checked={this.state.size === "s"}
            onChange={this.inputChangeHandler}
          /> Small<br/>
          <input
            type="radio"
            name="size"
            value="m"
            checked={this.state.size === "m"}
            onChange={this.inputChangeHandler}
          /> Medium<br/>
          <input
            type="radio"
            name="size"
            value="l"
            checked={this.state.size === "l"}
            onChange={this.inputChangeHandler}
          /> Large<br/>
          <input
            type="radio"
            name="size"
            value="xl"
            checked={this.state.size === "xl"}
            onChange={this.inputChangeHandler}
          /> Extra Large<br/>
          <input
            type="radio"
            name="size"
            value="u"
            checked={this.state.size === "u"}
            onChange={this.inputChangeHandler}
          /> Unknown
        </div>
        <div>
          <h5>Optional information:</h5>
          <p><small>This information is optional, but the more information we have, the better chance we have of finding
            this dog a new home!</small></p>
          <input
            type="text"
            name="favorite_cat_food"
            placeholder="Favorite brand of cat food"
            value={this.state.favorite_cat_food}
            onChange={this.inputChangeHandler}
          />
          <div>
            <input
              type="checkbox"
              name="french_films"
              checked={this.state.french_films}
              onChange={this.inputChangeHandler}
            /> Likes classy French films<br/>
          </div>
          <div>
            <input
              type="checkbox"
              name="chicken_noises"
              checked={this.state.chicken_noises}
              onChange={this.inputChangeHandler}
            /> Is unafraid to express its feelings through interpretive dance and high-pitched chicken noises<br/>
          </div>
          <div>
            <input
              type="checkbox"
              name="is_robot"
              id="is_robot"
              checked={this.state.is_robot}
              onChange={this.inputChangeHandler}
            /> Is actually a robot<br/>
          </div>
          <div hidden={!this.state.is_robot}>
            <input
              type="checkbox"
              hidden={this.state.is_robot}
            /> Is from the future (we're just curious)<br/>
          </div>
          <div>
            <input
              type='checkbox'
              name='is_carl_sagan'
              checked={this.state.is_carl_sagan}
              onChange={this.inputChangeHandler}
            /> Is Carl Sagan
          </div>
        </div>
        <button className="button" onClick={this.submitHandler} disabled={this.disabled()}>Submit</button>
      </div>
    )
  }
}