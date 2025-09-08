document.addEventListener("DOMContentLoaded", function() {
    let selectedCards = new Set();
    let toolbarExpanded = false;
    const totalCardsLenth = document.querySelectorAll(".custom-card").length;
    let selectAll = false;

    // ---------------- Toggle toolbar ----------------
    function toggleToolbar() {
        fetch("/actions_toolbar/toggle_toolbar", {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            toolbarExpanded = data.expanded;
            const toolbar = document.getElementById("actions-toolbar");

            // Show/hide select/edit/delete buttons
            toolbar.querySelectorAll("#select-all-btn, #delete-btn, #edit-btn").forEach(btn => {
                btn.parentElement.style.display = toolbarExpanded ? "inline-block" : "none";
                btn.disabled = !toolbarExpanded;
            });

            // Show/hide add button
            toolbar.querySelector("#add-btn").style.display = toolbarExpanded ? "none" : "inline-block";

            // Clear selections when collapsing
            if (!toolbarExpanded) {
                resetToolbar();
            }

            // Show/hide select icons on each card
            document.querySelectorAll(".custom-card .card-select-icon").forEach(icon => {
                icon.style.display = toolbarExpanded ? "block" : "none";
            });
            updateToolbarIcon()
        });
    }
    window.toggleToolbar = toggleToolbar;

    // ---------------- Popup open/close ----------------
    function openCategoryPopup() {
        document.getElementById("category-popup").style.display = "flex";
    }
    function closePopup() {
        document.getElementById("category-popup").style.display = "none";
    }
    window.openCategoryPopup = openCategoryPopup;
    window.closePopup = closePopup;


    // ---------------- AJAX category creation ----------------
    const form = document.getElementById("category-form");
    const container = document.querySelector(".cards-grid"); // Correct container

    form.addEventListener("submit", function(e) {
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

    // ---------------- Handle single card click ----------------
    function handleCardClick(cardElem, event) {
        if (toolbarExpanded) {
            event.preventDefault(); // prevent navigation

            // Toggle selection in Set
            if (selectedCards.has(cardElem.dataset.id)) {
                selectedCards.delete(cardElem.dataset.id);
            } else {
                selectedCards.add(cardElem.dataset.id);
            }

            
            if (selectedCards.values.length < totalCardsLenth) 
                selectAll = false;

            // Toggle visual selection and icon
            toggleCardSelection(cardElem);

            updateToolbarIcon(); // <--- update toolbar icon
        } else {
            // Toolbar collapsed: navigate
            const url = cardElem.dataset.url;
            window.location.href = url;
        }
    }
    window.handleCardClick = handleCardClick;

    // ---------------- Select all ----------------
    const selectAllForm = document.querySelector('form[action$="select_all"]');
    if (selectAllForm) {
        selectAllForm.addEventListener("submit", function(e) {
            e.preventDefault();
            if (!toolbarExpanded) return;
            selectAll = !selectAll;
            if (!selectAll) {
                selectedCards.clear();
                document.querySelectorAll(".custom-card.selected").forEach(card => {
                card.classList.remove("selected");
                // Reset icon
                const icon = card.querySelector("i");
                if (icon) {
                    icon.classList.remove("fa-check-square");
                    icon.classList.add("fa-square-o");
                }
            });
            }
            else {
                document.querySelectorAll(".custom-card").forEach(card => {
                    if (!selectedCards.has(card.dataset.id)) {
                        selectedCards.add(card.dataset.id);

                        // Toggle selection visually and icon
                        if (!card.classList.contains("selected")) {
                            toggleCardSelection(card);
                        }
                    }
                });
            }
            console.log("All selected:", Array.from(selectedCards));
            
            updateToolbarIcon(); // <--- update toolbar icon
        });
    }
   // ---------------- Delete selected with modern popup ----------------
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
                body: JSON.stringify({ selected_items: Array.from(selectedCards) })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    Array.from(selectedCards).forEach(id => {
                        const card = document.querySelector(`.custom-card[data-id="${id}"]`);
                        if (card) card.remove();
                    });
                    selectedCards.clear();
                    updateToolbarIcon();
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
    // ---------------- Edit selected ----------------
const editForm = document.getElementById("edit-form");
const editPopup = document.getElementById("edit-popup");
const editNameInput = document.getElementById("edit-name");
const editIconInput = document.getElementById("edit-icon");
const editPreview = document.getElementById("edit-icon-preview");
const editBtn = document.getElementById("edit-btn");

if (editBtn && editForm && editPopup) {
    // Open popup when Edit clicked
    editBtn.addEventListener("click", function(e) {
        e.preventDefault(); // stop form submission
        if (selectedCards.size !== 1) return;

        const categoryId = Array.from(selectedCards)[0];
        const card = document.querySelector(`.custom-card[data-id="${categoryId}"]`);
        if (!card) return;

        // Prefill with current name
        editNameInput.value = card.querySelector(".card-title")?.innerText.trim() || "";

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
    editIconInput.addEventListener("change", function() {
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
    editForm.addEventListener("submit", function(e) {
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

        const categoryId = Array.from(selectedCards)[0];
        const formData = new FormData(editForm);
        formData.append("selected_items", categoryId);

        fetch("/actions_toolbar/edit_selected", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Replace card with updated HTML
                const oldCard = document.querySelector(`.custom-card[data-id="${categoryId}"]`);
                if (oldCard) {
                    oldCard.insertAdjacentHTML("beforebegin", data.html);
                    oldCard.remove();
                }
                selectedCards.clear();
                updateToolbarIcon();
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



        
    // ---------------- Clear selections ----------------
    function resetToolbar(state) {
        fetch("/actions_toolbar/reset_toolbar", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `state=${state}`
        })
        .then(res => res.json())
        .then(data => {
            selectAll = false;
            selectedCards.clear();       
            updateToolbarIcon()
            document.querySelectorAll(".custom-card.selected").forEach(card => {
                card.classList.remove("selected");
                // Reset icon
                const icon = card.querySelector("i");
                if (icon) {
                    icon.classList.remove("fa-check-square");
                    icon.classList.add("fa-square-o");
                }
            });
        });
    }
    
    // ---------------- Toggle individual icon ----------------
    function toggleCardSelection(cardElem) {
        const icon = cardElem.querySelector(".card-select-icon i");
        const selected = cardElem.classList.toggle("selected");

        if (!icon) return;

        if (selected) {
            icon.classList.remove("fa-square-o");
            icon.classList.add("fa-check-square");
        } else {
            icon.classList.remove("fa-check-square");
            icon.classList.add("fa-square-o");
        }
    }


    function updateToolbarIcon() {
        const selectAllIcon = document.querySelector("#select-all-btn i");
        const deleteBtn = document.getElementById("delete-btn");
        const editBtn = document.getElementById("edit-btn")
        if (!selectAllIcon) return;

        if (selectedCards.size === 0 || selectedCards.size < totalCardsLenth) {
            // No cards selected
            selectAllIcon.classList.remove("fa-check-square");
            selectAllIcon.classList.add("fa-square-o");
        } else {
            // Some cards selected
            selectAllIcon.classList.remove("fa-square-o");
            selectAllIcon.classList.add("fa-check-square");
        }
            
        // --- Control Delete button ---
        if (deleteBtn) {
            deleteBtn.disabled = selectedCards.size === 0;  
        }

        // --- Control Edit button ---
        if (editBtn) {
            editBtn.disabled = (selectedCards.size > 1 || selectedCards.size === 0);
        }
    }
});
