import omni.replicator.core as rep

with rep.new_layer():
	cameraFront = rep.create.camera(focal_length=8)
	cameraBack = rep.create.camera(focal_length=8)
	cameraLeft = rep.create.camera(focal_length=8)
	cameraRight = rep.create.camera(focal_length=8)

	bgjet_front1 = rep.get.prims(semantics=[("class", "bgjet_front1")])
	bgjet_front2 = rep.get.prims(semantics=[("class", "bgjet_front2")])
	bgjet_front3 = rep.get.prims(semantics=[("class", "bgjet_front3")])
	bgjet_back1 = rep.get.prims(semantics=[("class", "bgjet_back1")])
	bgjet_back2 = rep.get.prims(semantics=[("class", "bgjet_back2")])
	bgjet_back3 = rep.get.prims(semantics=[("class", "bgjet_back3")])
	bgjet_left1 = rep.get.prims(semantics=[("class", "bgjet_left1")])
	bgjet_right1 = rep.get.prims(semantics=[("class", "bgjet_right1")])

	ground_xform = rep.get.xform(semantics=[("class", "ground_xform")])
		
	with rep.trigger.on_frame(num_frames=100):
		#cameras
		with cameraFront:
			rep.modify.pose(position=rep.distribution.uniform((-10,385,490), (10,385,490)),
				look_at=rep.distribution.uniform((-10,375,565),(10,385,565)), 
				look_at_up_axis=rep.distribution.sequence([(0,1,0), (1,0,0), (0,-1,0), (-1,0,0)]),
			)
			rep.modify.attribute("focalLength", rep.distribution.uniform(8,25))
		with cameraBack:
			rep.modify.pose(position=rep.distribution.uniform((-10,379,565), (10,379,565)),
				look_at=rep.distribution.uniform((-10,370,490),(10,380,490)), 
				look_at_up_axis=rep.distribution.sequence([(0,1,0), (1,0,0), (0,-1,0), (-1,0,0)]),
			)
			rep.modify.attribute("focalLength", rep.distribution.uniform(8,25))
			
		with cameraLeft:
			rep.modify.pose(position=rep.distribution.uniform((38,379,530), (38,379,550)),
				look_at=rep.distribution.uniform((-38,365,530),(-38,375,550)), 
				look_at_up_axis=rep.distribution.sequence([(0,1,0), (1,0,0), (0,-1,0), (-1,0,0)]),
			)
			rep.modify.attribute("focalLength", rep.distribution.uniform(8,25))

		with cameraRight:
			rep.modify.pose(position=rep.distribution.uniform((-38,379,530), (-38,379,550)),
				look_at=rep.distribution.uniform((38,355,520),(38,385,560)),
				look_at_up_axis=rep.distribution.sequence([(0,1,0), (1,0,0), (0,-1,0), (-1,0,0)]),
			)
			rep.modify.attribute("focalLength", rep.distribution.uniform(8,25))
		
		#background jets
		with bgjet_front1:
			rep.modify.pose(position=rep.distribution.uniform((-20,240,2030), (20,260,2050)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)
		
		with bgjet_front2:
			rep.modify.pose(position=rep.distribution.uniform((1550,240,2030), (1570,260,2050)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)
		
		with bgjet_front3:
			rep.modify.pose(position=rep.distribution.uniform((-1570,240,2030), (-1550,260,2050)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)

		with bgjet_back1:
			rep.modify.pose(position=rep.distribution.uniform((-20,240,-2350), (20,260,-2330)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)

		with bgjet_back2:
			rep.modify.pose(position=rep.distribution.uniform((1550,240,-2350), (1570,260,-2330)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)

		with bgjet_back3:
			rep.modify.pose(position=rep.distribution.uniform((-1570,240,-2350), (-1550,260,-2330)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)

		with bgjet_left1:
			rep.modify.pose(position=rep.distribution.uniform((1550,240,-280), (1570,260,-260)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)
		
		with bgjet_right1:
			rep.modify.pose(position=rep.distribution.uniform((-1570,240,-280), (-1550,260,-260)),
			rotation=rep.distribution.uniform((0,-90,-180), (0,-90,180)),
			)
		#ground and sky
		with ground_xform:
			rep.modify.pose(rotation=rep.distribution.uniform((0,0,0), (360,0,360)))

	rp_front = rep.create.render_product(cameraFront, (1920, 1080))
	rp_back = rep.create.render_product(cameraBack, (1920, 1080))
	rp_left = rep.create.render_product(cameraLeft, (1920, 1080))
	rp_right = rep.create.render_product(cameraRight, (1920, 1080))

	writer = rep.WriterRegistry.get("BasicWriter")
	writer.initialize( output_dir="E:/Outsyders/GitHub/Omniverse_Blue_Angels_Training/Renders",
		rgb=True, #basic rgb color image output
		semantic_segmentation=True, #class segmentation image for each frame along with accompanying json file 
		distance_to_camera=True, #Numpy depth data output

	)
	#randomize output, all four cameras write to a single folder for further processing
	for rp in [rp_front, rp_back, rp_left, rp_right]:
		writer.attach(rp)
