window.clearScoreInput = function(formEl) {
  const input = formEl.querySelector('input[name="delta"]');
  if (input) input.value = "";
};