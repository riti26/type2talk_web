// toolbar.js
import { resetActionsToolbar, updateActionsToolbarIcon, toggleCardSelection } from "./utils.js";

let selectedCards = new Set();
let cardType = null;
let toolbarExpanded = false;
let selectAll = false;
let totalCardsLength = 0;

export function initActionsToolbar() {
    totalCardsLength = document.querySelectorAll(".custom-card").length;

    window.toggleActionsToolbar = function () {
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
                resetActionsToolbar(selectedCards, toolbarExpanded);
                selectAll = false;
            }

            // Show/hide select icons on each card
            document.querySelectorAll(".custom-card .card-select-icon").forEach(icon => {
                icon.style.display = toolbarExpanded ? "block" : "none";
            });
            updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
        });
    };

    // ---------------- Handle single card click ----------------
    window.handleCardClick = function(cardElem, event) {
        if (toolbarExpanded) {
            event.preventDefault(); // prevent navigation

            cardType = cardElem.dataset.item ? JSON.parse(cardElem.dataset.item).type : null;

            // Toggle selection in Set
            if (selectedCards.has(cardElem.dataset.id)) {
                selectedCards.delete(cardElem.dataset.id);
            } else {
                selectedCards.add(cardElem.dataset.id);
            }

            // Update selectAll state
            if (selectedCards.size < totalCardsLength) 
                selectAll = false;
            else if (selectedCards.size === totalCardsLength)
                selectAll = true;

            // Toggle visual selection and icon
            toggleCardSelection(cardElem);

            updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
        } else {
            // Toolbar collapsed: navigate
            const item = cardElem.dataset.item ? JSON.parse(cardElem.dataset.item) : null;
            if(item && item.is_standalone) {
                if (item.is_standalone) {
                    fetch(cardElem.dataset.url, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ text: item.text })
                    })
                    .then(response => {
                        if (!response.ok) throw new Error("HTTP " + response.status);
                        return response.blob();
                    })
                    .then(blob => {
                        const audio = new Audio(URL.createObjectURL(blob));
                        return audio.play();
                    })
                    .catch(err => console.error("Playback error:", err));
                }
            }
            else 
            {
                // Navigate to card's URL
                const url = cardElem.dataset.url;
                window.location.href = url;
            }
        }
    }

    // ---------------- Select all ----------------
    const selectAllForm = document.querySelector('form[action$="select_all"]');
    if (selectAllForm) {
        selectAllForm.addEventListener("submit", function (e) {
            e.preventDefault();
            if (!toolbarExpanded) return;

            selectAll = !selectAll;

            if (!selectAll) {
                // Clear all selections
                selectedCards.clear();
                document.querySelectorAll(".custom-card.selected").forEach(card => {
                    card.classList.remove("selected");
                    const icon = card.querySelector("i");
                    if (icon) {
                        icon.classList.remove("fa-check-square");
                        icon.classList.add("fa-square-o");
                    }
                });
            } else {
                // Select all
            cardType = document.querySelectorAll(".custom-card") ? JSON.parse(document.querySelectorAll(".custom-card")[0].dataset.item).type : null;
                document.querySelectorAll(".custom-card").forEach(card => {
                    if (!selectedCards.has(card.dataset.id)) {
                        selectedCards.add(card.dataset.id);
                        if (!card.classList.contains("selected")) {
                            toggleCardSelection(card);
                        }
                    }
                });
            }

            console.log("All selected:", Array.from(selectedCards));
            updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
        });
    }
}

export { selectedCards, totalCardsLength, selectAll, cardType };
