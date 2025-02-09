document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".cancel-btn").forEach(button => {
    button.addEventListener("click", async function () {
      const row = this.closest("tr");
      const name = row.getAttribute("data-name");
      const contact = row.getAttribute("data-contact");
      const type = row.getAttribute("data-type");

      const response = await fetch("/delete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, contact, type }),
      });

      const result = await response.json();
      if (result.success) {
        row.remove(); // Remove row from table
      } else {
        alert(result.message);
      }
    });
  });
});
