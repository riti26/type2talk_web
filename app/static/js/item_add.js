// category.js
import { updateActionsToolbarIcon } from "./utils.js";
import { selectedCards, totalCardsLength } from "./actions_toolbar.js";

export function initAddItemForm() {
    const form = document.getElementById("category-form");
    const container = document.querySelector(".cards-grid");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent normal form submission

        const formData = new FormData(form);

        // Ensure is_standalone is set
        const radios = document.querySelectorAll('input[name="is_standalone"]');
        let selected = false;
        radios.forEach(r => {
            if (r.checked) {
                formData.set("is_standalone", r.value);
                selected = true;
            }
        });
        if (!selected) {
            alert("Please select a category type (Work or Folder).");
            return;
        }

        fetch("/actions_toolbar/add_item", {
            method: "POST",
            body: formData
        })
        .then(resp => resp.json())
        .then(data => {
        if (data.success && container) {
            container.insertAdjacentHTML("beforeend", data.html); // prepend to grid

            // alert("Data added successfully!");  <-- remove this line

            form.reset();
            closePopup();
        } else {
            alert("Failed to create category: " + (data.error || "Unknown error"));
        }
    })
        .catch(err => {
            console.error("Error adding category:", err);
            alert("Error adding category. Check console for details.");
        });
    });
}
