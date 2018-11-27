import "babel-polyfill";
import $ from "jquery";

import React from "react";
import ReactDOM from "react-dom";

import Hannah from "./hannah";

$(document).ready(() => {
  ReactDOM.render(
    <div><h1>Graphikz</h1></div>,
      //<Hannah number={1} />
      //<Hannah number={2} />
    //</div>,
    document.getElementById("root")
  );
});
