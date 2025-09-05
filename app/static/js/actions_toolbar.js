function toggleToolbar() {
    fetch("/actions_toolbar/toggle_toolbar", {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest" }
    })
    .then(response => response.json())
    .then(data => {
        const expanded = data.expanded;
        const toolbar = document.getElementById("actions-toolbar");

        // Show/hide correct buttons based on expanded state
        toolbar.querySelectorAll("#select-all-btn, #delete-btn, #edit-btn").forEach(btn => {
            btn.parentElement.style.display = expanded ? "inline" : "none";
        });

        toolbar.querySelector("#add-btn").parentElement.style.display = expanded ? "none" : "inline";
    });
}
