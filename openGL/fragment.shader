// pebble hyper_params

// pebble lights

uniform vec2 resolution;

#define __pi__ 3.1415926535897932384626433832795

mat3 rotMatrix(vec3 rot)
{
	mat3 XY = mat3(
		cos(rot[2]),-sin(rot[2]),0,
		sin(rot[2]), cos(rot[2]),0,
		          0,           0,1);
	mat3 XZ = mat3(
		cos(rot[1]),0,-sin(rot[1]),
		          0,1,           0,
		sin(rot[1]),0, cos(rot[1]));
	mat3 YZ = mat3(
		1,          0,           0,
		0,cos(rot[0]),-sin(rot[0]),
		0,sin(rot[0]), cos(rot[0]));
	return XY * XZ * YZ;

}

float sceneSDF(in vec3 p)
{
	// pebble distance_estimator
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
		vec3 diff = max(dot(normal,lightdir),0.0);
		deffuse += diff * light_colors[i];
	}
	return vec4(deffuse, 1.);
}

// ToDo Specular Pass

void main(){
	float distance = PLANK;

	vec3 ro = // pebble camera_position;

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y;
	vec3 rd = vec3(uv, 1.) * rotMatrix( pebble camera_rotation );

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
			gl_FragColor = (ambient + deffuse + specular) * vec4(.9, .3, .0, 1.);
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