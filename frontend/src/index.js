import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

import './css/global.css';
import './css/custom.css';
import './scss/index.scss';
// import './scss/base.scss';
// import './scss/styles.scss';

import PugOrUgh from './components/app';
import * as serviceWorker from './serviceWorker';

axios.defaults.baseURL = 'http://127.0.0.1:8000';

ReactDOM.render(<PugOrUgh />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
