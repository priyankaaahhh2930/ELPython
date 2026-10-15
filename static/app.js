const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
if (menuToggle && sidebar) menuToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
// Show a live total on the billing form before it is submitted.
const billingForm = document.querySelector('form.data-form');
if (billingForm && window.location.pathname === '/billing') {
  const feeInputs = [...billingForm.querySelectorAll('input[type="number"]')];
  if (feeInputs.length >= 2) {
    const preview = document.createElement('div');
    preview.className = 'total-preview';
    preview.innerHTML = '<span>Estimated total</span><strong>₹0.00</strong>';
    const submit = billingForm.querySelector('button[type="submit"]');
    if (submit) billingForm.insertBefore(preview, submit);
    const updateTotal = () => { const total = feeInputs.reduce((sum, input) => sum + (Number(input.value) || 0), 0); preview.querySelector('strong').textContent = `₹${total.toFixed(2)}`; };
    feeInputs.forEach(input => input.addEventListener('input', updateTotal));
  }
}
