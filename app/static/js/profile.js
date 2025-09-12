export function initProfile(){
    document.querySelectorAll(".delete-btn").forEach(btn => {
        const modalId = btn.dataset.modal;
        const modal = document.getElementById(modalId);
        if (!modal) return;

        const cancelBtn = modal.querySelector(".cancel-btn");

        // Open modal
        btn.addEventListener("click", () => {
            modal.style.display = "flex"; // show flex for centering
        });

        // Close modal
        cancelBtn.addEventListener("click", () => {
            modal.style.display = "none";
        });

        // Close modal if clicked outside content
        window.addEventListener("click", (e) => {
            if (e.target === modal) modal.style.display = "none";
        });
    });
}