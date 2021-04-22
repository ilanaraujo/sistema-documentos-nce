 //for feather icons
 feather.replace()

 //Toogle sidebar - mobile devices
 nav = document.querySelector('#sidenav')
 
 loginPage = document.querySelector('#login-page')
 signupPage = document.querySelector('#signup-page')
 gridContainer = document.querySelector('.grid-container')
 formContent = document.querySelector('.form-content')
 navIcon = document.querySelector('#nav-icon')

 //Add and remove provided class names
 function openNav() {
     nav.classList.toggle('active')
 }
 function closeNav() {
     nav.classList.toggle('active')
 }
 const close = document.querySelector('[closeNav]')
 close.onclick = closeNav
 const open = document.querySelector('[openNav]')
 open.onclick = openNav

 if (loginPage) {
    gridContainer.setAttribute('id', 'login-page')
    formContent.setAttribute('id', 'login-page')

    // sem item de logout pra páginas iniciais
    navIcon.parentNode.removeChild(navIcon)
 }

 if (signupPage) {
    gridContainer.setAttribute('id', 'signup-page')
    formContent.setAttribute('id', 'signup-page')

    navIcon.parentNode.removeChild(navIcon)
 }