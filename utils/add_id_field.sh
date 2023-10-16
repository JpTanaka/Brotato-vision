original_path=$(pwd)

# add id to tree, fruit, item_box, legendary_item_box 
echo "id = 35" >> entities/units/neutral/tree_stats.tres
echo "id->tree"
echo "id = 37" >> items/consumables/fruit/fruit_data.tres
echo "id->fruit"
echo "id = 38" >> items/consumables/item_box/item_box_data.tres
echo "id->item_box"
echo "id = 39" >> items/consumables/legendary_item_box/legendary_item_box_data.tres
echo "id->legendary_item_box"

# add id to all enemies
cd entities/units/enemies
for dir in $(ls); do
	if [[ $dir =~ ^[0-9]+$ ]]; then
		cd $dir
		
		number=$(echo $dir | sed 's/^0*//')
		filename="${number}_stats.tres"
		if [ ! -f "$filename" ]; then
		       	echo "'$filename' not found"
			cd ..
			exit 1
		fi

		#cat $filename | sed "s/^id = .*/id = $number/" > $filename
		echo "id = $number" >> $filename
		echo "id->$dir"
		cd ..
	fi
done

cd $original_path 


# add id to stats and consumable_data
id_line="export (int) var id = 0" 
echo "$id_line" >> items/consumables/consumable_data.gd
echo "+$id_line -> consumable_data.gd"
echo "$id_line" >> entities/units/unit/stats.gd
echo "+$id_line -> stats.gd"

