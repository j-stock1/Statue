import * as THREE from '../static/three.module.js';
//import {GLTFLoader} from '../static/GLTFLoader.js';
import {OrbitControls} from '../static/OrbitControls.js';

const parent = document.getElementById("panel2")

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, parent.offsetWidth/parent.offsetHeight, 1, 1000);
const renderer = new THREE.WebGLRenderer();


camera.position.set(100, 0, 0);

const controls = new OrbitControls(camera, renderer.domElement)

const light = new THREE.SpotLight()
const ambilight = new THREE.AmbientLight(0x444444);
light.position.set(200, 200, 1000)
scene.add(ambilight)
scene.add(light)

var object, material;

var objGeometry = new THREE.CylinderGeometry(1, 1, 3, 22, 1);


var r = 7;
var rings = 17;
var crystals = 22;

var objects = [];
let full_list = [];
for (var ring = 0; ring < rings; ring++) {
	let temp_ring = []
	let crystal = 0;
	for (var i = 0; i < 360; i += (360 / (crystals))) {
		material = new THREE.MeshPhongMaterial({color: 0xFFA500});
		material.transparent = true;
		var x = Math.sin(i*(Math.PI/180))*r;
		var y = Math.cos(i*(Math.PI/180))*r;
		object = new THREE.Mesh(objGeometry.clone(), material);
		object.position.x = y;
		object.position.y = (rings / 2 * -4) + (ring * 4);
		object.position.z = x;
		object.callback = objectClickHandler;
		object.ring = ring;
		object.crystal = crystal;
		crystal++;
		scene.add(object);
		temp_ring.push(object);
		full_list.push(object)
	}
	objects.push(temp_ring);
}

function setState(state){
	for(let ring = 0; ring < rings; ring++){
		for(let crystal = 0; crystal < crystals; crystal++){
			let obj = objects[ring][crystal];
			let color = state[ring][crystal];
			obj.material.color.setHex(rgbToHex(color[0], color[1], color[2], "0x"));
			//obj.material.color.setHex("0xff0000");
			obj.material.needsUpdate = true
		}
	}
}

function objectClickHandler(test) {
	let obj = test.object
	//alert("Clicked");
	//console.log(count);
	setForm(obj.ring, obj.crystal);
}
scene.background = new THREE.Color('#72c0ff');

renderer.setSize(parent.offsetWidth, parent.offsetHeight);
parent.appendChild(renderer.domElement);
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
function onDocumentMouseDown(event) {
	//event.preventDefault();

	const rect = event.target.getBoundingClientRect();
	mouse.x = ((event.clientX - rect.left) / renderer.domElement.clientWidth) * 2 - 1;
	mouse.y =  - ((event.clientY -rect.top) / renderer.domElement.clientHeight) * 2 + 1;
	raycaster.setFromCamera(mouse, camera);
	var intersects = raycaster.intersectObjects(full_list);
	if (intersects.length > 0)
		intersects[0].object.callback(intersects[0]);
}
function onDocumentMouseMove(event) {
	//event.preventDefault();
 
	const rect = event.target.getBoundingClientRect();
	mouse.x = ((event.clientX - rect.left) / renderer.domElement.clientWidth) * 2 - 1;
	mouse.y =  - ((event.clientY -rect.top) / renderer.domElement.clientHeight) * 2 + 1;
 
    raycaster.setFromCamera(mouse, camera);
 
    var intersects = raycaster.intersectObjects(full_list);
    var canvas = document.body.getElementsByTagName('canvas')[0];
 
    if (intersects.length > 0)
        canvas.style.cursor = "pointer";
	else
        canvas.style.cursor = "default";
}
function resize(){
	renderer.setSize(0,0);
	renderer.setSize(parent.offsetWidth, parent.offsetHeight);
	camera.aspect = parent.offsetWidth/parent.offsetHeight;
	camera.updateProjectionMatrix();
}

window.onresize = resize

document.addEventListener('mousemove', onDocumentMouseMove, false);
renderer.domElement.addEventListener('mousedown', onDocumentMouseDown, false);

setUpdateStatueCallback(setState);

function animate() {
	renderer.render(scene, camera);
	requestAnimationFrame(animate);
}
animate();

