var lesson10 = {
	init: function() {
		this.scene = new THREE.Scene();
		this.scene.fog = new THREE.FogExp2(0xcce0ff, 0.0003);
		this.camera = new THREE.PerspectiveCamera();
		this.scene.add(this.camera);
		this.camera.position.set(100, 0, 0);
		this.renderer = new THREE.WebGLRenderer({ antialias:true });
		this.renderer.setSize(window.innerWidth - 20, window.innerHeight - 20);
		this.renderer.setClearColor(this.scene.fog.color);
		this.container = document.createElement('div');
		document.body.appendChild(this.container);
		this.container.appendChild(this.renderer.domElement);
		this.controls = new THREE.OrbitControls(this.camera);
		this.controls.maxDistance = 150;
		this.clock = new THREE.Clock();
		this.scene.add( new THREE.AmbientLight(0x444444));
		var dirLight = new THREE.DirectionalLight(0xffffff);
		dirLight.position.set(200, 200, 1000).normalize();
		this.camera.add(dirLight);
		this.camera.add(dirLight.target);
		/*
		const gltfLoader = new GLTFLoader();
		const url = 'resources/scene.gltf';
		gltfLoader.load(url, (gltf) => {
			const root = gltf.scene;
			scene.add(root);
		});
		*/
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
				this.scene.add(object);
			}
		}
 	}
};

function animate() {
	requestAnimationFrame(animate);
	render();
	update();
}
function update() {
	var delta = lesson10.clock.getDelta();
	lesson10.controls.update(delta);
}

function render() {
	if (lesson10.renderer)
		lesson10.renderer.render(lesson10.scene, lesson10.camera);
}

function initializeLesson() {
	lesson10.init();
	animate();
}

if (window.addEventListener)
	window.addEventListener('load', initializeLesson, false);
else if (window.attachEvent)
	window.attachEvent('onload', initializeLesson);
else window.onload = initializeLesson;