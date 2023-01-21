// Made with Amplify Shader Editor
// Available at the Unity Asset Store - http://u3d.as/y3X 
Shader "HologramFlipbook"
{
	Properties
	{
		_Cutoff( "Mask Clip Value", Float ) = 0.5
		[HDR][NoScaleOffset]_SignSprites("Sign Sprites", 2D) = "white" {}
		_FlipbookColumns("Flipbook Columns", Float) = 0
		_FlipbookRows("Flipbook Rows", Float) = 0
		_FlipbookSpeed("Flipbook Speed", Float) = 0
		_EmissionIntensity("Emission Intensity", Range( 1 , 15)) = 1
		[HideInInspector] _texcoord( "", 2D ) = "white" {}
		[HideInInspector] __dirty( "", Int ) = 1
	}

	SubShader
	{
		Tags{ "RenderType" = "Transparent"  "Queue" = "Geometry+0" "IsEmissive" = "true"  }
		Cull Off
		Blend One One
		
		CGPROGRAM
		#include "UnityShaderVariables.cginc"
		#pragma target 3.0
		#if defined(SHADER_API_D3D11) || defined(SHADER_API_XBOXONE) || defined(UNITY_COMPILER_HLSLCC) || defined(SHADER_API_PSSL) || (defined(SHADER_TARGET_SURFACE_ANALYSIS) && !defined(SHADER_TARGET_SURFACE_ANALYSIS_MOJOSHADER))//ASE Sampler Macros
		#define SAMPLE_TEXTURE2D(tex,samplerTex,coord) tex.Sample(samplerTex,coord)
		#else//ASE Sampling Macros
		#define SAMPLE_TEXTURE2D(tex,samplerTex,coord) tex2D(tex,coord)
		#endif//ASE Sampling Macros

		#pragma surface surf Unlit keepalpha addshadow fullforwardshadows 
		struct Input
		{
			float2 uv_texcoord;
		};

		uniform float _EmissionIntensity;
		UNITY_DECLARE_TEX2D_NOSAMPLER(_SignSprites);
		uniform float _FlipbookColumns;
		uniform float _FlipbookRows;
		uniform float _FlipbookSpeed;
		SamplerState sampler_SignSprites;
		uniform float _Cutoff = 0.5;

		inline half4 LightingUnlit( SurfaceOutput s, half3 lightDir, half atten )
		{
			return half4 ( 0, 0, 0, s.Alpha );
		}

		void surf( Input i , inout SurfaceOutput o )
		{
			float temp_output_4_0_g2 = _FlipbookColumns;
			float temp_output_5_0_g2 = _FlipbookRows;
			float2 appendResult7_g2 = (float2(temp_output_4_0_g2 , temp_output_5_0_g2));
			float totalFrames39_g2 = ( temp_output_4_0_g2 * temp_output_5_0_g2 );
			float2 appendResult8_g2 = (float2(totalFrames39_g2 , temp_output_5_0_g2));
			float clampResult42_g2 = clamp( 0.0 , 0.0001 , ( totalFrames39_g2 - 1.0 ) );
			float temp_output_35_0_g2 = frac( ( ( ( _FlipbookSpeed * _Time.y ) + clampResult42_g2 ) / totalFrames39_g2 ) );
			float2 appendResult29_g2 = (float2(temp_output_35_0_g2 , ( 1.0 - temp_output_35_0_g2 )));
			float2 temp_output_15_0_g2 = ( ( i.uv_texcoord / appendResult7_g2 ) + ( floor( ( appendResult8_g2 * appendResult29_g2 ) ) / appendResult7_g2 ) );
			float4 tex2DNode1 = SAMPLE_TEXTURE2D( _SignSprites, sampler_SignSprites, temp_output_15_0_g2 );
			o.Emission = ( _EmissionIntensity * tex2DNode1 ).rgb;
			o.Alpha = 1;
			clip( tex2DNode1.a - _Cutoff );
		}

		ENDCG
	}
	Fallback "Diffuse"
	CustomEditor "ASEMaterialInspector"
}
/*ASEBEGIN
Version=18400
1110;96;2521;1268;1514.5;678;1;True;False
Node;AmplifyShaderEditor.RangedFloatNode;7;-972,-308.5;Inherit;False;Property;_FlipbookSpeed;Flipbook Speed;4;0;Create;True;0;0;False;0;False;0;10;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.TimeNode;9;-989,-132.5;Inherit;False;0;5;FLOAT4;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.RangedFloatNode;11;-847,-568.5;Inherit;False;Property;_FlipbookColumns;Flipbook Columns;2;0;Create;True;0;0;False;0;False;0;10;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.RangedFloatNode;12;-814,-445.5;Inherit;False;Property;_FlipbookRows;Flipbook Rows;3;0;Create;True;0;0;False;0;False;0;1;0;0;0;1;FLOAT;0
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;10;-758,-207.5;Inherit;False;2;2;0;FLOAT;0;False;1;FLOAT;0;False;1;FLOAT;0
Node;AmplifyShaderEditor.FunctionNode;6;-568,-432.5;Inherit;False;Flipbook;-1;;2;53c2488c220f6564ca6c90721ee16673;2,71,0,68,0;8;51;SAMPLER2D;0.0;False;13;FLOAT2;0,0;False;4;FLOAT;5;False;5;FLOAT;2;False;24;FLOAT;0;False;2;FLOAT;0;False;55;FLOAT;0;False;70;FLOAT;0;False;5;COLOR;53;FLOAT2;0;FLOAT;47;FLOAT;48;FLOAT;62
Node;AmplifyShaderEditor.RangedFloatNode;5;-117,-408.5;Inherit;False;Property;_EmissionIntensity;Emission Intensity;5;0;Create;True;0;0;False;0;False;1;15;1;15;0;1;FLOAT;0
Node;AmplifyShaderEditor.SamplerNode;1;-180,-261.5;Inherit;True;Property;_SignSprites;Sign Sprites;1;2;[HDR];[NoScaleOffset];Create;True;0;0;False;0;False;-1;None;3a63562cd05e32f4a91277f04f0b7cd3;True;0;False;white;Auto;False;Object;-1;Auto;Texture2D;8;0;SAMPLER2D;;False;1;FLOAT2;0,0;False;2;FLOAT;0;False;3;FLOAT2;0,0;False;4;FLOAT2;0,0;False;5;FLOAT;1;False;6;FLOAT;0;False;7;SAMPLERSTATE;;False;5;COLOR;0;FLOAT;1;FLOAT;2;FLOAT;3;FLOAT;4
Node;AmplifyShaderEditor.SimpleMultiplyOpNode;4;157,-335.5;Inherit;False;2;2;0;FLOAT;0;False;1;COLOR;0,0,0,0;False;1;COLOR;0
Node;AmplifyShaderEditor.StandardSurfaceOutputNode;0;358,-279;Float;False;True;-1;2;ASEMaterialInspector;0;0;Unlit;HologramFlipbook;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;False;Off;0;False;-1;0;False;-1;False;0;False;-1;0;False;-1;False;0;Custom;0.5;True;True;0;True;Transparent;;Geometry;All;14;all;True;True;True;True;0;False;-1;False;0;False;-1;255;False;-1;255;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;-1;False;2;15;10;25;False;0.5;True;4;1;False;-1;1;False;-1;0;0;False;-1;0;False;-1;0;False;-1;0;False;-1;0;False;0;0,0,0,0;VertexOffset;True;False;Cylindrical;False;Relative;0;;0;-1;-1;-1;0;False;0;0;False;-1;-1;0;False;-1;0;0;0;False;0.1;False;-1;0;False;-1;True;15;0;FLOAT3;0,0,0;False;1;FLOAT3;0,0,0;False;2;FLOAT3;0,0,0;False;3;FLOAT;0;False;4;FLOAT;0;False;6;FLOAT3;0,0,0;False;7;FLOAT3;0,0,0;False;8;FLOAT;0;False;9;FLOAT;0;False;10;FLOAT;0;False;13;FLOAT3;0,0,0;False;11;FLOAT3;0,0,0;False;12;FLOAT3;0,0,0;False;14;FLOAT4;0,0,0,0;False;15;FLOAT3;0,0,0;False;0
WireConnection;10;0;7;0
WireConnection;10;1;9;2
WireConnection;6;4;11;0
WireConnection;6;5;12;0
WireConnection;6;2;10;0
WireConnection;1;1;6;0
WireConnection;4;0;5;0
WireConnection;4;1;1;0
WireConnection;0;2;4;0
WireConnection;0;10;1;4
ASEEND*/
//CHKSM=788A2F6E6722A309DC61C419870DB29228416354