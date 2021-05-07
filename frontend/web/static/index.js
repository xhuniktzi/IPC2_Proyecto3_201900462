const resetButton = document.getElementById('reset-button');
const input = document.getElementById('input');
const documentInput = document.getElementById('document');

resetButton.addEventListener('click', (e) => {
  const url = 'http://localhost:5000/reset';
  fetch(url, {
    method: 'PATCH',
  })
      .then(
          location.reload(),
      );
});

documentInput.addEventListener('change', (e)=> {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.readAsText(file);
  reader.addEventListener('load', (e) => {
    input.innerHTML = reader.result;
  });
});
