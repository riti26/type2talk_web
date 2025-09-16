export function initFeedback() {
    const stars = document.querySelectorAll(".star-rating span");
    let selectedRating = 0;

    stars.forEach((star, index) => {
        star.addEventListener("click", () => {
            selectedRating = star.getAttribute("data-value");
            stars.forEach(s => s.classList.remove("selected"));
            for (let i = 0; i < selectedRating; i++) {
                stars[i].classList.add("selected");
            }
        });
        star.addEventListener("mouseover", () => {
            stars.forEach((s, i) => {
                s.style.color = i <= index ? "#FFD700" : "#ccc";
            });
        });

        star.addEventListener("mouseout", () => {
            stars.forEach((s, i) => {
                s.style.color = i < selectedRating ? "#FFD700" : "#ccc";
            });
        });

        // Star click (select rating)
        star.addEventListener("click", () => {
            selectedRating = parseInt(star.getAttribute("data-value"));
            stars.forEach((s, i) => {
                s.style.color = i < selectedRating ? "#FFD700" : "#ccc";
            });
        });
    });
}
