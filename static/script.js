document.addEventListener("DOMContentLoaded", () => {
  // 📝 Form Submission
  document.getElementById('contactForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
      name: document.getElementById('name').value.trim(),
      password: document.getElementById('password').value.trim(),
      contact: document.getElementById('contact').value.trim(),
      location: document.getElementById('location').value.trim(),
      amount: parseFloat(document.getElementById('amount').value.trim()).toFixed(2),
      type: document.getElementById('type').value.trim()
    };

    const response = await fetch('/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    const result = await response.json();
    if (result.redirect) {
      window.location.href = result.redirect;
    }
  });

  // 🔍 Filtering Functionality
  document.getElementById("filterButton").addEventListener("click", applyFilters);

  function applyFilters() {
    let selectedLocation = document.getElementById("filterLocation").value.toLowerCase();
    let selectedType = document.getElementById("filterType").value.toLowerCase();
    let minAmount = parseInt(document.getElementById("minAmount").value) || 0;
    let maxAmount = parseInt(document.getElementById("maxAmount").value) || Infinity;

    document.querySelectorAll("#requestTable tr").forEach(row => {
      let rowLocation = row.getAttribute("data-location").toLowerCase();
      let rowType = row.getAttribute("data-type").toLowerCase();
      let rowAmount = parseInt(row.getAttribute("data-amount"));

      let locationMatch = selectedLocation === "" || rowLocation.includes(selectedLocation);
      let typeMatch = selectedType === "" || rowType === selectedType;
      let amountMatch = rowAmount >= minAmount && rowAmount <= maxAmount;

      row.style.display = locationMatch && typeMatch && amountMatch ? "" : "none";
    });
  }

  // 🛑 Delete Request Functionality
  document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
      const row = e.target.closest("tr");
      const name = row.getAttribute("data-name");
      const password = prompt("Enter your password to confirm deletion:");

      if (!password) return;

      const response = await fetch('/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, password })
      });

      const result = await response.json();
      if (result.success) {
        row.remove(); // Remove row from table
        alert("Request deleted successfully!");
      } else {
        alert(result.message);
      }
    });
  });
});
