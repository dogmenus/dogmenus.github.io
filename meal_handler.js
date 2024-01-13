
window.onload = onLoaded

function onLoaded() {
  const hour = new Date().getHours()
  const minute = new Date().getMinutes()
  if (hour < 10 || (hour == 10 && minute < 30)) {
    breakfast()
  }
  else if (hour < 15) {
    lunch()
  }
  else {
    dinner()
  }
}

function breakfast() {
  console.log("breakfast")
  document.getElementById("lunch").style.display = "none";
  document.getElementById("dinner").style.display = "none";
  document.getElementById("breakfast").style.display = "block";
}

function lunch() {
  console.log("lunch")
  document.getElementById("breakfast").style.display = "none";
  document.getElementById("dinner").style.display = "none";
  document.getElementById("lunch").style.display = "block";
}

function dinner() {
  console.log("dinner")
  document.getElementById("breakfast").style.display = "none";
  document.getElementById("lunch").style.display = "none";
  document.getElementById("dinner").style.display = "block";
}
