// Made with Amplify Shader Editor
// Available at the Unity Asset Store - http://u3d.as/y3X 
Shader "SandyTop"
{
	Properties
	{
		_GlobalMetalness("Global Metalness", Float) = 0
		_GlobalSmoothness("Global Smoothness", Range( 0 , 1)) = 0
		[NoScaleOffset]_NoiseMap("Noise Map", 2D) = "white" {}
		_DiscolorationFadet("Discoloration Fadet", Range( 0 , 1)) = 1
		_DiscolorScale1("Discolor Scale", Range( 0 , 1)) = 0.5423828
		_DiscolorationContrast("Discoloration Contrast", Range( 0 , 2)) = 0.5
		_DiscolorationIntensity("Discoloration Intensity", Range( 0 , 3)) = 1.494118
		_AlbedoTint("Albedo Tint", Color) = (1,1,1,0)
		[NoScaleOffset]_RockAlbedo("Main Albedo", 2D) = "white" {}
		[NoScaleOffset]_RockNormal("Main Normal", 2D) = "bump" {}
		_RockNormalIntensity("Main Normal Intensity", Float) = 1
		_RockTiling("Main Tiling", Float) = 1
		_RockRotation("Main Rotation", Float) = 0
		_RockOffset("Main Offset", Vector) = (0,0,0,0)
		[NoScaleOffset]_RockDetailNormal("Detail Normal", 2D) = "bump" {}
		_DetailNormalIntensity("Detail Normal Intensity", Float) = 1
		_RockDetailNormalTiling("Detail Normal Tiling", Float) = 1
		_RockDetailNormalRotation("Detail Normal Rotation", Float) = 0
		_RockDetailNormalOffset("Detail Normal Offset", Vector) = (0,0,0,0)
		[NoScaleOffset]_SandAlbedoA("Sand Albedo A", 2D) = "white" {}
		[NoScaleOffset]_SandNormalA("Sand Normal A", 2D) = "bump" {}
		_SandATiling("Sand A Tiling", Range( 0 , 0.5)) = 0.5
		[NoScaleOffset]_SandAlbedoB("Sand Albedo B", 2D) = "white" {}
		[NoScaleOffset]_SandNormalB("Sand Normal B", 2D) = "bump" {}
		_SandBTiling("Sand B Tiling", Range( 0 , 0.5)) = 0.5
		_SandFalloff("Sand Main Opacity", Range( 0 , 10)) = 7
		_SandCoverage("Sand Vertical Distance", Range( -10 , 10)) = 2
		[Toggle]_UseHeightBlending("Use Noise For Sand Opacity", Float) = 1
		_HeightTiling("Sand Noise Tiling", Range( 0 , 0.5)) = 0.5
		_HeightFalloff("Sand Noise Opacity Blur", Range( 0 , 1)) = 1
		_SandNoiseBlendOffset("Sand A/B Blend Offset", Vector) = (0,0,0,0)
		_SandNoiseBlendTiling("Sand A/B Blend Tiling", Float) = 1
		[Toggle(_USEFRESNEL_ON)] _UseFresnel("Use Fresnel", Float) = 0
		_F_Bias("F_Bias", Float) = 0
		_F_Scale("F_Scale", Float) = 2.5
		_F_Power("F_Power", Float) = 6
		_F_Distance("F_Distance", Float) = 256
		[HideInInspector] _texcoord( "", 2D ) = "white" {}
		[HideInInspector] __dirty( "", Int ) = 1
	}

	SubShader
	{
		Tags{ "RenderType" = "Opaque"  "Queue" = "Geometry+0" }
		Cull Back
		ZTest LEqual
		CGINCLUDE
		#include "UnityStandardUtils.cginc"
		#include "UnityShaderVariables.cginc"
		#include "UnityPBSLighting.cginc"
		#include "Lighting.cginc"
		#pragma target 3.0
		#pragma shader_feature_local _USEFRESNEL_ON
		#ifdef UNITY_PASS_SHADOWCASTER
			#undef INTERNAL_DATA
			#undef WorldReflectionVector
			#undef WorldNormalVector
			#define INTERNAL_DATA half3 internalSurfaceTtoW0; half3 internalSurfaceTtoW1; half3 internalSurfaceTtoW2;
			#define WorldReflectionVector(data,normal) reflect (data.worldRefl, half3(dot(data.internalSurfaceTtoW0,normal), dot(data.internalSurfaceTtoW1,normal), dot(data.internalSurfaceTtoW2,normal)))
			#define WorldNormalVector(data,normal) half3(dot(data.internalSurfaceTtoW0,normal), dot(data.internalSurfaceTtoW1,normal), dot(data.internalSurfaceTtoW2,normal))
		#endif
		struct Input
		{
			float2 uv_texcoord;
			float3 worldPos;
			half3 worldNormal;
			INTERNAL_DATA
			float eyeDepth;
		};

		uniform sampler2D _RockNormal;
		uniform half _RockTiling;
		uniform half2 _RockOffset;
		uniform half _RockRotation;
		uniform half _RockNormalIntensity;
		uniform sampler2D _RockDetailNormal;
		uniform half _RockDetailNormalTiling;
		uniform half2 _RockDetailNormalOffset;
		uniform half _RockDetailNormalRotation;
		uniform half _DetailNormalIntensity;
		uniform sampler2D _SandNormalA;
		uniform half _SandATiling;
		uniform sampler2D _SandNormalB;
		uniform half _SandBTiling;
		uniform sampler2D _NoiseMap;
		uniform half _SandNoiseBlendTiling;
		uniform half2 _SandNoiseBlendOffset;
		uniform half _SandFalloff;
		uniform half _SandCoverage;
		uniform half _HeightTiling;
		uniform half _UseHeightBlending;
		uniform half _HeightFalloff;
		uniform half4 _AlbedoTint;
		uniform sampler2D _RockAlbedo;
		uniform sampler2D _SandAlbedoA;
		uniform sampler2D _SandAlbedoB;
		uniform half _DiscolorationContrast;
		uniform half _DiscolorScale1;
		uniform half _DiscolorationIntensity;
		uniform half _DiscolorationFadet;
		uniform half _F_Bias;
		uniform half _F_Scale;
		uniform half _F_Power;
		uniform half _F_Distance;
		uniform half _GlobalMetalness;
		uniform half _GlobalSmoothness;


		inline float4 TriplanarSampling410( sampler2D topTexMap, float3 worldPos, float3 worldNormal, float falloff, float2 tiling, float3 normalScale, float3 index )
		{
			float3 projNormal = ( pow( abs( worldNormal ), falloff ) );
			projNormal /= ( projNormal.x + projNormal.y + projNormal.z ) + 0.00001;
			float3 nsign = sign( worldNormal );
			half4 xNorm; half4 yNorm; half4 zNorm;
			xNorm = tex2D( topTexMap, tiling * worldPos.zy * float2(  nsign.x, 1.0 ) );
			yNorm = tex2D( topTexMap, tiling * worldPos.xz * float2(  nsign.y, 1.0 ) );
			zNorm = tex2D( topTexMap, tiling * worldPos.xy * float2( -nsign.z, 1.0 ) );
			return xNorm * projNormal.x + yNorm * projNormal.y + zNorm * projNormal.z;
		}


		float4 CalculateContrast( float contrastValue, float4 colorTarget )
		{
			float t = 0.5 * ( 1.0 - contrastValue );
			return mul( float4x4( contrastValue,0,0,t, 0,contrastValue,0,t, 0,0,contrastValue,t, 0,0,0,1 ), colorTarget );
		}

		void vertexDataFunc( inout appdata_full v, out Input o )
		{
			UNITY_INITIALIZE_OUTPUT( Input, o );
			o.eyeDepth = -UnityObjectToViewPos( v.vertex.xyz ).z;
		}

		void surf( Input i , inout SurfaceOutputStandard o )
		{
			half2 temp_cast_0 = (_RockTiling).xx;
			float2 uv_TexCoord335 = i.uv_texcoord * temp_cast_0 + _RockOffset;
			float cos403 = cos( _RockRotation );
			float sin403 = sin( _RockRotation );
			half2 rotator403 = mul( uv_TexCoord335 - float2( 1,1 ) , float2x2( cos403 , -sin403 , sin403 , cos403 )) + float2( 1,1 );
			half2 RockTiling342 = rotator403;
			half2 temp_cast_1 = (_RockDetailNormalTiling).xx;
			float2 uv_TexCoord339 = i.uv_texcoord * temp_cast_1 + _RockDetailNormalOffset;
			float cos402 = cos( _RockDetailNormalRotation );
			float sin402 = sin( _RockDetailNormalRotation );
			half2 rotator402 = mul( uv_TexCoord339 - float2( 1,1 ) , float2x2( cos402 , -sin402 , sin402 , cos402 )) + float2( 1,1 );
			half2 RockDetailTiling343 = rotator402;
			half3 temp_output_248_0 = BlendNormals( UnpackScaleNormal( tex2D( _RockNormal, RockTiling342 ), _RockNormalIntensity ) , UnpackScaleNormal( tex2D( _RockDetailNormal, RockDetailTiling343 ), _DetailNormalIntensity ) );
			half3 BaseNormals452 = temp_output_248_0;
			float3 ase_worldPos = i.worldPos;
			half2 appendResult370 = (half2(ase_worldPos.x , ase_worldPos.z));
			half2 SandATiling_A338 = ( _SandATiling * appendResult370 );
			half2 appendResult393 = (half2(ase_worldPos.x , ase_worldPos.z));
			half2 SandBTiling_A341 = ( appendResult393 * _SandBTiling );
			half2 temp_cast_2 = (_SandNoiseBlendTiling).xx;
			float2 uv_TexCoord425 = i.uv_texcoord * temp_cast_2 + _SandNoiseBlendOffset;
			half noiseGen432 = tex2D( _NoiseMap, uv_TexCoord425 ).r;
			half3 lerpResult35 = lerp( UnpackNormal( tex2D( _SandNormalA, SandATiling_A338 ) ) , UnpackNormal( tex2D( _SandNormalB, SandBTiling_A341 ) ) , noiseGen432);
			half3 ase_worldNormal = WorldNormalVector( i, half3( 0, 0, 1 ) );
			half temp_output_252_0 = (ase_worldNormal.y*_SandFalloff + _SandCoverage);
			half2 appendResult369 = (half2(ase_worldPos.x , ase_worldPos.z));
			half2 appendResult379 = (half2(ase_worldPos.x , ase_worldPos.y));
			half2 appendResult380 = (half2(ase_worldPos.y , ase_worldPos.z));
			half lerpResult265 = lerp( temp_output_252_0 , (( 1.0 - 10.0 ) + (( temp_output_252_0 * ( tex2D( _NoiseMap, ( _HeightTiling * appendResult369 ) ).g * tex2D( _NoiseMap, ( _HeightTiling * appendResult379 ) ).g * tex2D( _NoiseMap, ( _HeightTiling * appendResult380 ) ).g ) ) - 0.0) * (10.0 - ( 1.0 - 10.0 )) / (1.0 - 0.0)) , (( _UseHeightBlending )?( ( 1.0 - _HeightFalloff ) ):( 0.0 )));
			half sandSettings254 = saturate( lerpResult265 );
			half3 lerpResult15 = lerp( BaseNormals452 , BlendNormals( temp_output_248_0 , lerpResult35 ) , sandSettings254);
			o.Normal = lerpResult15;
			half4 lerpResult37 = lerp( tex2D( _SandAlbedoA, SandATiling_A338 ) , tex2D( _SandAlbedoB, SandBTiling_A341 ) , noiseGen432);
			half4 lerpResult10 = lerp( ( _AlbedoTint * tex2D( _RockAlbedo, RockTiling342 ) ) , lerpResult37 , sandSettings254);
			half lerpResult407 = lerp( 0.5 , 0.0005 , _DiscolorScale1);
			float4 triplanar410 = TriplanarSampling410( _NoiseMap, ase_worldPos, ase_worldNormal, 1.0, ( half2( 0.1,0.1 ) * lerpResult407 ), 1.0, 0 );
			half4 lerpResult417 = lerp( lerpResult10 , ( ( CalculateContrast(_DiscolorationContrast,triplanar410) * _DiscolorationIntensity ) * lerpResult10 ) , _DiscolorationFadet);
			half3 _Vector0 = half3(0,0,0);
			half3 ase_worldViewDir = normalize( UnityWorldSpaceViewDir( ase_worldPos ) );
			half3 ase_worldTangent = WorldNormalVector( i, half3( 1, 0, 0 ) );
			half3 ase_worldBitangent = WorldNormalVector( i, half3( 0, 1, 0 ) );
			half3x3 ase_tangentToWorldFast = float3x3(ase_worldTangent.x,ase_worldBitangent.x,ase_worldNormal.x,ase_worldTangent.y,ase_worldBitangent.y,ase_worldNormal.y,ase_worldTangent.z,ase_worldBitangent.z,ase_worldNormal.z);
			half fresnelNdotV438 = dot( mul(ase_tangentToWorldFast,BaseNormals452), ase_worldViewDir );
			half fresnelNode438 = ( _F_Bias + _F_Scale * pow( 1.0 - fresnelNdotV438, _F_Power ) );
			half3 temp_cast_4 = (fresnelNode438).xxx;
			half3 lerpResult440 = lerp( temp_cast_4 , _Vector0 , sandSettings254);
			half cameraDepthFade444 = (( i.eyeDepth -_ProjectionParams.y - 0.0 ) / _F_Distance);
			half clampResult449 = clamp( cameraDepthFade444 , 0.0 , 1.0 );
			#ifdef _USEFRESNEL_ON
				half3 staticSwitch441 = ( lerpResult440 * ( 1.0 - clampResult449 ) );
			#else
				half3 staticSwitch441 = _Vector0;
			#endif
			half3 fresnel451 = staticSwitch441;
			o.Albedo = ( lerpResult417 + half4( fresnel451 , 0.0 ) ).rgb;
			o.Metallic = _GlobalMetalness;
			o.Smoothness = _GlobalSmoothness;
			o.Alpha = 1;
		}

		ENDCG
		CGPROGRAM
		#pragma surface surf Standard keepalpha fullforwardshadows vertex:vertexDataFunc 

		ENDCG
		Pass
		{
			Name "ShadowCaster"
			Tags{ "LightMode" = "ShadowCaster" }
			ZWrite On
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#pragma target 3.0
			#pragma multi_compile_shadowcaster
			#pragma multi_compile UNITY_PASS_SHADOWCASTER
			#pragma skip_variants FOG_LINEAR FOG_EXP FOG_EXP2
			#include "HLSLSupport.cginc"
			#if ( SHADER_API_D3D11 || SHADER_API_GLCORE || SHADER_API_GLES || SHADER_API_GLES3 || SHADER_API_METAL || SHADER_API_VULKAN )
				#define CAN_SKIP_VPOS
			#endif
			#include "UnityCG.cginc"
			#include "Lighting.cginc"
			#include "UnityPBSLighting.cginc"
			struct v2f
			{
				V2F_SHADOW_CASTER;
				float3 customPack1 : TEXCOORD1;
				float4 tSpace0 : TEXCOORD2;
				float4 tSpace1 : TEXCOORD3;
				float4 tSpace2 : TEXCOORD4;
				UNITY_VERTEX_INPUT_INSTANCE_ID
				UNITY_VERTEX_OUTPUT_STEREO
			};
			v2f vert( appdata_full v )
			{
				v2f o;
				UNITY_SETUP_INSTANCE_ID( v );
				UNITY_INITIALIZE_OUTPUT( v2f, o );
				UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO( o );
				UNITY_TRANSFER_INSTANCE_ID( v, o );
				Input customInputData;
				vertexDataFunc( v, customInputData );
				float3 worldPos = mul( unity_ObjectToWorld, v.vertex ).xyz;
				half3 worldNormal = UnityObjectToWorldNormal( v.normal );
				half3 worldTangent = UnityObjectToWorldDir( v.tangent.xyz );
				half tangentSign = v.tangent.w * unity_WorldTransformParams.w;
				half3 worldBinormal = cross( worldNormal, worldTangent ) * tangentSign;
				o.tSpace0 = float4( worldTangent.x, worldBinormal.x, worldNormal.x, worldPos.x );
				o.tSpace1 = float4( worldTangent.y, worldBinormal.y, worldNormal.y, worldPos.y );
				o.tSpace2 = float4( worldTangent.z, worldBinormal.z, worldNormal.z, worldPos.z );
				o.customPack1.xy = customInputData.uv_texcoord;
				o.customPack1.xy = v.texcoord;
				o.customPack1.z = customInputData.eyeDepth;
				TRANSFER_SHADOW_CASTER_NORMALOFFSET( o )
				return o;
			}
			half4 frag( v2f IN
			#if !defined( CAN_SKIP_VPOS )
			, UNITY_VPOS_TYPE vpos : VPOS
			#endif
			) : SV_Target
			{
				UNITY_SETUP_INSTANCE_ID( IN );
				Input surfIN;
				UNITY_INITIALIZE_OUTPUT( Input, surfIN );
				surfIN.uv_texcoord = IN.customPack1.xy;
				surfIN.eyeDepth = IN.customPack1.z;
				float3 worldPos = float3( IN.tSpace0.w, IN.tSpace1.w, IN.tSpace2.w );
				half3 worldViewDir = normalize( UnityWorldSpaceViewDir( worldPos ) );
				surfIN.worldPos = worldPos;
				surfIN.worldNormal = float3( IN.tSpace0.z, IN.tSpace1.z, IN.tSpace2.z );
				surfIN.internalSurfaceTtoW0 = IN.tSpace0.xyz;
				surfIN.internalSurfaceTtoW1 = IN.tSpace1.xyz;
				surfIN.internalSurfaceTtoW2 = IN.tSpace2.xyz;
				SurfaceOutputStandard o;
				UNITY_INITIALIZE_OUTPUT( SurfaceOutputStandard, o )
				surf( surfIN, o );
				#if defined( CAN_SKIP_VPOS )
				float2 vpos = IN.pos;
				#endif
				SHADOW_CASTER_FRAGMENT( IN )
			}
			ENDCG
		}
	}
	Fallback "SandyTop_Opt"
	CustomEditor "ASEMaterialInspector"
}
/*ASEBEGIN
Version=18800
6.666667;6;2560;1373;-170.2765;-292.4186;1;True;True
Node;AmplifyShaderEditor.CommentaryNode;433;-6948.612,-2308.808;Inherit;False;4215.075;1287.307;Comment;26;362;379;369;329;380;377;378;368;429;431;24;20;253;430;383;264;311;252;287;310;384;294;309;265;96;254;Sand Height Blend;1,1,1,1;0;0
Node;AmplifyShaderEditor.WorldPosInputsNode;362;-6898.612,-1361.469;Inherit;False;0;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.DynamicAppendNode;369;-6549.379,-1548.199;Inherit;False;FLOAT2;4;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;3;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RangedFloatNode;329;-6742.615,-1747.97;Inherit;False;Property;_HeightTiling;Sand Noise Tiling;31;0;Create;False;0;0;0;False;0;False;0.5;0.245;0;0.5;0;1;FLOAT;0
Node;AmplifyShaderEditor.DynamicAppendNode;379;-6530.66,-1397.324;Inherit;False;FLOAT2;4;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;3;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.DynamicAppendNode;380;-6548.66,-1202.324;Inherit;False;FLOAT2;4;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;3;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;368;-6284.086,-1650.437;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.Vector2Node;394;-2000.012,-120.8808;Inherit;False;Property;_RockDetailNormalOffset;Detail Normal Offset;19;0;Create;False;0;0;0;False;0;False;0,0;0,0;0;3;FLOAT2;0;FLOAT;1;FLOAT;2
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;377;-6261.66,-1443.324;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RangedFloatNode;336;-1980.34,-640.0621;Inherit;False;Property;_RockTiling;Main Tiling;12;0;Create;False;0;0;0;False;0;False;1;10;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;340;-2033.807,-219.666;Inherit;False;Property;_RockDetailNormalTiling;Detail Normal Tiling;17;0;Create;False;0;0;0;False;0;False;1;1;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.Vector2Node;395;-2000.776,-533.5065;Inherit;False;Property;_RockOffset;Main Offset;14;0;Create;False;0;0;0;False;0;False;0,0;0,0;0;3;FLOAT2;0;FLOAT;1;FLOAT;2
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;378;-6241.66,-1212.324;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RangedFloatNode;24;-5308.753,-1932.136;Half;False;Property;_SandFalloff;Sand Main Opacity;28;0;Create;False;0;0;0;False;0;False;7;6.13;0;10;0;1;FLOAT;0
Node;AmplifyShaderEditor.TextureCoordinatesNode;339;-1688.806,-218.6661;Inherit;False;0;-1;2;3;2;SAMPLER2D;;False;0;FLOAT2;1,1;False;1;FLOAT2;0,0;False;5;FLOAT2;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.WorldNormalVector;20;-5253.243,-2258.808;Inherit;True;False;1;0;FLOAT3;0,0,0;False;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.RangedFloatNode;404;-1847.419,-360.9127;Inherit;False;Property;_RockRotation;Main Rotation;13;0;Create;False;0;0;0;False;0;False;0;0;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;253;-5286.856,-1821.026;Half;False;Property;_SandCoverage;Sand Vertical Distance;29;0;Create;False;0;0;0;False;0;False;2;0.3;-10;10;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;401;-1721.842,-47.44635;Inherit;False;Property;_RockDetailNormalRotation;Detail Normal Rotation;18;0;Create;False;0;0;0;False;0;False;0;0;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.TextureCoordinatesNode;335;-1772.633,-566.0282;Inherit;False;0;-1;2;3;2;SAMPLER2D;;False;0;FLOAT2;1,1;False;1;FLOAT2;0,0;False;5;FLOAT2;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SamplerNode;430;-6011.416,-1475.691;Inherit;True;Property;_TextureSample0;Texture Sample 0;34;0;Create;True;0;0;0;False;0;False;-1;None;None;True;0;False;white;Auto;False;Instance;422;Auto;Texture2D;8;0;SAMPLER2D;;False;1;FLOAT2;0,0;False;2;FLOAT;0;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SamplerNode;431;-6008.416,-1253.691;Inherit;True;Property;_TextureSample1;Texture Sample 1;34;0;Create;True;0;0;0;False;0;False;-1;None;None;True;0;False;white;Auto;False;Instance;422;Auto;Texture2D;8;0;SAMPLER2D;;False;1;FLOAT2;0,0;False;2;FLOAT;0;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SamplerNode;429;-6023.877,-1691.588;Inherit;True;Property;_TextureSample4;Texture Sample 4;34;0;Create;True;0;0;0;False;0;False;-1;None;None;True;0;False;white;Auto;False;Instance;422;Auto;Texture2D;8;0;SAMPLER2D;;False;1;FLOAT2;0,0;False;2;FLOAT;0;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.ScaleAndOffsetNode;252;-4844.025,-1986.916;Inherit;True;3;0;FLOAT;0;False;1;FLOAT;1;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;264;-4877.705,-1271.972;Inherit;False;Constant;_HeightBlend;Height Blend;15;0;Create;True;0;0;0;False;0;False;10;10;0;10;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;311;-4408.514,-1137.501;Inherit;False;Property;_HeightFalloff;Sand Noise Opacity Blur;32;0;Create;False;0;0;0;False;0;False;1;0.78;0;1;0;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;383;-5236.416,-1510.57;Inherit;True;3;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RotatorNode;402;-1449.842,-203.4464;Inherit;False;3;0;FLOAT2;0,0;False;1;FLOAT2;1,1;False;2;FLOAT;1;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RotatorNode;403;-1485.419,-400.9127;Inherit;False;3;0;FLOAT2;0,0;False;1;FLOAT2;1,1;False;2;FLOAT;1;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;343;-1244.106,-154.1661;Inherit;False;RockDetailTiling;-1;True;1;0;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.OneMinusNode;310;-4532.992,-1475.561;Inherit;False;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;434;-1300.619,-34.3177;Inherit;False;Property;_DetailNormalIntensity;Detail Normal Intensity;16;0;Create;True;0;0;0;False;0;False;1;0.75;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;405;-1236.293,-269.4054;Inherit;False;Property;_RockNormalIntensity;Main Normal Intensity;11;0;Create;False;0;0;0;False;0;False;1;1;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;342;-1274.8,-372.2305;Inherit;False;RockTiling;-1;True;1;0;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;287;-4545.932,-1711.029;Inherit;True;2;2;0;FLOAT;0;False;1;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.OneMinusNode;384;-4128.458,-1216.165;Inherit;False;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.TFHCRemapNode;309;-4231.646,-1637.684;Inherit;True;5;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;1;False;3;FLOAT;0;False;4;FLOAT;1;False;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;4;-965.3806,-379.7589;Inherit;True;Property;_RockNormal;Main Normal;9;1;[NoScaleOffset];Create;False;0;0;0;False;0;False;-1;None;4d08f2df0f563ff48ac176208eb7fbca;True;0;True;bump;Auto;True;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;2;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.WorldPosInputsNode;357;-2329.429,241.1959;Inherit;True;0;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.SamplerNode;247;-952.3076,-174.4019;Inherit;True;Property;_RockDetailNormal;Detail Normal;15;1;[NoScaleOffset];Create;False;0;0;0;False;0;False;-1;None;97a88bb9a705ed84c91f3405dd2c56b1;True;0;True;bump;Auto;True;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.ToggleSwitchNode;294;-4004.933,-1393.029;Inherit;False;Property;_UseHeightBlending;Use Noise For Sand Opacity;30;0;Create;False;0;0;0;False;0;False;1;2;0;FLOAT;0;False;1;FLOAT;1;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;334;-1873.897,619.612;Inherit;False;Property;_SandBTiling;Sand B Tiling;27;0;Create;True;0;0;0;False;0;False;0.5;0.1;0;0.5;0;1;FLOAT;0
Node;AmplifyShaderEditor.Vector2Node;427;-912.7841,687.4364;Inherit;False;Property;_SandNoiseBlendOffset;Sand A/B Blend Offset;33;0;Create;False;0;0;0;False;0;False;0,0;0,0;0;3;FLOAT2;0;FLOAT;1;FLOAT;2
Node;AmplifyShaderEditor.BlendNormalsNode;248;-271.5685,-149.295;Inherit;False;0;3;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT3;0,0,0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.DynamicAppendNode;370;-1848.11,259.8158;Inherit;False;FLOAT2;4;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;3;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.DynamicAppendNode;393;-1845.835,392.9863;Inherit;False;FLOAT2;4;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;3;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.CommentaryNode;450;601.5503,664.6876;Inherit;False;2014.154;852.3796;Fresnel;15;441;448;440;446;449;438;439;436;444;437;435;445;451;453;454;FRESNEL EFFECT;1,1,1,1;0;0
Node;AmplifyShaderEditor.RangedFloatNode;426;-935.0364,568.321;Inherit;False;Property;_SandNoiseBlendTiling;Sand A/B Blend Tiling;34;0;Create;False;0;0;0;False;0;False;1;0.5;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.LerpOp;265;-3595.039,-1592.56;Inherit;True;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;331;-1898.225,67.69201;Inherit;False;Property;_SandATiling;Sand A Tiling;23;0;Create;True;0;0;0;False;0;False;0.5;0.1;0;0.5;0;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;360;-1514.47,405.9065;Inherit;False;2;2;0;FLOAT2;0,0;False;1;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RangedFloatNode;408;-645.913,-1572.692;Inherit;False;Property;_DiscolorScale1;Discolor Scale;4;0;Create;False;0;0;0;False;0;False;0.5423828;0.6;0;1;0;1;FLOAT;0
Node;AmplifyShaderEditor.TextureCoordinatesNode;425;-662.7721,565.7031;Inherit;False;0;-1;2;3;2;SAMPLER2D;;False;0;FLOAT2;1,1;False;1;FLOAT2;0,0;False;5;FLOAT2;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.RangedFloatNode;445;707.1892,1339.545;Inherit;False;Property;_F_Distance;F_Distance;39;0;Create;True;0;0;0;False;0;False;256;256;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;452;101.703,-154.1792;Inherit;False;BaseNormals;-1;True;1;0;FLOAT3;0,0,0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.SaturateNode;96;-3208.416,-1590.404;Inherit;True;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;361;-1523.899,79.76813;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RangedFloatNode;436;817.2053,1099.104;Inherit;False;Property;_F_Power;F_Power;38;0;Create;True;0;0;0;False;0;False;6;6;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.CameraDepthFade;444;949.2276,1232.918;Inherit;False;3;2;FLOAT3;0,0,0;False;0;FLOAT;1;False;1;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;338;-1282.91,61.06499;Inherit;False;SandATiling_A;-1;True;1;0;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;254;-2957.537,-1584.419;Inherit;False;sandSettings;-1;True;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;437;810.2053,978.1038;Inherit;False;Property;_F_Scale;F_Scale;37;0;Create;True;0;0;0;False;0;False;2.5;3.96;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.Vector2Node;406;-391.1418,-2027.584;Inherit;False;Constant;_Vector1;Vector 1;12;0;Create;True;0;0;0;False;0;False;0.1,0.1;0,0;0;3;FLOAT2;0;FLOAT;1;FLOAT;2
Node;AmplifyShaderEditor.SamplerNode;424;-426.096,465.7913;Inherit;True;Property;_TextureSample3;Texture Sample 3;34;0;Create;True;0;0;0;False;0;False;-1;None;None;True;0;False;white;Auto;False;Instance;422;Auto;Texture2D;8;0;SAMPLER2D;;False;1;FLOAT2;0,0;False;2;FLOAT;0;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.GetLocalVarNode;453;696.0491,730.7643;Inherit;False;452;BaseNormals;1;0;OBJECT;;False;1;FLOAT3;0
Node;AmplifyShaderEditor.RangedFloatNode;435;761.2813,865.8533;Inherit;False;Property;_F_Bias;F_Bias;36;0;Create;True;0;0;0;False;0;False;0;0;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.LerpOp;407;-348.0399,-1715.336;Inherit;False;3;0;FLOAT;0.5;False;1;FLOAT;0.0005;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;341;-1272.374,337.6406;Inherit;False;SandBTiling_A;-1;True;1;0;FLOAT2;0,0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.GetLocalVarNode;345;-454.8459,-861.5452;Inherit;False;338;SandATiling_A;1;0;OBJECT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.ClampOpNode;449;1248.339,1169.703;Inherit;False;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;1;False;1;FLOAT;0
Node;AmplifyShaderEditor.FresnelNode;438;1029.488,923.7086;Inherit;False;Standard;TangentNormal;ViewDir;False;False;5;0;FLOAT3;0,0,1;False;4;FLOAT3;0,0,0;False;1;FLOAT;0;False;2;FLOAT;1;False;3;FLOAT;5;False;1;FLOAT;0
Node;AmplifyShaderEditor.GetLocalVarNode;454;1239.216,1008.8;Inherit;False;254;sandSettings;1;0;OBJECT;;False;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;409;-79.81081,-1813.445;Inherit;False;2;2;0;FLOAT2;0,0;False;1;FLOAT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.GetLocalVarNode;346;-464.8459,-631.5452;Inherit;False;341;SandBTiling_A;1;0;OBJECT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.TexturePropertyNode;421;-560.5229,-2456.302;Inherit;True;Property;_NoiseMap;Noise Map;2;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;340475781ce7f804a913adbde5f5d4cc;340475781ce7f804a913adbde5f5d4cc;False;white;Auto;Texture2D;-1;0;2;SAMPLER2D;0;SAMPLERSTATE;1
Node;AmplifyShaderEditor.GetLocalVarNode;344;-498.8459,-1091.545;Inherit;False;342;RockTiling;1;0;OBJECT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;432;-111.1154,502.6921;Inherit;False;noiseGen;-1;True;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.Vector3Node;439;1268.224,714.6874;Inherit;False;Constant;_Vector0;Vector 0;39;0;Create;True;0;0;0;False;0;False;0,0,0;0,0,0;0;4;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3
Node;AmplifyShaderEditor.TriplanarNode;410;66.03321,-1829.427;Inherit;True;Spherical;World;False;Discoloration;_Discoloration;white;2;None;Mid Texture 2;_MidTexture2;white;-1;None;Bot Texture 2;_BotTexture2;white;-1;None;Triplanar Sampler;Tangent;10;0;SAMPLER2D;;False;5;FLOAT;1;False;1;SAMPLER2D;;False;6;FLOAT;0;False;2;SAMPLER2D;;False;7;FLOAT;0;False;9;FLOAT3;0,0,0;False;8;FLOAT;1;False;3;FLOAT2;1,1;False;4;FLOAT;1;False;5;FLOAT4;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.LerpOp;440;1473.073,919.398;Inherit;False;3;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT;0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.OneMinusNode;446;1468.847,1150.206;Inherit;True;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.GetLocalVarNode;52;-13.21389,-332.7122;Inherit;False;432;noiseGen;1;0;OBJECT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;1;-200.6146,-1101.435;Inherit;True;Property;_RockAlbedo;Main Albedo;8;1;[NoScaleOffset];Create;False;0;0;0;False;0;False;-1;None;cc168f8fce39f8b4cae4214385487daf;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.ColorNode;350;-145.7357,-1349.867;Inherit;False;Property;_AlbedoTint;Albedo Tint;7;0;Create;True;0;0;0;False;0;False;1,1,1,0;1,1,1,0;True;0;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.RangedFloatNode;411;318.7731,-1508.514;Inherit;False;Property;_DiscolorationContrast;Discoloration Contrast;5;0;Create;True;0;0;0;False;0;False;0.5;0.4;0;2;0;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;9;-198.8298,-889.1171;Inherit;True;Property;_SandAlbedoA;Sand Albedo A;20;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;373ffbb035cfad44684b869f90421f7d;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SamplerNode;36;-188.0774,-668.9915;Inherit;True;Property;_SandAlbedoB;Sand Albedo B;24;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;a41c697e2efb30b4da9dceeed6754b12;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;448;1691.658,970.7871;Inherit;False;2;2;0;FLOAT3;0,0,0;False;1;FLOAT;0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.LerpOp;37;270.4825,-458.6638;Inherit;False;3;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;2;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.GetLocalVarNode;255;443.3558,-189.1497;Inherit;False;254;sandSettings;1;0;OBJECT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;413;636.7729,-1508.514;Inherit;False;Property;_DiscolorationIntensity;Discoloration Intensity;6;0;Create;True;0;0;0;False;0;False;1.494118;3;0;3;0;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;351;221.9795,-1226.258;Inherit;True;2;2;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleContrastOpNode;412;591.7729,-1627.514;Inherit;False;2;1;COLOR;0,0,0,0;False;0;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.SamplerNode;14;-938.6995,39.87342;Inherit;True;Property;_SandNormalA;Sand Normal A;21;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;216b6fd9b2d3f07498a470564b76c7db;True;0;True;bump;Auto;True;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.StaticSwitch;441;1947.885,931.0444;Inherit;False;Property;_UseFresnel;Use Fresnel;35;0;Create;True;0;0;0;False;0;False;0;0;1;True;;Toggle;2;Key0;Key1;Create;True;True;9;1;FLOAT3;0,0,0;False;0;FLOAT3;0,0,0;False;2;FLOAT3;0,0,0;False;3;FLOAT3;0,0,0;False;4;FLOAT3;0,0,0;False;5;FLOAT3;0,0,0;False;6;FLOAT3;0,0,0;False;7;FLOAT3;0,0,0;False;8;FLOAT3;0,0,0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.SamplerNode;34;-927.4965,292.0663;Inherit;True;Property;_SandNormalB;Sand Normal B;25;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;40ae2bab02204d249ba12fc12a531f3a;True;0;True;bump;Auto;True;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;FLOAT3;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.LerpOp;10;779.7692,-277.2395;Inherit;True;3;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;2;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;414;996.173,-1554.814;Inherit;False;2;2;0;COLOR;0,0,0,0;False;1;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;451;2287.144,929.4335;Inherit;False;fresnel;-1;True;1;0;FLOAT3;0,0,0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.RangedFloatNode;416;1316.618,-451.7326;Inherit;False;Property;_DiscolorationFadet;Discoloration Fadet;3;0;Create;True;0;0;0;False;0;False;1;0.543;0;1;0;1;FLOAT;0
Node;AmplifyShaderEditor.LerpOp;35;-57.60392,277.8254;Inherit;False;3;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT;0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;415;1256.325,-966.361;Inherit;False;2;2;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.LerpOp;417;1545.064,-775.7509;Inherit;False;3;0;COLOR;0,0,0,0;False;1;COLOR;0,0,0,0;False;2;FLOAT;0;False;1;COLOR;0
Node;AmplifyShaderEditor.CommentaryNode;418;-2327.97,1345.834;Inherit;False;2608.409;1412.821;Old Metalness/Smoothness Stuff;17;33;42;31;51;349;348;16;38;347;2;303;39;256;304;302;17;305;Old Metalness/Smoothness;1,1,1,1;0;0
Node;AmplifyShaderEditor.GetLocalVarNode;258;467.9611,222.2855;Inherit;False;254;sandSettings;1;0;OBJECT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.BlendNormalsNode;30;123.939,148.029;Inherit;False;0;3;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT3;0,0,0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.GetLocalVarNode;455;1977.015,-60.2516;Inherit;False;451;fresnel;1;0;OBJECT;;False;1;FLOAT3;0
Node;AmplifyShaderEditor.CommentaryNode;428;89.6899,-2790.928;Inherit;False;370;280;Comment;1;422;Noise Map Sampler for Reference Everywhere Else;1,1,1,1;0;0
Node;AmplifyShaderEditor.RangedFloatNode;33;-2139.246,2615.314;Inherit;False;Constant;_SandNoiseMixScale;Sand Noise Mix Scale;24;0;Create;True;0;0;0;False;0;False;10;10;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.LerpOp;17;98.43832,1843.834;Inherit;False;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;38;-1963.934,1944.938;Inherit;True;Property;_SandBMaskMapMetallicRSmoothnessA;Sand B Mask Map- Metallic(R) Smoothness(A);26;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;561d625eb3eb1984bb48cc58bb3a4438;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SimpleAddOpNode;442;2215.37,-76.70358;Inherit;False;2;2;0;COLOR;0,0,0,0;False;1;FLOAT3;0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.LerpOp;305;-141.5616,1395.834;Inherit;False;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.TextureCoordinatesNode;42;-2118.992,2388.143;Inherit;False;0;-1;2;3;2;SAMPLER2D;;False;0;FLOAT2;1,1;False;1;FLOAT2;0,0;False;5;FLOAT2;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.LerpOp;302;-621.5618,1651.834;Inherit;False;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.GetLocalVarNode;304;-365.5617,1683.834;Inherit;False;254;sandSettings;1;0;OBJECT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;419;1612.651,88.9505;Inherit;False;Property;_GlobalMetalness;Global Metalness;0;0;Create;True;0;0;0;False;0;False;0;0;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RegisterLocalVarNode;51;-1336.064,2371.499;Inherit;False;noiseGenOLD;-1;True;1;0;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.GetLocalVarNode;348;-2261.423,1709.964;Inherit;False;338;SandATiling_A;1;0;OBJECT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.SamplerNode;2;-1966.02,1471.884;Inherit;True;Property;_RockMaskMapMetallicRSmoothnessA;Rock Mask Map- Metallic(R) Smoothness(A);10;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;a84a444f23ec0804ab3c77cd954dd80a;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.LerpOp;15;766.5215,66.17463;Inherit;False;3;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT;0;False;1;FLOAT3;0
Node;AmplifyShaderEditor.LerpOp;39;-749.5618,2243.833;Inherit;False;3;0;FLOAT;0;False;1;FLOAT;0;False;2;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;422;139.6899,-2740.928;Inherit;True;Property;_TextureSample2;Texture Sample 2;34;0;Create;True;0;0;0;False;0;False;-1;None;None;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;;False;1;FLOAT2;0,0;False;2;FLOAT;0;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.GetLocalVarNode;256;-77.56161,2147.833;Inherit;False;254;sandSettings;1;0;OBJECT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.GetLocalVarNode;303;-829.5618,1795.834;Inherit;False;51;noiseGenOLD;1;0;OBJECT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.GetLocalVarNode;349;-2277.97,2024.692;Inherit;False;341;SandBTiling_A;1;0;OBJECT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.GetLocalVarNode;347;-2277.422,1496.965;Inherit;False;342;RockTiling;1;0;OBJECT;0;False;1;FLOAT2;0
Node;AmplifyShaderEditor.SamplerNode;16;-1971.234,1680.814;Inherit;True;Property;_SandAMaskMapMetallicRSmoothnessA;Sand A Mask Map- Metallic(R) Smoothness(A);22;1;[NoScaleOffset];Create;True;0;0;0;False;0;False;-1;None;None;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;0,0;False;1;FLOAT2;0,0;False;2;FLOAT;1;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.NoiseGeneratorNode;31;-1700.38,2499.654;Inherit;True;Simplex3D;True;False;2;0;FLOAT3;0,0,0;False;1;FLOAT;1;False;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;420;1611.651,207.9505;Inherit;False;Property;_GlobalSmoothness;Global Smoothness;1;0;Create;True;0;0;0;False;0;False;0;0.75;0;1;0;1;FLOAT;0
Node;AmplifyShaderEditor.StandardSurfaceOutputNode;0;2418.961,-31.66497;Half;False;True;-1;2;ASEMaterialInspector;0;0;Standard;SandyTop;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;Back;0;False;-1;3;False;-1;False;0;False;-1;0;False;-1;False;0;Opaque;0.5;True;True;0;False;Opaque;;Geometry;All;14;all;True;True;True;True;0;False;-1;False;0;False;-1;255;False;-1;255;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;False;0;4;10;25;False;0.5;True;0;0;False;-1;0;False;-1;0;0;False;-1;0;False;-1;1;False;-1;1;False;-1;0;False;0;0,0,0,0;VertexOffset;True;False;Cylindrical;False;Relative;0;SandyTop_Opt;-1;-1;-1;-1;0;False;0;0;False;-1;-1;0;False;-1;0;0;0;False;0.1;False;-1;0;False;-1;False;16;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT3;0,0,0;False;3;FLOAT;0;False;4;FLOAT;0;False;5;FLOAT;0;False;6;FLOAT3;0,0,0;False;7;FLOAT3;0,0,0;False;8;FLOAT;0;False;9;FLOAT;0;False;10;FLOAT;0;False;13;FLOAT3;0,0,0;False;11;FLOAT3;0,0,0;False;12;FLOAT3;0,0,0;False;14;FLOAT4;0,0,0,0;False;15;FLOAT3;0,0,0;False;0
WireConnection;369;0;362;1
WireConnection;369;1;362;3
WireConnection;379;0;362;1
WireConnection;379;1;362;2
WireConnection;380;0;362;2
WireConnection;380;1;362;3
WireConnection;368;0;329;0
WireConnection;368;1;369;0
WireConnection;377;0;329;0
WireConnection;377;1;379;0
WireConnection;378;0;329;0
WireConnection;378;1;380;0
WireConnection;339;0;340;0
WireConnection;339;1;394;0
WireConnection;335;0;336;0
WireConnection;335;1;395;0
WireConnection;430;1;377;0
WireConnection;431;1;378;0
WireConnection;429;1;368;0
WireConnection;252;0;20;2
WireConnection;252;1;24;0
WireConnection;252;2;253;0
WireConnection;383;0;429;2
WireConnection;383;1;430;2
WireConnection;383;2;431;2
WireConnection;402;0;339;0
WireConnection;402;2;401;0
WireConnection;403;0;335;0
WireConnection;403;2;404;0
WireConnection;343;0;402;0
WireConnection;310;0;264;0
WireConnection;342;0;403;0
WireConnection;287;0;252;0
WireConnection;287;1;383;0
WireConnection;384;0;311;0
WireConnection;309;0;287;0
WireConnection;309;3;310;0
WireConnection;309;4;264;0
WireConnection;4;1;342;0
WireConnection;4;5;405;0
WireConnection;247;1;343;0
WireConnection;247;5;434;0
WireConnection;294;1;384;0
WireConnection;248;0;4;0
WireConnection;248;1;247;0
WireConnection;370;0;357;1
WireConnection;370;1;357;3
WireConnection;393;0;357;1
WireConnection;393;1;357;3
WireConnection;265;0;252;0
WireConnection;265;1;309;0
WireConnection;265;2;294;0
WireConnection;360;0;393;0
WireConnection;360;1;334;0
WireConnection;425;0;426;0
WireConnection;425;1;427;0
WireConnection;452;0;248;0
WireConnection;96;0;265;0
WireConnection;361;0;331;0
WireConnection;361;1;370;0
WireConnection;444;0;445;0
WireConnection;338;0;361;0
WireConnection;254;0;96;0
WireConnection;424;1;425;0
WireConnection;407;2;408;0
WireConnection;341;0;360;0
WireConnection;449;0;444;0
WireConnection;438;0;453;0
WireConnection;438;1;435;0
WireConnection;438;2;437;0
WireConnection;438;3;436;0
WireConnection;409;0;406;0
WireConnection;409;1;407;0
WireConnection;432;0;424;1
WireConnection;410;0;421;0
WireConnection;410;3;409;0
WireConnection;440;0;438;0
WireConnection;440;1;439;0
WireConnection;440;2;454;0
WireConnection;446;0;449;0
WireConnection;1;1;344;0
WireConnection;9;1;345;0
WireConnection;36;1;346;0
WireConnection;448;0;440;0
WireConnection;448;1;446;0
WireConnection;37;0;9;0
WireConnection;37;1;36;0
WireConnection;37;2;52;0
WireConnection;351;0;350;0
WireConnection;351;1;1;0
WireConnection;412;1;410;0
WireConnection;412;0;411;0
WireConnection;14;1;338;0
WireConnection;441;1;439;0
WireConnection;441;0;448;0
WireConnection;34;1;341;0
WireConnection;10;0;351;0
WireConnection;10;1;37;0
WireConnection;10;2;255;0
WireConnection;414;0;412;0
WireConnection;414;1;413;0
WireConnection;451;0;441;0
WireConnection;35;0;14;0
WireConnection;35;1;34;0
WireConnection;35;2;432;0
WireConnection;415;0;414;0
WireConnection;415;1;10;0
WireConnection;417;0;10;0
WireConnection;417;1;415;0
WireConnection;417;2;416;0
WireConnection;30;0;248;0
WireConnection;30;1;35;0
WireConnection;17;0;2;4
WireConnection;17;1;39;0
WireConnection;17;2;256;0
WireConnection;38;1;349;0
WireConnection;442;0;417;0
WireConnection;442;1;455;0
WireConnection;305;0;2;1
WireConnection;305;1;302;0
WireConnection;305;2;304;0
WireConnection;302;0;16;1
WireConnection;302;1;38;1
WireConnection;302;2;303;0
WireConnection;51;0;31;0
WireConnection;2;1;347;0
WireConnection;15;0;452;0
WireConnection;15;1;30;0
WireConnection;15;2;258;0
WireConnection;39;0;16;4
WireConnection;39;1;38;4
WireConnection;422;0;421;0
WireConnection;16;1;348;0
WireConnection;31;0;42;0
WireConnection;31;1;33;0
WireConnection;0;0;442;0
WireConnection;0;1;15;0
WireConnection;0;3;419;0
WireConnection;0;4;420;0
ASEEND*/
//CHKSM=58E1B6B2219B824509DE17F52F6D93E475C0A0AC