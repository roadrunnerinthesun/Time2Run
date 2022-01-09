'use strict';

function replaceRandomRun(results) {
    document.querySelector('#run-text').innerHTML = results;
  }
  
  function showRandomRun(evt) {
    fetch('/random_run')
      .then(response => response.text())
      .then(replaceRandomRun);
  }
  
document.querySelector('#get-run-button').addEventListener('click', showRandomRun);

