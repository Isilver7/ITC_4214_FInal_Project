document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("search-form");
    const searchQuery = document.getElementById("search-query");
    const productList = document.getElementById("product-list");

    const searchUrl = searchForm.dataset.searchUrl; 

    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const query = searchQuery.value;
        fetch(`${searchUrl}?query=${encodeURIComponent(query)}`)
            .then((response) => response.text())
            .then((data) => {
                productList.innerHTML = data;
            })
            .catch((error) => {
                console.error("Error fetching search results:", error);
            });
    });
});
