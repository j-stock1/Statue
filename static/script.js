import * as THREE from '../static/three.module.js';
//import {GLTFLoader} from '../static/GLTFLoader.js';
import {OrbitControls} from '../static/OrbitControls.js';

const scene = new THREE.Scene();
var SCREEN_WIDTH = window.innerWidth, SCREEN_HEIGHT = window.innerHeight;
var ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT;
const camera = new THREE.PerspectiveCamera(45, ASPECT, 1, 1000);
camera.position.set(100, 0, 0);
const renderer = new THREE.WebGLRenderer();
//const loader = new GLTFLoader();
const controls = new OrbitControls(camera, renderer.domElement)
const light = new THREE.SpotLight()
const ambilight = new THREE.AmbientLight(0x444444);
light.position.set(200, 200, 1000)
scene.add(ambilight)
scene.add(light)
//const flamingo = await loader.loadAsync('https://cdn.devdojo.com/assets/3d/parrot.glb');
var object, material;
var objGeometry = new THREE.CylinderGeometry(1, 1, 3, 22, 1);
material = new THREE.MeshPhongMaterial({color: 0xFFA500});
material.transparent = true;
var r = 7;
var rows = 22;
var columns = 17;
var count = 0;
var objects = [];
for (var col = 0; col <= columns; ++col) {
	for (var i = 0; i < 360; i += (360 / (rows - 1))) {
		//material = new THREE.MeshPhongMaterial({color: Math.random() *  0xffffff});
		//material.transparent = true;
		var x = Math.sin(i*(Math.PI/180))*r;
		var y = Math.cos(i*(Math.PI/180))*r;
		object = new THREE.Mesh(objGeometry.clone(), material);
		object.position.x = y;
		object.position.y = (columns / 2 * -4) + (col * 4);
		object.position.z = x;
		object.callback = objectClickHandler;
		scene.add(object);
		objects[count] = object;
		count++;
	}
}
function objectClickHandler(test) {
	alert("Clicked");
	console.log(test);
	//console.log(count);
}
scene.background = new THREE.Color('#72c0ff');
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();
function onDocumentMouseDown(event) {
	event.preventDefault();
	mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
	mouse.y =  - (event.clientY / renderer.domElement.clientHeight) * 2 + 1;
	raycaster.setFromCamera(mouse, camera);
	var intersects = raycaster.intersectObjects(objects);
	if (intersects.length > 0)
		intersects[0].object.callback("Herefjlsf");
}
function onDocumentMouseMove(event) {
	event.preventDefault();
 
    mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
    mouse.y =  - (event.clientY / renderer.domElement.clientHeight) * 2 + 1;
 
    raycaster.setFromCamera(mouse, camera);
 
    var intersects = raycaster.intersectObjects(objects);
    var canvas = document.body.getElementsByTagName('canvas')[0];
 
    if (intersects.length > 0)
        canvas.style.cursor = "pointer";
	else
        canvas.style.cursor = "default";
}
document.addEventListener('mousemove', onDocumentMouseMove, false);
document.addEventListener('mousedown', onDocumentMouseDown, false);
function animate() {
	requestAnimationFrame(animate);
	renderer.render(scene, camera);
}
animate();
