const quantityInputs = document.querySelectorAll('.quantity');
const totalCostElements = document.querySelectorAll('.total-cost-value');
const priceElements = document.querySelectorAll('.price-element');
const totalCostAllProductsElement = document.getElementById('total-cost-all-products-value');

quantityInputs.forEach((input, index) => {
  input.addEventListener('input', () => {
    updateTotalCost(index);
    updateTotalCostAllProducts();
  });
});

function updateTotalCost(index) {
  const quantity = parseInt(quantityInputs[index].value);
  const productPrice = parseInt(priceElements[index].textContent);
  const totalCost = quantity * productPrice;
  totalCostElements[index].textContent = `${totalCost} р.`;
}

function updateTotalCostAllProducts() {
  let totalCostAllProducts = 0;
  totalCostElements.forEach((element) => {
    const totalCost = parseInt(element.textContent.replace(' р.', ''));
    totalCostAllProducts += totalCost;
  });
  totalCostAllProductsElement.textContent = `${totalCostAllProducts} р.`;
}

updateTotalCostAllProducts();

function handleSubmit(event) {
      document.getElementById("submitButton").style.display = "none";
      document.getElementById("loadingButton").style.display = "block";
      document.getElementById("myForm").submit();
    }
