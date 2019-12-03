
	var map = new BMap.Map("allmap"); 
	var point = new BMap.Point(117.201108,39.137231); 
	map.centerAndZoom(point, 17);
	map.addControl(new BMap.MapTypeControl({
		mapTypes:[
            BMAP_NORMAL_MAP,
            BMAP_HYBRID_MAP
        ]}));	  
	map.setCurrentCity("北京");
	map.enableScrollWheelZoom(true);
	var marker = new BMap.Marker(point, {
			icon: new BMap.Symbol(BMap_Symbol_SHAPE_POINT, {
				scale: 1.5,
				fillColor: "orange",
				fillOpacity: 0.8
			})
		}
		);
		map.addOverlay(marker); 
		marker.enableDragging(); 

		var ctrl = new BMapLib.TrafficControl({
            showPanel: false
        });      
        map.addControl(ctrl);
        ctrl.setAnchor(BMAP_ANCHOR_BOTTOM_RIGHT);