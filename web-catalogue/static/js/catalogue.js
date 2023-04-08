// asynchronous function to load the products
async function loadProducts() {
	// fetching the JSON data from the products file
	const response = await fetch("/static/products.json");
	const data = await response.json();
	const products = data.products;

	// function to render the products based on the applied filters
	function renderProducts() {
		const filter = document.getElementById("filter").value.toLowerCase();
		const category = document.getElementById("category").value;

		const filteredProducts = products.filter(product => {
			if (category && product.category !== category) {
				return false;
			}
			if (filter && !product.name.toLowerCase().includes(filter)) {
				return false;
			}
			return true;
		});

		// selecting the container to render the filtered products
		const shopItems = document.querySelector('.shop-items');
		shopItems.innerHTML = "";

		// looping through the filtered products and rendering them
		filteredProducts.forEach((product) => {
			const shopItem = document.createElement("div");
			shopItem.classList.add("col");
			shopItem.innerHTML = `
            <div class="card rounded-3">
                <div class="card-img-wrapper">
                    <img src="${product.image}" class="card-img-top-shop" alt="${product.name}">
                </div>
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">€${product.price.toFixed(2)}</p>
                </div>
            </div>
            `;
			shopItems.appendChild(shopItem);
		});

		// adding event listeners to the filter inputs
		document.getElementById("filter").addEventListener("input", renderProducts);
		document.getElementById("category").addEventListener("change", renderProducts);
	}
	// rendering the products
	renderProducts();
}
loadProducts();