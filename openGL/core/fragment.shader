// Math constants

#define __pi__ 3.1415926535897932384626433832795

// Utils libs

float smooth_border(float x)
{
	return ( x<__pi__ && x>-__pi__ ) ? (cos(x) + 1)/2 : 0;
}

vec4 csdf(float sdf, vec4 color, float falloff)
{
	return smooth_border((sdf * __pi__) / falloff / 2) * color;
}

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

// Primitive DE Lib

float sdSphere( vec3 p, float r )
{
	return length(p) - r;
}

float sdEllipsoid( vec3 p, vec3 r )
{
	float k0 = length(p/r);
	float k1 = length(p/(r*r));
	return k0*(k0-1.0)/k1;
}

float sdBox( vec3 p, vec3 b)
{
	b/=2;
	vec3 q = abs(p) - b;
	return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0);
}

float sdRoundBox( vec3 p, vec3 b, float r )
{
	vec3 q = abs(p) - b;
	return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0) - r;
}

float sdPlane( vec3 p, vec4 n )
{
	//n = normalize(n);
	return dot(p,n.xyz) + n.w;
}

float sdCapsule( vec3 p, vec3 a, vec3 b, float r )
{
	vec3 pa = p - a, ba = b - a;
	float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
	return length( pa - ba*h ) - r;
}

float sdVerticalCapsule( vec3 p, float h, float r )
{
	p -= vec3(0, 0, -h/2);
	p.z -= clamp( p.z, 0.0, h );
	return length( p ) - r;
}

float sdCappedCylinder( vec3 p, float h, float r )
{
	vec2 d = abs(vec2(length(p.xy),p.z)) - vec2(r,h);
	return min(max(d.x,d.y),0.0) + length(max(d,0.0));
}

float sdCylinder( vec3 p, vec3 c )
{
	return length(p.xy-c.xy)-c.z;
}

float sdTorus( vec3 p, float outer, float inner)
{
	vec2 t = vec2(outer, inner);
	vec2 q = vec2(length(p.xy)-t.x,p.z);
	return length(q)-t.y;
}

float sdOctahedron( vec3 p, float s)
{
	p = abs(p);
	float m = p.x+p.y+p.z-s;
	vec3 q;
	   if( 3.0*p.x < m ) q = p.xyz;
	else if( 3.0*p.y < m ) q = p.yzx;
	else if( 3.0*p.z < m ) q = p.zxy;
	else return m*0.57735027;

	float k = clamp(0.5*(q.z-q.y+s),0.0,s); 
	return length(vec3(q.x,q.y-s+k,q.z-k)); 
}

float dot2( vec3 v )
{
	return dot(v,v);
}

float udTriangle( vec3 p, vec3 a, vec3 b, vec3 c )
{
	vec3 ba = b - a; vec3 pa = p - a;
	vec3 cb = c - b; vec3 pb = p - b;
	vec3 ac = a - c; vec3 pc = p - c;
	vec3 nor = cross( ba, ac );

	return sqrt(
	(sign(dot(cross(ba,nor),pa)) +
	 sign(dot(cross(cb,nor),pb)) +
	 sign(dot(cross(ac,nor),pc))<2.0)
	 ?
	 min( min(
	 dot2(ba*clamp(dot(ba,pa)/dot2(ba),0.0,1.0)-pa),
	 dot2(cb*clamp(dot(cb,pb)/dot2(cb),0.0,1.0)-pb) ),
	 dot2(ac*clamp(dot(ac,pc)/dot2(ac),0.0,1.0)-pc) )
	 :
	 dot(nor,pa)*dot(nor,pa)/dot2(nor) );
}

float udQuad( vec3 p, vec3 a, vec3 b, vec3 c, vec3 d )
{
	vec3 ba = b - a; vec3 pa = p - a;
	vec3 cb = c - b; vec3 pb = p - b;
	vec3 dc = d - c; vec3 pc = p - c;
	vec3 ad = a - d; vec3 pd = p - d;
	vec3 nor = cross( ba, ad );

	return sqrt(
	(sign(dot(cross(ba,nor),pa)) +
	 sign(dot(cross(cb,nor),pb)) +
	 sign(dot(cross(dc,nor),pc)) +
	 sign(dot(cross(ad,nor),pd))<3.0)
	 ?
	 min( min( min(
	 dot2(ba*clamp(dot(ba,pa)/dot2(ba),0.0,1.0)-pa),
	 dot2(cb*clamp(dot(cb,pb)/dot2(cb),0.0,1.0)-pb) ),
	 dot2(dc*clamp(dot(dc,pc)/dot2(dc),0.0,1.0)-pc) ),
	 dot2(ad*clamp(dot(ad,pd)/dot2(ad),0.0,1.0)-pd) )
	 :
	 dot(nor,pa)*dot(nor,pa)/dot2(nor) );
}


// Unions lib
float opUnion( float d1, float d2 ) {  return min(d1,d2); }

float opSubtraction( float d1, float d2 ) { return max(-d1,d2); }

float opIntersection( float d1, float d2 ) { return max(d1,d2); }

float opSmoothUnion( float d1, float d2, float k ) {
    float h = clamp( 0.5 + 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) - k*h*(1.0-h); }

float opSmoothSubtraction( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2+d1)/k, 0.0, 1.0 );
    return mix( d2, -d1, h ) + k*h*(1.0-h); }

float opSmoothIntersection( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) + k*h*(1.0-h); }


