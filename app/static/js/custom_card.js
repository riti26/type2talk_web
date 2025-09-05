function handleCardClick(cardElement) {
    const jsonData = cardElement.getAttribute('data-item');
    const itemData = JSON.parse(jsonData);

    fetch("/card_click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(itemData)
    })
    .then(res => res.blob()) // get binary audio
    .then(blob => {
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        audio.play();
    })
    .catch(err => console.error(err));
}
