document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star");
    const feedback = document.getElementById("rating-feedback");

    stars.forEach((star) => {
        star.addEventListener("mouseenter", () => {
            const value = star.getAttribute("data-value");
            stars.forEach((s) => {
                if (s.getAttribute("data-value") <= value) {
                    s.classList.add("selected");
                } else {
                    s.classList.remove("selected");
                }
            });
        });
    });

    document.querySelector(".rating-stars").addEventListener("mouseleave", () => {
        stars.forEach((s) => s.classList.remove("selected"));
    });

    stars.forEach((star) => {
        star.addEventListener("click", () => {
            const starsValue = star.getAttribute("data-value");

            fetch(`${window.location.origin}/rate/${itemId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
                body: JSON.stringify({ stars: starsValue }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        feedback.textContent = `You rated this item ${data.stars} stars.`;
                        feedback.style.color = "green";
                        feedback.style.display = "block";
                    } else {
                        feedback.textContent = "There was an error. Please try again.";
                        feedback.style.color = "red";
                        feedback.style.display = "block";
                    }
                })
                .catch(() => {
                    feedback.textContent = "There was an error. Please try again.";
                    feedback.style.color = "red";
                    feedback.style.display = "block";
                });
        });
    });
});
