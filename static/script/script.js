//for feather icons
feather.replace()

//Toogle sidebar - mobile devices
nav = document.querySelector("#sidenav")
navIcon = document.querySelector("#nav-icon")
gridContainer = document.querySelector(".grid-container")
formContent = document.querySelector(".form-content")
loginPage = document.querySelector("#login-page")
signupPage = document.querySelector("#signup-page")

let urlAtual = window.location.href
let recuperarSenhaDeslogado = false

if (urlAtual.includes("redefinirsenha?token")) {
    recuperarSenhaDeslogado = true

    nav.style.width = "0"
    // sem item de logout pra página redefinir senha
    navIcon.parentNode.removeChild(navIcon)
}

if (!loginPage || !signupPage || !recuperarSenhaDeslogado) {
    nav.classList.add("active")
}

if (loginPage) {
    gridContainer.setAttribute("id", "login-page__container")
    formContent.setAttribute("id", "login-page__form")

    // sem item de logout pra páginas iniciais
    navIcon.parentNode.removeChild(navIcon)
}

if (signupPage) {
    nav.style.width = "0"
    gridContainer.setAttribute("id", "signup-page__container")
    formContent.setAttribute("id", "signup-page__form")

    navIcon.parentNode.removeChild(navIcon)
}

// abrir e fechar navegação no mobile
function openNav() {
    nav.classList.toggle("active")
}
function closeNav() {
    nav.classList.toggle("active")
}

const close = document.querySelector("[closeNav]")
close.onclick = closeNav
const open = document.querySelector("[openNav]")
open.onclick = openNav
