window.clearScoreInput = function(formEl) {
  const input = formEl.querySelector('input[name="delta"]');
  if (input) input.value = "";
};

window.clearBatchScoreInputs = function() {
  const inputs = document.querySelectorAll('.score-input');
  inputs.forEach(input => input.value = "");
};

window.toggleSign = function(button) {
  const input = button.nextElementSibling;
  if (!input) return;
  
  const value = parseFloat(input.value) || 0;
  input.value = -value;
};
