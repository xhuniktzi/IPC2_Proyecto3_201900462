const byDateForm = document.getElementById('by-date-form');
const byDateResults = document.getElementById('by-date-results');
const byErrorForm = document.getElementById('by-error-form');
const byErrorResults = document.getElementById('by-error-results');

byDateForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const date = byDateForm.elements['date'].value;
  const url = `http://localhost:5000/stats/by_date?date=${date}`;
  fetch(url, {
    method: 'GET',
  })
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
      })
      .then((resJson) => {
        console.log(resJson);
        for (const element of resJson.data) {
          const percentage = Math.floor((element.cant / resJson.total)*100);

          const label = document.createElement('div');
          // eslint-disable-next-line max-len
          label.innerHTML = `${element.user} - ${element.cant} / ${resJson.total}`;
          byDateResults.appendChild(label);

          const bar = document.createElement('div');
          bar.classList.add('progress');
          byDateResults.appendChild(bar);

          const progressBar = document.createElement('div');
          progressBar.classList.add('progress-bar');
          progressBar.setAttribute('role', 'progressbar');
          progressBar.style = `width: ${percentage}%;`;
          progressBar.setAttribute('aria-valuenow', percentage);
          progressBar.setAttribute('aria-valuemin', 0);
          progressBar.setAttribute('aria-valuemax', 100);
          progressBar.innerHTML = `${percentage}%`;
          bar.appendChild(progressBar);
        }
      });
});

byErrorForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const error = byErrorForm.elements['error'].value;
  const url = `http://localhost:5000/stats/by_error?error=${error}`;
  fetch(url, {
    method: 'GET',
  })
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
      })
      .then((resJson) => {
        for (const element of resJson.data) {
          const percentage = Math.floor((element.cant / resJson.total)*100);

          const label = document.createElement('div');
          // eslint-disable-next-line max-len
          label.innerHTML = `${element.date} - ${element.cant} / ${resJson.total}`;
          byErrorResults.appendChild(label);

          const bar = document.createElement('div');
          bar.classList.add('progress');
          byErrorResults.appendChild(bar);

          const progressBar = document.createElement('div');
          progressBar.classList.add('progress-bar');
          progressBar.setAttribute('role', 'progressbar');
          progressBar.style = `width: ${percentage}%;`;
          progressBar.setAttribute('aria-valuenow', percentage);
          progressBar.setAttribute('aria-valuemin', 0);
          progressBar.setAttribute('aria-valuemax', 100);
          progressBar.innerHTML = `${percentage}%`;
          bar.appendChild(progressBar);
        }
      });
});
