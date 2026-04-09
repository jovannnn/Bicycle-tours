/*Скрипта за хамбургер менито */
document.getElementById('menu-icon').addEventListener('click', function() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('active'); 
});
