// web/main.js

// Fungsi untuk menambahkan produk baru
async function addProduct() {
    const name = document.getElementById("productName").value;
    const price = parseFloat(document.getElementById("productPrice").value);
    const stock = parseInt(document.getElementById("productStock").value);
    const description = document.getElementById("productDescription").value;
    const category = document.getElementById("productCategory").value;

    const response = await eel.add_product_eel( name, price, stock, description, category)();
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

// Fungsi untuk memuat daftar produk dari database
async function loadProducts() {
    const products = await eel.get_products_eel()();
    const productList = document.getElementById("productList");
    productList.innerHTML = ""; // Clear current list
    products.forEach(product => {
        const li = document.createElement("li");
        li.textContent = `${product.id} - ${product.name} - $${product.price} - Stock: ${product.quantity}`;
        li.setAttribute("data-product-id", product.id);
        li.addEventListener("click", () => addToTransaction(product.id));  // Menambahkan event listener untuk menambah ke transaksi
        productList.appendChild(li);
    });
}

// Fungsi untuk menambahkan item ke transaksi
async function addToTransaction(productId) {
    const quantity = prompt("Enter quantity:");
    if (!quantity || isNaN(quantity)) {
        alert("Please enter a valid quantity.");
        return;
    }

    const response = await eel.create_transaction_eel(productId, parseInt(quantity))();
    if (response.status) {
        alert(response.status);
        document.getElementById("transactionTotal").innerText = `Total: $${response.total.toFixed(2)}`;
    } else {
        alert(response.error);
    }
}

// Fungsi untuk memproses pembayaran
async function processPayment() {
    const total = parseFloat(document.getElementById("transactionTotal").innerText.replace("Total: $", ""));
    const amount = parseFloat(prompt("Enter payment amount:"));
    
    if (isNaN(amount)) {
        alert("Please enter a valid amount.");
        return;
    }

    const response = await eel.process_payment_eel(amount, total)();
    alert(response.status);
    if (response.status === "Payment successful") {
        document.getElementById("transactionTotal").innerText = "Total: $0.00";
        loadProducts();  // Reload products to update stock
    }
}

// Fungsi untuk menerapkan promosi ke produk
async function applyPromotion() {
    const productId = prompt("Enter product ID to apply promotion:");
    const discount = parseFloat(prompt("Enter discount percentage (0-100):"));

    if (isNaN(discount) || discount < 0 || discount > 100) {
        alert("Please enter a valid discount percentage.");
        return;
    }

    const response = await eel.apply_promotion_eel(productId, discount)();
    if (response.status) {
        alert(`${response.status}. New price: $${response.new_price.toFixed(2)}`);
        loadProducts();  // Reload products to reflect new prices
    } else {
        alert(response.error);
    }
}

// Fungsi untuk menghasilkan faktur transaksi
async function generateInvoice() {
    // Get transaction items from the backend
    const transactionItems = await eel.get_transaction_items_eel()(); // Fetch transaction items
    if (transactionItems.length === 0) {
        alert("No items in transaction.");
        return;
    }

    // Generate invoice using the fetched transaction items
    const invoiceResponse = await eel.generate_invoice_eel(transactionItems)();
    if (invoiceResponse.invoice) {
        alert("Invoice generated:\n" + invoiceResponse.invoice);
    }
}


// Load products on page load
window.onload = loadProducts;
