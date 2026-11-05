document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".message").forEach((message) => {
    setTimeout(() => { message.style.transition = "opacity .5s"; message.style.opacity = "0"; }, 4500);
  });
});
