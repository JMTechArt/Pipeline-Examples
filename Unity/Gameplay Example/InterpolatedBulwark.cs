using System.Collections;
using System.Collections.Generic;
using Ez.Pooly;
using UnityEngine;
using Simutronics.Network.Core;
using System;
using Simutronics.Network.Unsafe;
using simutronics.galahad.lance;

namespace Simutronics.Game.Cyberplayground
{
	
	public class InterpolatedBulwark : InterpolatedGameObject
	{
		
		public LineRenderer[] lineRenderers;
		public GameObject lineRendererEnabler;
		public int lineCurvePositionCount = 200;

		[Range(0f,0.05f)]
		public float helixOffset = 0.015f;
		public float helixAngle = 50f;
		public float speed = 5f;

		private void DrawBeam(int lrIndex, Vector3 startingPoint, Vector3 targetPoint)
    	{
			lineRenderers[lrIndex].positionCount = lineCurvePositionCount;
			float proximityOffset = 0f;
			float lineLength = 0f;
			float distance = Vector3.Distance(startingPoint, targetPoint);
			Vector3 transformVector = startingPoint;
			
			
			for (int i = 0; i < lineRenderers[lrIndex].positionCount; i++)
			{   
				float angle = i * (2 * Mathf.PI / helixAngle);
				float sine = Mathf.Sin(angle) * proximityOffset;
				float cosine = Mathf.Cos(angle) * proximityOffset;

				lineRenderers[lrIndex].transform.parent.LookAt(targetPoint);
				lineRenderers[lrIndex].transform.Rotate(0,0,speed*Time.deltaTime);
				
				transformVector = lineRenderers[lrIndex].transform.localPosition;    
				transformVector = new Vector3(transformVector.x + sine, transformVector.y + cosine, transformVector.z + lineLength);
		
				lineRenderers[lrIndex].SetPosition(i, transformVector);

				lineLength += (distance / (float)lineRenderers[lrIndex].positionCount);

				if (i < lineRenderers[lrIndex].positionCount/2)
				{
					proximityOffset += helixOffset;
				}
				else
				{
					proximityOffset -= helixOffset;
				}   
			}
		}

		
	}
}
