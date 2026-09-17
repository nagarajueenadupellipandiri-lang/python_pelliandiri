(function () {

    /*
     * Get saved theme from this browser.
     * If nothing is saved, use Sky Blue.
     */
    const savedTheme = localStorage.getItem("adminTheme") || "sky";

    document.documentElement.setAttribute(
        "data-theme",
        savedTheme
    );

})();


/*
 * Change theme
 */
function setTheme(theme) {

    document.documentElement.setAttribute(
        "data-theme",
        theme
    );

    /*
     * Save theme in browser localStorage.
     */
    localStorage.setItem(
        "adminTheme",
        theme
    );

    closeThemeMenu();
}


/*
 * Open / close theme menu
 */
function toggleThemeMenu() {

    const menu = document.getElementById("themeMenu");

    if (!menu) {
        return;
    }

    menu.classList.toggle("hidden");
}


/*
 * Close theme menu
 */
function closeThemeMenu() {

    const menu = document.getElementById("themeMenu");

    if (!menu) {
        return;
    }

    menu.classList.add("hidden");
}


/*
 * Close menu when clicking outside
 */
document.addEventListener("click", function (event) {

    const menu = document.getElementById("themeMenu");
    const button = document.getElementById("themeButton");

    if (!menu || !button) {
        return;
    }

    if (
        !menu.contains(event.target) &&
        !button.contains(event.target)
    ) {
        menu.classList.add("hidden");
    }

});
