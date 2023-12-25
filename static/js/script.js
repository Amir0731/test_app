let body = document.body;
// let checkbox = document.querySelector('.form-check-input')
let themeIcon = document.querySelector('.theme_icon')
let img_modal_box = document.querySelector('.model_img')

function Change() {
    theme = localStorage.getItem('theme')
    if (theme) {
        body.dataset.bsTheme = theme
        themeIcon.src = theme === 'dark' ? '/media/icon-moon.svg' : '/media/icon-sun.svg'
    } else {
        localStorage.setItem('theme', 'dark')
        body.dataset.bsTheme = localStorage.getItem(('theme'))
        themeIcon.src = '/media/icon-moon.svg'
    }
    // condition = localStorage.getItem(('theme'))
    // checkbox.checked = condition === 'light' ? false : true
}

Change()

function myFunction(el) {
    // console.log(el.target.dataset.themeValue)
    localStorage.setItem('theme', el.target.dataset.themeValue)
    Change()
}


function openImgModal() {
    img_modal_box.style.display = (img_modal_box.style.display == "none" ? "block" : "none");
}

function closeImgModal(){
    img_modal_box.style.display = 'none'
}