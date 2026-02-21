const sidebar = document.querySelector('#sidebar');
const toggle = document.querySelector('#toggle');
const main = document.querySelector('main');

toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close');
})