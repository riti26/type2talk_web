// delete.js
import { selectedCards } from "./actions_toolbar.js";
import { updateActionsToolbarIcon, getScreenName } from "./utils.js";

export function initDelete() {
    const deleteForm = document.querySelector('form[action$="delete_selected"]');
    const deletePopup = document.getElementById("delete-confirm-popup");
    const deleteYes = document.getElementById("delete-confirm-yes");
    const deleteNo = document.getElementById("delete-confirm-no");

    if (deleteForm && deletePopup) {
        deleteForm.addEventListener("submit", function(e) {
            e.preventDefault();
            if (selectedCards.size === 0) return;
            deletePopup.style.display = "flex";
        });

        deleteYes.addEventListener("click", function() {
            fetch("/actions_toolbar/delete_selected", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ cardType: getScreenName() == "home" ? "category" : "communication_items", selected_items: Array.from(selectedCards) })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    Array.from(selectedCards).forEach(id => {
                        const card = document.querySelector(`.custom-card[data-id="${id}"]`);
                        if (card) card.remove();
                    });
                    selectedCards.clear();
                    updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
                } else {
                    alert("Failed to delete: " + (data.error || "Unknown error"));
                }
                deletePopup.style.display = "none";
            })
            .catch(err => {
                console.error("Delete error:", err);
                alert("Error deleting categories. Check console.");
                deletePopup.style.display = "none";
            });
        });

        deleteNo.addEventListener("click", function() {
            deletePopup.style.display = "none";
        });
    }
}
