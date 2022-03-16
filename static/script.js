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
		scene.add(object);
	}
}
scene.background = new THREE.Color('#72c0ff');
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
function animate() {
	requestAnimationFrame(animate);
	renderer.render(scene, camera);
}
animate();
