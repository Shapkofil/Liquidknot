varying vec4 v_color;

// ToDo get consts from blender
const float PLANK = .0005;
const float MAX_DISTANCE = 100.;
const int MAX_STEP = 128;
const float EPSILON = .001;

const float ambient_factor = .1;

uniform vec2 resolution;

float sceneSDF(vec3 p)
{
	p = mod(p ,2.) - 1.;
	return length(p)-0.7;
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

	vec3 ro = vec3(0., 0., -1.);

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y /2.;
	vec3 rd = vec3(uv, 1.);

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
			gl_FragColor = (ambient + deffuse +specular) * vec4(.7, .3, .7, 1.);
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