// edit.js
import { selectedCards } from "./actions_toolbar.js";
import { updateActionsToolbarIcon, getScreenName } from "./utils.js";

export function initEdit() {
    const editForm = document.getElementById("edit-form");
    const editPopup = document.getElementById("edit-popup");
    const editNameInput = document.getElementById("edit-name");
    const editIconInput = document.getElementById("edit-icon");
    const editPreview = document.getElementById("edit-icon-preview");
    const editBtn = document.getElementById("edit-btn");

    if (editBtn && editForm && editPopup) {
        // Open popup when Edit clicked
        editBtn.addEventListener("click", function (e) {
            e.preventDefault(); // stop form submission
            if (selectedCards.size !== 1) return;

            const categoryId = Array.from(selectedCards)[0];
            const card = document.querySelector(`.custom-card[data-id="${categoryId}"]`);
            if (!card) return;

            // Prefill with current name
            editNameInput.value = card.querySelector(".card-text")?.innerText.trim() || "";

            // Prefill with current icon
            const currentIcon = card.querySelector("img")?.getAttribute("src");
            if (currentIcon) {
                editPreview.src = currentIcon;
                editPreview.style.display = "block";
            } else {
                editPreview.style.display = "none";
            }

            // Show popup
            editPopup.style.display = "flex";
        });

        // Live preview when selecting new icon
        editIconInput.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = e => {
                    editPreview.src = e.target.result;
                    editPreview.style.display = "block";
                };
                reader.readAsDataURL(file);
            }
        });

        // Submit edit
        editForm.addEventListener("submit", function (e) {
            e.preventDefault();
            if (selectedCards.size !== 1) return;

            // Check if both fields are empty
            const nameEmpty = !editNameInput.value.trim();
            const iconEmpty = !editIconInput.files.length;

            // Show error only if both are empty
            if (nameEmpty && iconEmpty) {
                if (nameEmpty) editNameInput.setCustomValidity("Please fill out name or icon.");
                if (iconEmpty) editIconInput.setCustomValidity("Please fill out name or icon.");

                editNameInput.reportValidity();
                editIconInput.reportValidity();
                return;
            }

            // Clear any previous custom validity
            editNameInput.setCustomValidity("");
            editIconInput.setCustomValidity("");

            const itemId = Array.from(selectedCards)[0];
            const formData = new FormData(editForm);
            formData.append("selected_item", itemId);
            formData.append("type", getScreenName() == "home" ? "category" : "communication_items" );

            fetch("/actions_toolbar/edit_selected", {
                method: "POST",
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Replace card with updated HTML
                        const oldCard = document.querySelector(`.custom-card[data-id="${itemId}"]`);
                        if (oldCard) {
                            oldCard.insertAdjacentHTML("beforebegin", data.html);
                            oldCard.remove();
                        }
                        selectedCards.clear();
                        updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
                        editPopup.style.display = "none";
                    } else {
                        alert("Edit failed: " + (data.error || "Unknown error"));
                    }
                })
                .catch(err => {
                    console.error("Edit error:", err);
                    alert("Error editing category. Check console.");
                });
        });
    }
}