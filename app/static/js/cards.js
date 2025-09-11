import { toggleCardSelection, updateActionsToolbarIcon } from "./utils.js";
import { addToPhraseToolbar } from "./phrase_toolbar.js";

export function handleCardClick(cardElem, event, { toolbarExpanded, selectedCards}) {
    if (toolbarExpanded) {
        event.preventDefault(); // prevent navigation


        // Toggle selection in Set
        if (selectedCards.has(cardElem.dataset.id)) {
            selectedCards.delete(cardElem.dataset.id);
        } else {
            selectedCards.add(cardElem.dataset.id);
        }

        // Toggle visual selection and icon
        toggleCardSelection(cardElem);

        updateActionsToolbarIcon(selectedCards, document.querySelectorAll(".custom-card").length);
    } else {
        // Toolbar collapsed: navigate
        const item = cardElem.dataset.item ? JSON.parse(cardElem.dataset.item) : null;
        if (item && item.is_standalone) {
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
            addToPhraseToolbar(item)
        }
        else {
            // Navigate to card's URL
            const url = cardElem.dataset.url;
            window.location.href = url;
        }
    }

}
