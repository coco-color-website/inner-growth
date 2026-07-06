document.addEventListener("DOMContentLoaded", () => {
  // 平滑滚动（所有锚点链接）
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (href === "#") return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // 给每个 stage 设置 CSS 变量，用于错落动画
  document.querySelectorAll(".stage").forEach((stage, index) => {
    stage.style.setProperty("--i", index);
  });
});
