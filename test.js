const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");

// 测试时先移除 HTML 里的 script 引用，避免重复加载 script.js
const testHtml = html.replace(/<script[^>]*src="script\.js"[^>]*><\/script>/g, "");

const dom = new JSDOM(testHtml, {
  runScripts: "dangerously",
  resources: "usable",
  pretendToBeVisual: true,
  url: "http://localhost:8080/"
});

const { window } = dom;
const document = window.document;

// jsdom 不会真正计算 CSS 布局，手动给容器一个尺寸
const mindmapEl = document.getElementById("mindmap");
mindmapEl.style.width = "1100px";
mindmapEl.style.height = "760px";

const script = document.createElement("script");
script.textContent = fs.readFileSync(path.join(__dirname, "script.js"), "utf8");
document.head.appendChild(script);

setTimeout(() => {
  const nodes = document.querySelectorAll(".node");
  const links = document.querySelectorAll(".link");

  console.log("初始节点数量:", nodes.length);
  console.log("初始连线数量:", links.length);

  let pass = true;

  if (nodes.length !== 7) {
    console.log("❌ 初始节点数量应为 7");
    pass = false;
  }

  if (links.length !== 6) {
    console.log("❌ 初始连线数量应为 6");
    pass = false;
  }

  // 测试点击分支节点展开
  const branch = document.querySelector('[data-id="b1"]');
  if (!branch) {
    console.log("❌ 未找到分支节点 b1");
    process.exit(1);
  }

  branch.click();

  setTimeout(() => {
    const nodesAfter = document.querySelectorAll(".node");
    const linksAfter = document.querySelectorAll(".link");
    console.log("展开后节点数量:", nodesAfter.length);
    console.log("展开后连线数量:", linksAfter.length);

    if (nodesAfter.length !== 12) {
      console.log("❌ 展开 b1 后节点数量应为 12");
      pass = false;
    }

    if (linksAfter.length !== 11) {
      console.log("❌ 展开 b1 后连线数量应为 11");
      pass = false;
    }

    // 测试点击叶子节点打开弹窗
    const leaf = document.querySelector('[data-id="b1-1"]');
    if (!leaf) {
      console.log("❌ 未找到叶子节点 b1-1");
      process.exit(1);
    }

    leaf.click();

    setTimeout(() => {
      const modal = document.getElementById("detailModal");
      const title = document.getElementById("modalTitle").textContent;
      const body = document.getElementById("modalBody").innerHTML;
      const visible = modal.getAttribute("aria-hidden") === "false";

      console.log("弹窗显示:", visible);
      console.log("弹窗标题:", title);
      console.log("弹窗内容长度:", body.length);

      if (!visible) {
        console.log("❌ 弹窗未显示");
        pass = false;
      }

      if (title !== "他人的爱不算什么") {
        console.log("❌ 弹窗标题不正确");
        pass = false;
      }

      if (body.length < 10) {
        console.log("❌ 弹窗内容过短");
        pass = false;
      }

      if (pass) {
        console.log("✅ 所有测试通过");
        process.exit(0);
      } else {
        console.log("❌ 部分测试未通过");
        process.exit(1);
      }
    }, 100);
  }, 100);
}, 200);
