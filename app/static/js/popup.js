import { getScreenName, getLastPathSegment } from "./utils.js";

export function initPopups() {
    const popup = document.getElementById("category-popup");
    if (!popup) return;

    const title = document.getElementById("popup-title");
    const form = document.getElementById("popup-form");
    const categoryInput = document.getElementById("item-category-id");
    const container = document.querySelector(".cards-grid");


    // ---------------- Category popup ----------------
    window.openPopup = function () {
        screen = getScreenName(); 
        if(screen == "home"){
            title.textContent = "Add New Category";
            form.action = "/actions_toolbar/add_item"; 

            // Show category-only fields
            document.querySelectorAll(".category-field").forEach(el => el.style.display = "block");

            // Clear hidden category input
            categoryInput.value = "";
        }
        else if (screen == "communication-items"){
            title.textContent = "Add New Item";
            form.action = "/actions_toolbar/add_communication_item";

            // Hide category-only fields
            document.querySelectorAll(".category-field").forEach(el => el.style.display = "none");

            categoryInput.value = getLastPathSegment();
        }

        popup.style.display = "flex";
    };

    // ---------------- Close popup ----------------
    window.closePopup = function () {
        popup.style.display = "none";
        form.reset();
    };

    // ---------------- Submit handler ----------------
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // prevent browser default submission
        if (!container) return;

        const formData = new FormData(form);

        // Ensure category type is set when adding category
        if (form.action.includes("add_item")) {
            const radios = document.querySelectorAll('input[name="is_standalone"]');
            let selected = false;
            radios.forEach(r => {
                if (r.checked) {
                    formData.set("is_standalone", r.value);
                    selected = true;
                }
            });
            if (!selected) {
                alert("Please select a category type (Word or Folder).");
                return;
            }
        }

        fetch(form.action, { method: "POST", body: formData })
            .then(resp => resp.json())
            .then(data => {
                if (data.success && data.html) {
                    container.insertAdjacentHTML("beforeend", data.html);
                    form.reset();
                    popup.style.display = "none";
                } else {
                    alert("Failed to create: " + (data.error || "Unknown error"));
                }
            })
            .catch(err => {
                console.error("Error submitting form:", err);
                alert("Error submitting form. Check console.");
            });
    });
}
