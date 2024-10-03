const quantityInputs = document.querySelectorAll('.quantity');
const totalCostElements = document.querySelectorAll('.total-cost-value');
const priceElements = document.querySelectorAll('.price-element');

quantityInputs.forEach((input, index) => {
  input.addEventListener('input', () => {
    updateTotalCost(index);
  });
});

function updateTotalCost(index) {
  const quantity = parseInt(quantityInputs[index].value);
  const productPrice = parseInt(priceElements[index].textContent);
  const totalCost = quantity * productPrice;
  totalCostElements[index].textContent = `${totalCost} р.`;
}
