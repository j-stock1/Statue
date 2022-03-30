let rings = 17
let crystals = 22

let updateStatueCallback = (state) => {}

let pattern = "test"
let keyframe = 0


function setUpdateStatueCallback(funct){
    updateStatueCallback = funct
    updateStatueCallback(statueState);
}


let statueState = []
for(let i = 0; i < rings; i++) {
    let temp = []
    for(let j = 0; j < crystals; j++){
        temp.push([0, 0, 0])
    }
    statueState.push(temp)
}

function getColor(hex) {
  const color = hex
  const r = parseInt(color.substr(1,2), 16)
  const g = parseInt(color.substr(3,2), 16)
  const b = parseInt(color.substr(5,2), 16)
  return [r, g, b]
}

function componentToHex(c) {
  let hex = c.toString(16);
  return hex.length === 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b, start="#") {
  return start + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function setForm(ring, crystal){
    const color = statueState[ring][crystal];
    document.getElementById("ringLabel").textContent = "Ring: " + ring.toString()
    document.getElementById("crystalLabel").textContent = "Crystal: " + crystal.toString()
    document.getElementById("ring").value = ring.toString()
    document.getElementById("crystal").value = crystal.toString()
    document.getElementById("color").value = rgbToHex(color[0], color[1], color[2])
}
setForm(0,0)

function resetFunct(){
    console.log("STUFF")
    const ring = parseInt(document.getElementById("ring").value)
    const crystal = parseInt(document.getElementById("crystal").value)
    setForm(ring, crystal)
}

function updateStatueState(form){
    const ring = parseInt(document.getElementById("ring").value)
    const crystal = parseInt(document.getElementById("crystal").value)

    if((isNaN(ring) && ring !== 0) || (isNaN(crystal) && crystal !== 0)){
        return;
    }
    if(ring < 0 || ring >= rings){
        return;
    }
    if(crystal < 0 || crystal >= crystals){
        return;
    }
    statueState[ring][crystal] = getColor(document.getElementById("color").value)

    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/api/edit_keyframe?name="+pattern+"&id="+keyframe.toString(), true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify({"state": statueState}));

    updateStatueCallback(statueState);
}

function loadStatueState(){
    const xhttp = new XMLHttpRequest();

    xhttp.open("GET", "/api/keyframe_info?name="+pattern+"&id="+keyframe.toString(), true);
    xhttp.onload = function() {
        statueState = JSON.parse(xhttp.response)["state"];
        updateStatueCallback(statueState);
    }
    xhttp.send();
}

loadStatueState();