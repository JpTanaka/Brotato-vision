func _process(delta)->void:
	if _wave_timer.time_left as int != _last_time_checked:
		_last_time_checked = _wave_timer.time_left as int
		var labels = ""
		var current_time = OS.get_datetime()
		var camera_position = _camera.get_camera_screen_center()
		var camera_corner = camera_position-get_viewport().get_visible_rect().size/2
		var camera_size =  get_viewport().get_visible_rect().size
		var image_data = get_viewport().get_texture().get_data()
		var file_path = "/Users/czartur/code/projects/Brotato-vision/images/rt/%s_%s" % [str(current_time.minute), str(current_time.second)]
		image_data.flip_y()
		image_data.save_png(file_path+".png")
		
		var elements = [_player]
		elements += _entity_spawner.enemies
		elements += _entity_spawner.neutrals
		elements += _consumables
		elements += _golds
		
		for element in elements:
			var x = (element.global_position[0]-camera_corner[0])/camera_size[0]
			var y = (element.global_position[1]-camera_corner[1])/camera_size[1]-0.01
			if x<0 or x>1 or y>1 or y<0: # out of the vision space
				continue
			
			var id
			if element is Entity:
				id = element.stats.id
			elif element is Consumable:
				id = element.consumable_data.id
			else: # element is Gold
				id = 36
			
			var label =  str(id)+ " " + str(x) + " " + str(y) + " " 
			label += str(element.sprite.texture.get_width()/camera_size[0]) + " " + str(element.sprite.texture.get_height()/camera_size[1])
			labels += label+"\n"
			
		var file = File.new()
		var result = file.open(file_path+".txt", File.WRITE)
		
		if result==OK:
			file.store_string(labels)
			file.close()
		else:
			print("Error:", result)