const body = document.body;
const button = document.querySelector(".more-btn");

const loadPage = () => {
  body.classList.add("load-page");
};


window.onload = loadPage;