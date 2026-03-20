window.clearScoreInput = function(formEl) {
  const input = formEl.querySelector('input[name="delta"]');
  if (input) input.value = "";
};

window.clearBatchScoreInputs = function() {
  const inputs = document.querySelectorAll('.score-input');
  inputs.forEach(input => input.value = "");
};

window.incrementScore = function(button, amount) {
  const container = button.closest('.flex');
  if (!container) return;
  
  const input = container.querySelector('input[type="number"]');
  if (!input) return;
  
  const currentValue = parseInt(input.value) || 0;
  input.value = currentValue + amount;
  
  // Trigger change event
  input.dispatchEvent(new Event('change', { bubbles: true }));
};
