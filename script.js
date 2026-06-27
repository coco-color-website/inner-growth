document.addEventListener("DOMContentLoaded", () => {
  const tocLinks = document.querySelectorAll(".toc-link");
  const sections = document.querySelectorAll(".stage, .hero");

  // 点击导航时更新 active 状态
  tocLinks.forEach((link) => {
    link.addEventListener("click", () => {
      tocLinks.forEach((l) => l.classList.remove("active"));
      link.classList.add("active");
    });
  });

  // 滚动时高亮当前章节
  const observerOptions = {
    root: null,
    rootMargin: "-40% 0px -50% 0px",
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach((link) => {
          link.classList.toggle("active", link.getAttribute("href") === `#${id}`);
        });
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));

  // 给每个 stage 设置 CSS 变量，用于错落动画
  document.querySelectorAll(".stage").forEach((stage, index) => {
    stage.style.setProperty("--i", index);
  });
});
