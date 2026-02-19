const sidebar = document.querySelector('#sidebar');
const toggle = document.querySelector('#toggle');
const main = document.querySelector('main');

toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close');

    if (sidebar.classList.contains('close')) {
        main.style.marginLeft = '4rem'
    } else {
        main.style.marginLeft = '12rem'
    }
})