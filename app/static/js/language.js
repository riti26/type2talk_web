import { showToast } from "./utils.js";

export function initLanguage(){
    const searchField = document.getElementById('search_field');
    const languageList = document.getElementById('language_list');
    const noLanguagesMsg = document.getElementById('no-languages');

    if(searchField)
        searchField.addEventListener('input', function() {
            const query = this.value.trim().toLowerCase();
            const cards = languageList.querySelectorAll('.language-card');
            let visibleCount = 0;

            cards.forEach(card => {
                const name = card.dataset.name.toLowerCase();
                const code = card.dataset.code.toLowerCase();
                if (name.includes(query) || code.includes(query)) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            noLanguagesMsg.style.display = visibleCount === 0 ? 'block' : 'none';
        });

    if(languageList)
        languageList.querySelectorAll('.language-card').forEach(card => {
            card.addEventListener('click', () => {
                const code = card.dataset.code;

                fetch('select-language', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ code })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        showToast(`Language selected: ${ card.dataset.name}`, true);
                    } else {
                        showToast(`Error: ${data.message}`, false);
                    }
                })
                .catch(() => showToast("Error selecting language", false));
            });
        });
}