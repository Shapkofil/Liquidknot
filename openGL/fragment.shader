// ToDo get consts from blender
const float PLANK = .0005;
const float MAX_DISTANCE = 1000.;
const int MAX_STEP = 256;
const float EPSILON = .001;

const float ambient_factor = .1;

uniform vec2 resolution;

#define __pi__ 3.1415926535897932384626433832795

mat3 rotMatrix(vec3 rot)
{
	rot = -rot;
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
	p = mod(p,4.0) - 2.0;
	vec3 b = vec3(1.,1.,1.)*.5;
	vec3 q = abs(p) - b;
  	return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
}

vec3 estimateNormal(vec3 p)
{
	return normalize(vec3(
		sceneSDF(vec3(p.x+EPSILON,p.y,p.z)) - sceneSDF(vec3(p.x-EPSILON,p.y,p.z)),
		sceneSDF(vec3(p.x,p.y+EPSILON,p.z)) - sceneSDF(vec3(p.x,p.y-EPSILON,p.z)),
		sceneSDF(vec3(p.x,p.y,p.z+EPSILON)) - sceneSDF(vec3(p.x,p.y,p.z-EPSILON))
		));
}

vec4 calculateDeffuse(vec3 p,vec3 ligth_p,vec3 ligth_c)
{
	vec3 normal = estimateNormal(p);
	vec3 ligthdir = normalize(ligth_p - p);
	vec3 diff = max(dot(normal,ligthdir),0.0);
	return vec4(diff * ligth_c, 1.);
}

//ToDo check proper specular
vec4 calculateSpecular(vec3 p,vec3 ligth_p,vec3 ligth_c, vec3 view, float amount)
{
	vec3 normal = estimateNormal(p);
	vec3 ligthdir = normalize(ligth_p - p);
	vec3 reflected = reflect(-ligthdir, normal);
	vec3 diff = pow(max(dot(view,ligthdir),.0), 256);
	return vec4(amount * diff * ligth_c, 1.);
}

void main(){
	float distance = PLANK;

	vec3 ro = vec3(0.,0.,-1.);

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y /2.;
	vec3 rd = vec3(uv, 1.) * rotMatrix(vec3(0, __pi__/4, 0));

	vec3 ligth_p = vec3(1., 1., -1.);
	vec3 ligth_c = vec3(.4, .4, .4);

	int step = 0;
	float cd = PLANK;

	vec4 ambient;
	vec4 deffuse = vec4(.0, .0, .0, 1.);
	vec4 specular = vec4(.0, .0, .0, 1.);
	while(true){

		cd = sceneSDF(ro);
		distance = distance + cd;
		step++;
		ro = ro + rd * cd;

		if(cd < PLANK){
			ambient = vec4(vec3(ambient_factor, ambient_factor, ambient_factor),.1);
			deffuse = calculateDeffuse(ro,ligth_p,ligth_c);
			specular = calculateSpecular(ro,ligth_p,ligth_c,rd,2.0);
			gl_FragColor = (ambient + deffuse +specular) * vec4(.7, .3, .3, 1.);
			break;
		}

		if(distance > MAX_DISTANCE)
		{
			gl_FragColor = vec4(.01, .01, .01, 1.) ;
			break;
		}

		if(step > MAX_STEP)
		{
			gl_FragColor = vec4(.01, .01, .01, 1.) ;
			break;
		}
	}
	
}