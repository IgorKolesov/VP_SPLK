function toogle_menu(){
    let nav = document.querySelector('.nav_panel')
    let toogle_btn = nav.querySelector('.toggle_btn')

    let menuState = localStorage.getItem('menuState');
    if (menuState === 'closed') {
        nav.style.transition = 'none';
        nav.classList.add('toggle');
        setTimeout(function() { nav.style.transition = '';}, 500)
    }

    toogle_btn.addEventListener('click', function() {
        nav.classList.toggle('toggle');

        if (nav.classList.contains('toggle')) {
            localStorage.setItem('menuState', 'closed');
        } else {
            localStorage.setItem('menuState', 'open');
        }
    })
}

toogle_menu()