import { showToast } from "./utils.js";
import { getPhraseItems, setPhraseItems } from "./phrase_toolbar.js";

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

    if(languageList){
        languageList.querySelectorAll('.language-card').forEach(card => {
            card.addEventListener('click', async () => {
                const code = card.dataset.code;
                const loader = document.getElementById("language-loader"); // make sure you have a loader element
                loader.style.display = "block"; // show loader
                const phrase_data = getPhraseItems();
                try {
                    const res = await fetch('select-language', {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ code, phrase_data })
                    });

                    if (!res.ok) {
                        throw new Error(`HTTP error! status: ${res.status}`);
                    }

                    const data = await res.json();

                    if (data.success) {
                        if(data.translated_phrase && data.translated_phrase.length > 0)
                            setPhraseItems(data.translated_phrase)
                        showToast(`Language selected: ${card.dataset.name}`, true);
                    } else {
                        showToast(`Error: ${data.message}`, false);
                    }
                } catch (error) {
                    console.error(error);
                    showToast("Error selecting language", false);
                } finally {
                    loader.style.display = "none"; // hide loader regardless of success/error
                }
            });
        });
    }
}