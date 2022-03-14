/**
 *
 * WebGL With Three.js - Lesson 10 - Drag and Drop Objects
 * http://www.script-tutorials.com/webgl-with-three-js-lesson-10/
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2015, Script Tutorials
 * http://www.script-tutorials.com/
 */

var lesson10 = {
  scene: null, camera: null, renderer: null,
  container: null, controls: null,
  clock: null, stats: null,
  plane: null, selection: null, offset: new THREE.Vector3(), objects: [],
  raycaster: new THREE.Raycaster(),

  init: function() {

	// Create main scene
	this.scene = new THREE.Scene();
	this.scene.fog = new THREE.FogExp2(0xcce0ff, 0.0003);

	var SCREEN_WIDTH = window.innerWidth - 20, SCREEN_HEIGHT = window.innerHeight - 20;

	// Prepare perspective camera
	var VIEW_ANGLE = 45, ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT, NEAR = 1, FAR = 1000;
	this.camera = new THREE.PerspectiveCamera(VIEW_ANGLE, ASPECT, NEAR, FAR);
	this.scene.add(this.camera);
	this.camera.position.set(100, 0, 0);
	this.camera.lookAt(new THREE.Vector3(0,0,0));

	// Prepare webgl renderer
	this.renderer = new THREE.WebGLRenderer({ antialias:true });
	this.renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
	this.renderer.setClearColor(this.scene.fog.color);

	// Prepare container
	this.container = document.createElement('div');
	document.body.appendChild(this.container);
	this.container.appendChild(this.renderer.domElement);

	// Events
	THREEx.WindowResize(this.renderer, this.camera);

	// Prepare Orbit controls
	this.controls = new THREE.OrbitControls(this.camera);
	this.controls.target = new THREE.Vector3(0, 0, 0);
	this.controls.maxDistance = 150;

	// Prepare clock
	this.clock = new THREE.Clock();

	// Add lights
	this.scene.add( new THREE.AmbientLight(0x444444));

	var dirLight = new THREE.DirectionalLight(0xffffff);
	dirLight.position.set(200, 200, 1000).normalize();
	this.camera.add(dirLight);
	this.camera.add(dirLight.target);


	// Plane, that helps to determinate an intersection position
	this.plane = new THREE.Mesh(new THREE.PlaneBufferGeometry(500, 500, 8, 8), new THREE.MeshBasicMaterial({color: 0xffffff}));
	this.plane.visible = false;
	this.scene.add(this.plane);

	var object, material;
	var objGeometry = new THREE.CylinderGeometry(1, 1, 3, 22,1);
	material = new THREE.MeshPhongMaterial({color: 0xFFA500});
	material.transparent = true;
	var r = 7;
	var count = 0;
	var rows = 22;
	var columns = 17;
	for (var col = 0; col <= columns; ++col) {
		for (var i = 0; i < 360; i += (360 / (rows - 1))) {
			count++;
			var x = Math.sin(i*(Math.PI/180))*r;
			var y = Math.cos(i*(Math.PI/180))*r;
			object = new THREE.Mesh(objGeometry.clone(), material);
			object.position.x = y;
			object.position.y = (columns / 2 * -4) + (col * 4);
			object.position.z = x;
			this.scene.add(object);
		}
	}
	console.log(`Count is ${count}`);


  }
};

// Animate the scene
function animate() {
  requestAnimationFrame(animate);
  render();
  update();
}

// Update controls and stats
function update() {
  var delta = lesson10.clock.getDelta();
  lesson10.controls.update(delta);
}

// Render the scene
function render() {
  if (lesson10.renderer) {
	lesson10.renderer.render(lesson10.scene, lesson10.camera);
  }
}

// Initialize lesson on page load
function initializeLesson() {
  lesson10.init();
  animate();
}

if (window.addEventListener)
  window.addEventListener('load', initializeLesson, false);
else if (window.attachEvent)
  window.attachEvent('onload', initializeLesson);
else window.onload = initializeLesson;