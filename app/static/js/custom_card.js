function handleCardClick(cardElement) {
    const jsonData = cardElement.getAttribute('data-item');
    const itemData = JSON.parse(jsonData);

    fetch("/card_click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(itemData)
    })
    .then(res => res.json())
    .then(data => {
        console.log("Server response:", data);
        // optionally do something in UI
    })
    .catch(err => console.error(err));
}
