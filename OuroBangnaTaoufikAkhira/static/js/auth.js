const sidebarToggle = document.getElementById('sidebar-toggle')
const sidebar = document.getElementById('sidebar')
const content = document.getElementById('content')

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed')
    content.classList.toggle('expanded')
})

const profileDropdown = document.getElementById('profile-dropdown')
const dropdownMenu = document.getElementById('dropdown-menu')

profileDropdown.addEventListener('click', (e) => {
    e.stopPropagation()
    dropdownMenu.classList.toggle('show')
})

document.addEventListener('click', () => {
    dropdownMenu.classList.remove('show')
})

dropdownMenu.addEventListener('click', (e) => {
    e.stopPropagation()
})