// pebble hyper_params

// pebble lights

uniform vec2 resolution;

#define __pi__ 3.1415926535897932384626433832795

float smin( float a, float b, float k )
{
    float h = max( k-abs(a-b), 0.0 )/k;
    return min( a, b ) - h*h*k*(1.0/4.0);
}

vec4 quat_conj(vec4 q)
{ 
  return vec4(-q.x, -q.y, -q.z, q.w); 
}
  
vec4 quat_mult(vec4 q1, vec4 q2)
{ 
  vec4 qr;
  qr.x = (q1.w * q2.x) + (q1.x * q2.w) + (q1.y * q2.z) - (q1.z * q2.y);
  qr.y = (q1.w * q2.y) - (q1.x * q2.z) + (q1.y * q2.w) + (q1.z * q2.x);
  qr.z = (q1.w * q2.z) + (q1.x * q2.y) - (q1.y * q2.x) + (q1.z * q2.w);
  qr.w = (q1.w * q2.w) - (q1.x * q2.x) - (q1.y * q2.y) - (q1.z * q2.z);
  return qr;
}

vec3 rotate_ray(vec3 position, vec4 qr)
{ 
	qr = vec4(qr.yzw,qr.x);
	vec4 qr_conj = quat_conj(qr);
	vec4 q_pos = vec4(position.x, position.y, position.z, 0);
	  
	vec4 q_tmp = quat_mult(qr, q_pos);
	qr = quat_mult(q_tmp, qr_conj);
	  
	return vec3(qr.x, qr.y, qr.z);
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

	vec3 ro = pebble camera_position;

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y;
	uv = vec2(uv[0], -uv[1]);
	vec3 rd = rotate_ray(normalize(vec3(uv, -pebble focal_lenght)), pebble camera_rotation);

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