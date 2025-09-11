// toolbar.js
import { resetActionsToolbar, updateActionsToolbarIcon, toggleCardSelection } from "./utils.js";
import { handleCardClick } from './cards.js'

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

    // Attach card click handler globally
    window.handleCardClick = (cardElem, event) => {
        handleCardClick(cardElem, event, { toolbarExpanded, selectedCards});
        // update selectAll here
        if (selectedCards.size < totalCardsLength) {
            selectAll = false;
        } else if (selectedCards.size === totalCardsLength) {
            selectAll = true;
        }
    };

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

            updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
        });
    }
}

export { selectedCards, totalCardsLength, selectAll, cardType };
