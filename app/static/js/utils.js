// utils.js
export function resetActionsToolbar(selectedCards, state) {
    fetch("/actions_toolbar/reset_toolbar", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `state=${state}`
    })
    .then(res => res.json())
    .then(data => {
        selectedCards.clear();       
        updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
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

export function toggleCardSelection(cardElem) {
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

export function updateActionsToolbarIcon(selectedCards, totalCardsLength) {
    const selectAllIcon = document.querySelector("#select-all-btn i");
    const deleteBtn = document.getElementById("delete-btn");
    const editBtn = document.getElementById("edit-btn")
    if (!selectAllIcon) return;

    if (selectedCards.size === 0 || selectedCards.size < totalCardsLength) {
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
