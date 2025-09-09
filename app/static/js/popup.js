// popup.js
export function initPopups() {
    window.openCategoryPopup = function () {
        document.getElementById("category-popup").style.display = "flex";
    };

    window.closePopup = function () {
        document.getElementById("category-popup").style.display = "none";
    };
}
