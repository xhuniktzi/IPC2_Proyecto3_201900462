/* eslint-disable require-jsdoc */
const inputTextArea = document.getElementById('input');
const outputTextArea = document.getElementById('output');
const buttonSend = document.getElementById('send-button');

getStatsXML();

buttonSend.addEventListener('click', (e) => {
  const url = 'http://localhost:5000/events';
  fetch(url, {
    method: 'POST',
    body: inputTextArea.value,
  })
      .then((res) => {
        if (res.ok) {
          getStatsXML();
        }
      });
});

function getStatsXML() {
  const url = 'http://localhost:5000/stats';
  fetch(url, {
    method: 'GET',
  })
      .then((res) => {
        if (res.ok) {
          return res.text();
        }
      })
      .then((resText) => {
        outputTextArea.value = resText;
      });
}
