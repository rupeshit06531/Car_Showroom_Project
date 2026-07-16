/*=========================================
Car Showroom Management System
Premium Dashboard JS
=========================================*/

document.addEventListener("DOMContentLoaded", function () {

/*=========================================
Counter Animation
=========================================*/

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

const target = parseInt(counter.innerText) || 0;

let count = 0;

const speed = Math.max(10, target / 80);

const updateCounter = () => {

if (count < target) {

count += speed;

counter.innerText = Math.ceil(count);

requestAnimationFrame(updateCounter);

} else {

counter.innerText = target;

}

};

updateCounter();

});

/*=========================================
Card Hover Effect
=========================================*/

document.querySelectorAll(".dashboard-card").forEach(card => {

card.addEventListener("mouseenter", () => {

card.style.transform = "translateY(-8px) scale(1.02)";

});

card.addEventListener("mouseleave", () => {

card.style.transform = "translateY(0px) scale(1)";

});

});

/*=========================================
Quick Card Animation
=========================================*/

document.querySelectorAll(".quick-card").forEach(card => {

card.addEventListener("mouseenter", () => {

card.style.transform = "translateY(-8px)";

});

card.addEventListener("mouseleave", () => {

card.style.transform = "translateY(0px)";

});

});

});

/*=========================================
DataTables
=========================================*/

$(document).ready(function(){

if($("#customerTable").length){

$("#customerTable").DataTable({

responsive:true,

pageLength:10,

ordering:true,

searching:true,

language:{

search:"Search Customer : "

}

});

}

if($("#salesTable").length){

$("#salesTable").DataTable({

responsive:true,

pageLength:10,

ordering:true,

searching:true,

language:{

search:"Search Sales : "

}

});

}

});

/*=========================================
Image Preview
=========================================*/

const imageInput=document.querySelector('input[type="file"]');

if(imageInput){

const preview=document.createElement("img");

preview.style.maxWidth="220px";

preview.style.marginTop="15px";

preview.style.borderRadius="15px";

preview.style.display="none";

preview.style.boxShadow="0 10px 20px rgba(0,0,0,.15)";

imageInput.parentNode.appendChild(preview);

imageInput.addEventListener("change",function(){

const file=this.files[0];

if(file){

preview.src=URL.createObjectURL(file);

preview.style.display="block";

}

});

}

/*=========================================
Sidebar Active Menu
=========================================*/

document.querySelectorAll(".sidebar-menu a").forEach(link=>{

if(link.href===window.location.href){

link.classList.add("active");

}

});

/*=========================================
Smooth Scroll
=========================================*/

document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

anchor.addEventListener("click",function(e){

e.preventDefault();

const target=document.querySelector(this.getAttribute("href"));

if(target){

target.scrollIntoView({

behavior:"smooth"

});

}

});

});

/*=========================================
Scroll To Top Button
=========================================*/

const topBtn=document.createElement("button");

topBtn.innerHTML='<i class="fas fa-arrow-up"></i>';

topBtn.className="btn btn-primary";

topBtn.style.position="fixed";

topBtn.style.bottom="20px";

topBtn.style.right="20px";

topBtn.style.width="50px";

topBtn.style.height="50px";

topBtn.style.borderRadius="50%";

topBtn.style.display="none";

topBtn.style.zIndex="9999";

document.body.appendChild(topBtn);

window.addEventListener("scroll",()=>{

if(window.scrollY>300){

topBtn.style.display="block";

}else{

topBtn.style.display="none";

}

});

topBtn.addEventListener("click",()=>{

window.scrollTo({

top:0,

behavior:"smooth"

});

});

/*=========================================
Loading Animation
=========================================*/

window.addEventListener("load",()=>{

document.body.classList.add("loaded");

});

/*=========================================
Auto Hide Alerts
=========================================*/

setTimeout(()=>{

document.querySelectorAll(".alert").forEach(alert=>{

const bsAlert=bootstrap.Alert.getOrCreateInstance(alert);

bsAlert.close();

});

},4000);

/*=========================================
Button Loading Effect
=========================================*/

document.querySelectorAll("form").forEach(form=>{

form.addEventListener("submit",()=>{

const btn=form.querySelector("button[type='submit']");

if(btn){

btn.disabled=true;

btn.innerHTML='<span class="spinner-border spinner-border-sm me-2"></span>Saving...';

}

});

});

/*=========================================
Fade Animation
=========================================*/

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("fade-up");

}

});

});

document.querySelectorAll(".card,.dashboard-card,.quick-card,.car-card").forEach(item=>{

observer.observe(item);

});

/*=========================================
Console
=========================================*/

console.log("%cCar Showroom Management System","color:#2563eb;font-size:18px;font-weight:bold;");
console.log("%cDeveloped by Rupesh Mahto","color:#16a34a;font-size:14px;");