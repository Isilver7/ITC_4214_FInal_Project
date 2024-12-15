document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star");
    const feedback = document.getElementById("rating-feedback");

    let selectedRating = 0;

    stars.forEach((star) => {
        star.addEventListener("mouseenter", () => {
            const value = parseInt(star.getAttribute("data-value"));
            stars.forEach((s) => {
                const starValue = parseInt(s.getAttribute("data-value"));
                if (starValue <= value) {
                    s.classList.add("hovered");
                } else {
                    s.classList.remove("hovered");
                }
            });
        });
    });

    document.querySelector(".rating-stars").addEventListener("mouseleave", () => {
        stars.forEach((s) => {
            s.classList.remove("hovered");
            if (parseInt(s.getAttribute("data-value")) <= selectedRating) {
                s.classList.add("selected");
            }
        });
    });

    stars.forEach((star) => {
        star.addEventListener("click", () => {
            const value = parseInt(star.getAttribute("data-value"));
            selectedRating = value;

            fetch(`${window.location.origin}/rate/${itemId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
                body: JSON.stringify({ stars: selectedRating }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data); 
                    if (data.success) {
                        feedback.textContent = `You rated this item ${data.stars} stars.`;
                        feedback.style.color = "green";
                        feedback.style.display = "block";

                        stars.forEach((s) => {
                            const starValue = parseInt(s.getAttribute("data-value"));
                            if (starValue <= selectedRating) {
                                s.classList.add("selected");
                            } else {
                                s.classList.remove("selected");
                            }
                        });
                    } else {
                        feedback.textContent = "Error: " + data.error;
                        feedback.style.color = "red";
                        feedback.style.display = "block";
                    }
                })
                .catch((error) => {
                    console.error("Fetch error:", error);
                    feedback.textContent = "An unexpected error occurred.";
                    feedback.style.color = "red";
                    feedback.style.display = "block";
                });
        });
    });
});