// Fractal Lib
float sdMandelbulb(vec3 p, int iters, float power, float bailout)
{
	vec3 z = p;
	float dr = 1.0;
	float r = 0.0;
	for (int i = 0; i < iters ; i++) {
		r = length(z);
		if (r>bailout) break;
		
		// convert to polar coordinates
		float theta = acos(z.z/r);
		float phi = atan(z.y,z.x);
		dr =  pow( r, power-1.0)*power*dr + 1.0;
		
		// scale and rotate the point
		float zr = pow( r,power);
		theta = theta*power;
		phi = phi*power;
		
		// convert back to cartesian coordinates
		z = zr*vec3(sin(theta)*cos(phi), sin(phi)*sin(theta), cos(theta));
		z+=p;
	}
	return 0.5*log(r)*r/dr;
} 
const float PLANK = 0.004999999888241291;
const float MAX_DISTANCE = 1000.0;
const float EPSILON = 0.004999999888241291;
const float AMBIENT = 0.1;
const int MAX_STEP = 256;
const vec4 WORLD_COLOR = vec4(0.0, 0.0, 0.0, 1.0);

const vec3 camera_position = vec3(7.53312349319458, -9.912906646728516, 2.522969961166382);
const vec4 camera_rotation = vec4(0.719944417476654, 0.6214413046836853, 0.20191822946071625, 0.23392260074615479);
const float focal_length = 50.0;

const vec2 sensor = vec2(36.0, 24.0);

const float light_count = 3;
const vec3 light_positions[3] = {vec3(-23.556310653686523, 16.937835693359375, 2.0), vec3(20.257213592529297, -20.77102279663086, 2.0), vec3(-13.044283866882324, -25.91595458984375, 2.0)};
const vec4 light_colors[3] = {vec4(1.0, 1.0, 1.0, 1.0), vec4(1.0, 1.0, 1.0, 1.0), vec4(1.0, 1.0, 1.0, 1.0)};

float LK_Cube( vec3 p )
{
    p -= vec3(-2.0, 0.0, 1.0);
    p = rotate_ray(p, vec4(-1., 1., 1., 1.) * vec4(1.0, 0.0, 0.0, 0.0));
    return sdBox(p, vec3(0.5, 0.5, 3.0));
}

float LK_Cube_001( vec3 p )
{
    p -= vec3(-1.25, 0.0, -0.25);
    p = rotate_ray(p, vec4(-1., 1., 1., 1.) * vec4(0.7071067690849304, 0.0, 0.7071067690849304, 0.0));
    return sdBox(p, vec3(0.5, 0.5, 2.0));
}

float LK_Cube_002( vec3 p )
{
    p -= vec3(0.0, 0.0, 0.0);
    p = rotate_ray(p, vec4(-1., 1., 1., 1.) * vec4(1.0, 0.0, 0.0, 0.0));
    return sdBox(p, vec3(0.5, 0.5, 3.0));
}

float LK_Cube_004( vec3 p )
{
    p -= vec3(0.0, 0.8510887622833252, -0.6055018901824951);
    p = rotate_ray(p, vec4(-1., 1., 1., 1.) * vec4(0.28462716937065125, -0.6450599431991577, 0.6505677103996277, 0.28221750259399414));
    return sdBox(p, vec3(0.5, 0.5000000596046448, 1.8799852132797241));
}

float LK_Cube_003( vec3 p )
{
    p -= vec3(0.0, 0.8026113510131836, 0.7105096578598022);
    p = rotate_ray(p, vec4(-1., 1., 1., 1.) * vec4(-0.23758260905742645, -0.6638293862342834, 0.6661657094955444, -0.24312184751033783));
    return sdBox(p, vec3(0.5, 0.5000000596046448, 1.8799850940704346));
}

uniform vec2 resolution;

float sceneSDF(in vec3 p)
{
	return opSmoothUnion(LK_Cube_003(p) , opSmoothUnion(LK_Cube_004(p) , opSmoothUnion(LK_Cube_002(p) , opSmoothUnion(LK_Cube_001(p) , LK_Cube(p), 0.05000000074505806), 0.05000000074505806), 0.05000000074505806), 0.05000000074505806);
}

vec4 sceneColor(in vec3 p)
{
	return normalize(csdf(LK_Cube(p), vec4(0.8, 0.8, 0.8, 1.0), 0.05000000074505806) + csdf(LK_Cube_001(p), vec4(0.8, 0.8, 0.8, 1.0), 0.02500000037252903) + csdf(LK_Cube_002(p), vec4(0.8, 0.8, 0.8, 1.0), 0.02500000037252903) + csdf(LK_Cube_004(p), vec4(0.8, 0.8, 0.8, 1.0), 0.02500000037252903) + csdf(LK_Cube_003(p), vec4(0.8, 0.8, 0.8, 1.0), 0.02500000037252903));
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

vec4 colorpow(vec4 p, float value)
{
	return vec4(pow(p.x,value),
				pow(p.y,value),
				pow(p.z,value),
				pow(p.w,value));
}

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

	float _min = 10000.;
	float thickness = .2;
	while(true){

		cd = sceneSDF(ro);
		distance = distance + cd;
		step++;
		_min = _min > cd ? cd : _min;
		ro = ro + rd * cd;

		if(cd < PLANK)
		{
			ambient = vec4(vec3(AMBIENT, AMBIENT, AMBIENT),.1);
			deffuse = calculateDeffuse(ro);
			specular = vec4(.0, .0, .0, .1);
			gl_FragColor = colorpow((ambient + deffuse + specular) * sceneColor(ro), 16.);
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
	if(_min >= PLANK && _min <= thickness)
	{
		gl_FragColor = colorpow(vec4(1., 1., 1., 1.) * _min/thickness * -1 + 1, 8.);
	}
}