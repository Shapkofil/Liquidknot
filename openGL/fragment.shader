varying vec4 v_color;

// ToDo get consts from blender
const float PLANK = .01;
const float MAX_DISTANCE = 100.;
const int MAX_STEP = 48;
const float EPSILON = .00001;

const float ambient_factor = .1;

uniform vec2 resolution;

float sceneSDF(vec3 p)
{
	return length(p)-0.4;
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

vec4 calculateSpecular(vec3 p,vec3 ligth_p,vec3 ligth_c, vec3 view, float amount)
{
	vec3 normal = estimateNormal(p);
	vec3 ligthdir = normalize(ligth_p - p);
	vec3 reflected = reflect(-ligthdir, normal);
	vec3 diff = pow(max(dot(view,ligthdir),.0), 8);
	return vec4(amount * diff * ligth_c, 1.);
}

void main(){
	float distance = PLANK;

	vec3 ro = vec3(0., 0., -1.);

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y;
	vec3 rd = vec3(uv, .85);

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
			ambient = vec4(1., 1., 1., 1.) * ambient_factor;
			deffuse = calculateDeffuse(ro,ligth_p,ligth_c);
			specular = calculateSpecular(ro,ligth_p,ligth_c,rd,500.0);
			break;
		}

		if(distance > MAX_DISTANCE)
		{
			ambient = vec4(.01, .01, .01, 1.);
			break;
		}

		if(step > MAX_STEP)
		{
			ambient = vec4(.01, .01, .01, 1.);
			break;
		}
	}
	ambient.w = 1.;
	gl_FragColor = (ambient + deffuse + specular) * vec4(.7,.3,.7,.1);
}