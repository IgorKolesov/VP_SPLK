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
};


function disable_menu_item(){
    let nav = document.querySelector('.nav_panel')
    let menu_items = nav.querySelectorAll('.nav_item')

    menu_items.forEach(item => {
        if (item.pathname == window.location.pathname){
            item.classList.add('active_page_link')
        }
    })
};


document.addEventListener('DOMContentLoaded', () => {
    toogle_menu();
    disable_menu_item();

    const swiper = new Swiper('.supplies_swiper', {
        // Optional parameters
        direction: 'horizontal',
        autoheight: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: true,
        },

        slidesPerView: 2.1,
        spaceBetween: 30,
        centeredSlidesBounds: true,
        autoheight: true,
        stopOnLastSlide: true,

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

        pagination: {
            el: '.swiper-pagination',
        },

    });
});
