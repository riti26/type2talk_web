const SESSION_KEY = "phrase_items";

export function initPhraseToolbar(){
    // Attach button click handlers globally
    window.playPhrase = () => {
        fetch("/card_click", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: getPhraseSentence() })
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
    };

    window.deleteLastItem = () => {
        removeLastPhraseItem()
    };
}

export function getPhraseItems() {
    return JSON.parse(sessionStorage.getItem(SESSION_KEY) || "[]");
}

export function setPhraseItems(items) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(items));
}

export function addToPhraseToolbar(item) {
    let items = getPhraseItems();
    items.push(item);
    setPhraseItems(items);
    renderPhraseToolbar();
}

export function removeLastPhraseItem() {
    let items = getPhraseItems();
    items.pop();
    setPhraseItems(items);
    renderPhraseToolbar();
}

export function clearPhraseItems() {
    sessionStorage.removeItem(SESSION_KEY);
    renderPhraseToolbar();
}

export function renderPhraseToolbar() {
    const container = document.getElementById("phrase-items-container");
    const template = document.getElementById("phrase-item-template");

    if (!container || !template) return;

    container.innerHTML = ""; // clear previous items

    const phraseItems = getPhraseItems();
    phraseItems.forEach(item => {
        const card = template.content.cloneNode(true);

        const cardElem = card.querySelector(".phrase-item-card");
        cardElem.querySelector("img").src = item.image_source 
                                            ? `/static/${item.image_source}` 
                                            : "/static/images/default.png";
        cardElem.querySelector("img").alt = item.text;
        cardElem.querySelector("span").textContent = item.text;

        cardElem.addEventListener("click", () => {
            playItemAudio(item.text);
        });

        container.appendChild(card);
    });
}

export function getPhraseSentence() {
    const phraseItems = getPhraseItems(); // get all items
    if (!phraseItems || !phraseItems.length) return "";

    // join all texts with space
    const sentence = phraseItems.map(item => item.text).join(" ");
    return sentence;
}

