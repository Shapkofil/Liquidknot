uniform vec2 resolution;

float sceneSDF(in vec3 p)
{
	// pebble distance_estimator
}

vec4 sceneColor(in vec3 p)
{
	// pebble scene_color
}

vec3 estimateNormal(vec3 p)
{
	return normalize(vec3(
		sceneSDF(vec3(p.x+EPSILON,p.y,p.z)) - sceneSDF(vec3(p.x-EPSILON,p.y,p.z)),
		sceneSDF(vec3(p.x,p.y+EPSILON,p.z)) - sceneSDF(vec3(p.x,p.y-EPSILON,p.z)),
		sceneSDF(vec3(p.x,p.y,p.z+EPSILON)) - sceneSDF(vec3(p.x,p.y,p.z-EPSILON))
		));
}

vec4 calculateDeffuse(vec3 p)
{
	vec3 deffuse = vec3(0, 0, 0);
	for(int i = 0;i<light_count;i++)
	{
		vec3 normal = estimateNormal(p);
		vec3 lightdir = normalize(light_positions[i] - p);
		float diff = max(dot(normal,lightdir),0.0);
		deffuse += diff * light_colors[i].xyz;
	}
	return vec4(deffuse, 1.);
}

// ToDo Specular Pass

void main(){
	float distance = PLANK;

	vec3 ro = camera_position;

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.x;
	uv *= vec2(1, -1) * (sensor/2).x;
	vec3 rd = normalize(rotate_ray(vec3(uv, -focal_length), camera_rotation));

	int step = 0;
	float cd = PLANK;

	vec4 ambient;
	vec4 deffuse;
	vec4 specular;
	while(true){

		cd = sceneSDF(ro);
		distance = distance + cd;
		step++;
		ro = ro + rd * cd;

		if(cd < PLANK)
		{
			ambient = vec4(vec3(AMBIENT, AMBIENT, AMBIENT),.1);
			deffuse = calculateDeffuse(ro);
			specular = vec4(.0, .0, .0, .1);
			gl_FragColor = (ambient + deffuse + specular) * sceneColor(ro);
			break;
		}

		if(distance > MAX_DISTANCE)
		{
			gl_FragColor = WORLD_COLOR ;
			break;
		}

		if(step > MAX_STEP)
		{
			gl_FragColor = WORLD_COLOR ;
			break;
		}
	}
	
}