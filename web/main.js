// web/main.js
async function addProduct() {
    const name = document.getElementById("productName").value;
    const price = parseFloat(document.getElementById("productPrice").value);
    const stock = parseInt(document.getElementById("productStock").value);
    const description = document.getElementById("productDescription").value;
    const category = document.getElementById("productCategory").value;

    const response = await eel.add_product(name, price, stock, description, category)();
    if (response) {
        alert("Product added successfully!");
        document.getElementById("productName").value = "";
        document.getElementById("productPrice").value = "";
        document.getElementById("productStock").value = "";
        document.getElementById("productDescription").value = "";
        document.getElementById("productCategory").value = "";
        loadProducts();
    }
}

async function loadProducts() {
    const products = await eel.get_products()();
    const productList = document.getElementById("productList");
    productList.innerHTML = ""; // Clear current list
    products.forEach(product => {
        const li = document.createElement("li");
        li.textContent = `${product.name} - $${product.price} - Stock: ${product.stock}`;
        productList.appendChild(li);
    });
}

// Load products on page load
window.onload = loadProducts;
