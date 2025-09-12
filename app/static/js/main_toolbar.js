import {clearPhraseItems} from "./phrase_toolbar.js"

export function initMainToolbar(){
    const menuContent = document.getElementById('menu-content');
    const menu = document.getElementById('hamburger');

    window.onMainMenuClick = function (e) {
        if (!menuContent) return; // safety check

        // Toggle the active class
        menuContent.classList.toggle('active');

        // Optional: stop click from bubbling if needed
        event.stopPropagation();
    }

    // Close menu if clicking outside
    document.addEventListener('click', (e) => {
        if(menuContent){
            if (!menuContent.contains(e.target) && e.target !== menu) {
                menuContent.classList.remove('active');
            }
        }
    });

    // Close menu when clicking a menu item
    document.querySelectorAll('.menu-item, .menu-item-child').forEach(item => {
        item.addEventListener('click', () => {
            menuContent.classList.remove('active');
        });
    });

    window.onMenuClick = function (route) {
        if(route == "logout"){
            fetch(`${route}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },

            })
            .then(response => response.json())
            .then(response => {
                if(response.logged_out)
                    clearPhraseItems()
                    window.location.href = "/auth/login";
            })
            .catch(err => {
                console.error("Logout error:", err);
            });;
        }
        else
            window.location.href = `/main/${route}`;
    };
}

export function doSmth() {
    return JSON.parse(sessionStorage.getItem(SESSION_KEY) || "[]");
}