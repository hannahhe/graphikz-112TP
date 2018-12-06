import "babel-polyfill";
import $ from "jquery";

import React from "react";
import ReactDOM from "react-dom";
import Clipboard from "clipboard";

import { Dropdown, Button, NavItem, Modal, Row, Input } from "react-materialize";

import Hannah from "./hannah";

/*
// uncool way to do it
function Blurb() {
  return <p>Welcome! Blah blah</p>
}

// cool alternative way to do it
const Blurb = () => {
  return <p>Welcome! Blah blah</p>;
}
*/
const clipboardRef = elem => {
  if (elem) { new Clipboard(elem) }
};

const Welcome = () => ( //make welcome blurb
  <p>Welcome!</p>
);


class UserInput extends React.Component {
  //define constructor here
  constructor(props) {
    super(props);
    this.state = {};
  }

  onChange = (e, val) => { //defines a function, onChange which takes an event and value and takes value and stores it in something
    this.state.graph_mode = val; //storing
  }

  getUploadedFileName = (e) => {  //get the file
    let files = e.target.files,
        value = e.target.value;
    var formData = new FormData();

    formData.append('GraphImage', files[0]);
    formData.append('GraphType', this.state.graph_mode);


    fetch('/graph', { //http put request
      method: 'PUT',
      body: formData
    })
    .then(response => response.json()) //get back a json
    .catch(error => console.error(error)) //error handling
    .then(response => {
      this.state.laTeX = response.latex;
      console.log(this.state.laTeX);
      console.log(this.state);
      this.forceUpdate();
    }); //if the json is valid
  }

  render() {
    return (
      <div>
        <Row>
         <ul>
          <li>Please select the type of graph you would like to tikzify:</li>
         </ul>
          <Input s={12} type='select' label="Pick your graph type..." defaultValue='1'
            onChange={ this.onChange }>
            <option value='1'>Select...</option>
            <option value='Scatter Plot'>Scatter Plot</option>
            <option value='Graph Theory'>Graph Theory</option>
          </Input>
        </Row>
        <Row>
         <ul>
          <li>Please upload your graph file:</li>
         </ul>
          <Input type="file" label="Upload File" s={12}
          onChange={this.getUploadedFileName} />
        </Row>
        <Row>
        <ul>
         <li>It's ready! Please copy your LaTeX Code and paste it into your project!:</li>
        </ul>
          <Button><i className="fa fa-clipboard" aria-hidden="true" /> <a className = 'white-text' ref={ clipboardRef } data-clipboard-text={this.state.laTeX}>Copy LaTeX</a></Button>
        </Row>
      </div>
    );
  }
}


/*  */
$(document).ready(() => {
  ReactDOM.render(
    <div>
      <h1 className='title'>\Graphikz[]</h1>
      <Welcome />
      <UserInput />

    </div>,
      //<Hannah number={1} />
      //<Hannah number={2} />
    //</div>,
    document.getElementById("root")
  );
});
