varying vec4 v_color;

const float PLANK = .1;
const float MAX_DISTANCE = 100.;
const int MAX_STEP = 48;

uniform vec2 resolution;

float sphere(vec3 p)
{
	return length(p) - 1.8;
}

void main(){
	float distance = PLANK;

	vec3 ro = vec3(.0, .0, -2.);

	// ToDo calculate uv
	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y;
	vec3 rd = vec3(uv, .1);

	int step = 0;
	float cd = PLANK;
	while(true){

		cd = sphere(ro);
		distance = distance + cd;
		step++;

		if(cd < PLANK){
			gl_FragColor = vec4(.8, .8, .8, 1.);
			break;
		}

		if(distance > MAX_DISTANCE)
		{
			gl_FragColor = vec4(.6, .0, .6, 1.);
			break;
		}

		if(step > MAX_STEP)
		{
			gl_FragColor = vec4(.0, .0, .0, 1.);
			break;
		}

		ro = ro + rd * cd;
	}
}