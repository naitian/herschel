window.onload = function () {
  console.log('hello');
  document.querySelector('div.nav-btn').onclick = function () {
    document.querySelector('nav').classList.toggle('active');
  }
}
