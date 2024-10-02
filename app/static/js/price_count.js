const quantityInput = document.getElementById('quantity');
    const totalCostElement = document.getElementById('total-cost-value');
    const priceElement = document.getElementById('priceElement')

    quantityInput.addEventListener('input', updateTotalCost);

    function updateTotalCost() {
      const quantity = parseInt(quantityInput.value);
      const productPrice = parseInt(priceElement.textContent);
      const totalCost = quantity * productPrice;
      totalCostElement.textContent = `${totalCost} р.`;
    }