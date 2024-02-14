const menuButton = document.querySelector('.menuBtn')
        const menuButtonIcon = document.querySelector('.menuBtn a')
        const accountMenuButton = document.querySelector('.accountMenu')

        menuButton.onClick = function () {
            accountMenuButton.classList.toggle('open')
        }