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
	n = normalize(n);
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
	vec2 d = abs(vec2(length(p.xz),p.y)) - vec2(h,r);
	return min(max(d.x,d.y),0.0) + length(max(d,0.0));
}

float sdCylinder( vec3 p, vec3 c )
{
	return length(p.xz-c.xy)-c.z;
}

float sdTorus( vec3 p, vec2 t )
{
	vec2 q = vec2(length(p.xz)-t.x,p.y);
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

float sdPyramid( vec3 p, float h)
{
	float m2 = h*h + 0.25;

	p.xz = abs(p.xz);
	p.xz = (p.z>p.x) ? p.zx : p.xz;
	p.xz -= 0.5;

	vec3 q = vec3( p.z, h*p.y - 0.5*p.x, h*p.x + 0.5*p.y);

	float s = max(-q.x,0.0);
	float t = clamp( (q.y-0.5*p.z)/(m2+0.25), 0.0, 1.0 );

	float a = m2*(q.x+s)*(q.x+s) + q.y*q.y;
	float b = m2*(q.x+0.5*t)*(q.x+0.5*t) + (q.y-m2*t)*(q.y-m2*t);

	float d2 = min(q.y,-q.x*m2-q.y*0.5) > 0.0 ? 0.0 : min(a,b);

	return sqrt( (d2+q.z*q.z)/m2 ) * sign(max(q.z,-p.y));
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

// ToDo get consts from blender
const float PLANK = .0005;
const float MAX_DISTANCE = 1000.;
const int MAX_STEP = 256;
const float EPSILON = .001;

const vec3 camera_position = vec3(-0.15561789274215698, -17.529552459716797, 3.605412483215332);
const vec4 camera_rotation = vec4(0.758284866809845, 0.6519233584403992, 0.0, 0.0);
const float focal_length = 4.166666666666667;

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

float LK_Cube( vec3 p )
{
    p -= vec3(-6.0, 0.0, 0.0);
    p = rotate_ray(p, vec4(1.0, 0.0, 0.0, 0.0));
    return sdBox(p, vec3(1.0, 1.0, 1.0));
}

float LK_Sphere( vec3 p )
{
    p -= vec3(-2.0, 0.0, 0.0);
    p = rotate_ray(p, vec4(1.0, 0.0, 0.0, 0.0));
    return sdEllipsoid(p, vec3(1.0, 1.0, 1.0));
}

float LK_Torus_001( vec3 p )
{
    p -= vec3(2.0, 0.0, 0.0);
    p = rotate_ray(p, vec4(1.0, 0.0, 0.0, 0.0));
    return sdTorus(p, vec2(1.0, 0.25));
}

float LK_Capsule( vec3 p )
{
    p -= vec3(6.0, 0.0, 0.0);
    p = rotate_ray(p, vec4(1.0, 0.0, 0.0, 0.0));
    return sdVerticalCapsule(p, 1.674194097518921, 0.4185485243797302);
}

float sceneSDF(in vec3 p)
{
	return opUnion(LK_Capsule(p) , opUnion(LK_Torus_001(p) , opUnion(LK_Sphere(p) , LK_Cube(p) ) ) );
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

	vec3 ro = camera_position;

	vec2 uv = (2.*gl_FragCoord.xy - resolution) / resolution.y;
	uv = vec2(uv[0], -uv[1]);
	vec3 rd = rotate_ray(normalize(vec3(uv, -focal_length)), camera_rotation);

	vec3 ligth_p = vec3(1., 1., -1.);
	vec3 ligth_c = vec3(.9, .9, .9);

	int step = 0;
	float cd = PLANK;

	vec4 ambient;
	vec4 deffuse = vec4(.0, .0, .0, 1.);
	vec4 specular = vec4(.0, .0, .0, 1.);
	float _min = 10000.;
	float thickness = .035;
	while(true){

		cd = sceneSDF(ro);
		_min = cd < _min ? cd : _min;
		distance = distance + cd;
		step++;
		ro = ro + rd * cd;

		if(cd < PLANK){
			ambient = vec4(vec3(ambient_factor, ambient_factor, ambient_factor),.1);
			deffuse = calculateDeffuse(ro,ligth_p,ligth_c);
			specular = calculateSpecular(ro,ligth_p,ligth_c,rd,2.0);
			gl_FragColor = (ambient + deffuse) * vec4(.15, .15, .15, 1.);
			break;
		}

		if(distance > MAX_DISTANCE)
		{
			gl_FragColor = vec4(.0, .0, .0, 1.) ;
			break;
		}

		if(step > MAX_STEP)
		{
			gl_FragColor = vec4(.0, .0, .0, 1.) ;
			break;
		}
	}
	if(_min>=PLANK && _min<= thickness)
	{
		gl_FragColor = vec4(.7, .7, .7, 1.);
	}
}