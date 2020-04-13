 //for feather icons
 feather.replace()

 //Toogle sidebar - mobile devices
 nav = document.querySelector('#sidenav')

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