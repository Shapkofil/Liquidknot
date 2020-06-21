// Math constants

const float pi = 3.1415926535897932384626433832795;

// Utils libs

float smooth_border(float x)
{
	return ( x<pi && x> -pi) ? (cos(x) + 1.)/2. : .0;
}

vec4 csdf(float sdf, vec4 color, float falloff)
{
	return smooth_border((sdf * pi) / falloff / 2.) * color;
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
	b/=2.;
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
	p -= vec3(0, 0, -h/2.);
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
// Abstact and Noise Lib

float sdSinField(vec3 p ,vec3 b)
{
  return sin(p.x*b.x)*sin(p.y*b.y)*sin(p.z*b.z);
}


//	Simplex 3D Noise
//	by Ian McEwan, Ashima Arts

vec4 permute(vec4 x){return mod(((x*34.0)+1.0)*x, 289.0);}
vec4 taylorInvSqrt(vec4 r){return 1.79284291400159 - 0.85373472095314 * r;}
float SimplexNoise(vec3 v, float N){
  const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
  const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);

  vec3 i  = floor(v + dot(v, C.yyy) );
  vec3 x0 =   v - i + dot(i, C.xxx) ;

  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min( g.xyz, l.zxy );
  vec3 i2 = max( g.xyz, l.zxy );

  vec3 x1 = x0 - i1 + 1.0 * C.xxx;
  vec3 x2 = x0 - i2 + 2.0 * C.xxx;
  vec3 x3 = x0 - 1. + 3.0 * C.xxx;

  i = mod(i, 289.0 );
  vec4 p = permute( permute( permute(
             i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
           + i.y + vec4(0.0, i1.y, i2.y, 1.0 ))
           + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));

  float n_ = 1.0/N;
  vec3  ns = n_ * D.wyz - D.xzx;

  vec4 j = p - 49.0 * floor(p * ns.z *ns.z);

  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_ );

  vec4 x = x_ *ns.x + ns.yyyy;
  vec4 y = y_ *ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);

  vec4 b0 = vec4( x.xy, y.xy );
  vec4 b1 = vec4( x.zw, y.zw );

  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));

  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;

  vec3 p0 = vec3(a0.xy,h.x);
  vec3 p1 = vec3(a0.zw,h.y);
  vec3 p2 = vec3(a1.xy,h.z);
  vec3 p3 = vec3(a1.zw,h.w);

  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;

  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1),
                                dot(p2,x2), dot(p3,x3) ) );
}

// Operator lib

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

float opSmoothEdges( float p , float r ){ return p - r; }


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
