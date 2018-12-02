import "babel-polyfill";
import $ from "jquery";

import React from "react";
import ReactDOM from "react-dom";

import { Dropdown, Button, NavItem, Modal } from "react-materialize";

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

const Blurb = () => ( //make welcome blurb
  <p>Welcome! Blah blah</p>
);

/*
class Instructions extends React.Component {
  render() {
    return (
      <ul>
        <li>Please select the type of graph you would like to tikzify: </li>
        <li>Please ... </li>
      </ul>
    );
  }
}



*/

/*  */
$(document).ready(() => {
  ReactDOM.render(
    <div>
      <h1>Graphikz</h1>
      <Blurb />
      <Modal
        header='Modal Header'
        trigger={<Button>MODAL</Button>}>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum</p>
      </Modal>
      <Dropdown trigger={ <Button>Drop me!</Button> }>
        <NavItem>Thing 1</NavItem>
        <NavItem>Thing 2</NavItem>
      </Dropdown>
    </div>,
      //<Hannah number={1} />
      //<Hannah number={2} />
    //</div>,
    document.getElementById("root")
  );
});
