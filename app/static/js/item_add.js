// item_add.js
import { updateActionsToolbarIcon } from "./utils.js";
import { selectedCards, totalCardsLength } from "./actions_toolbar.js";

export function initAddItemForm() {
    // Only run this code on /main/home
    if (window.location.pathname !== "/main/home") return;

    const form = document.getElementById("category-form");
    const container = document.querySelector(".cards-grid");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

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
                container.insertAdjacentHTML("beforeend", data.html);

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
// item.js
export function initAddCommunicationItemForm() {
    const path = window.location.pathname;
    const itemPathRegex = /^\/main\/communication-items\/(\d+)$/;
    const match = path.match(itemPathRegex);

    if (!match) return; // only run on /main/communication-items/:id
    const categoryId = match[1];

    const form = document.getElementById("item-form");
    const container = document.querySelector(".cards-grid");
    const header = document.getElementById("item-popup-title");

    if (!form) return;

    // Update popup header text
    if (header) {
        header.innerText = "Add New Item";
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        formData.set("category_id", categoryId); // add category id

        fetch("/actions_toolbar/add_communication_item", {
            method: "POST",
            body: formData
        })
        .then(resp => resp.json())
        .then(data => {
            if (data.success && container) {
                container.insertAdjacentHTML("beforeend", data.html);

                form.reset();
                closeItemPopup();
            } else {
                alert("Failed to create item: " + (data.error || "Unknown error"));
            }
        })
        .catch(err => {
            console.error("Error adding item:", err);
            alert("Error adding item. Check console for details.");
        });
    });
}

