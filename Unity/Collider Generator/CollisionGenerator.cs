using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using UnityEditorInternal;

public class CollisionGenerator : EditorWindow
{
    private PhysicMaterial      _phys                = null;
    private string              _boxprefix           = "BOX";
    private string              _meshprefix          = "MSH";
    private string              _convexprefix        = "CVX";
    private string[]            _layers              = new string[4] { "None", "Default", "Building","Terrain" };
    int _selected = 0;

    [MenuItem("/Tools/Generate Collision")]

    public static void ShowWindow()
    {
        GetWindow<CollisionGenerator>("Collision Generator");
    }

    private void OnGUI()
    {
        List<GameObject> boxcolliders;
        List<GameObject> convexcolliders;
        List<GameObject> meshcolliders;

        GUILayout.Space(10);
        GUILayout.Label("Generate Collision", EditorStyles.boldLabel);
        GUILayout.Space(10);
        _phys = (PhysicMaterial)EditorGUILayout.ObjectField("Phys Material", _phys, typeof(PhysicMaterial), true);
        _selected = EditorGUILayout.Popup("Object Layer", _selected, _layers);
        GUILayout.Space(10);
        
        GUILayout.Space(10);
        bool showLayerWarning = false;

        if (GUILayout.Button("Generate"))
        {
            if (_phys == null)
            {
                EditorUtility.DisplayDialog("Physics Material Error", "No physics material selected, physics material should not be none.", "Ok");
                return;
            }

            if (Selection.activeGameObject == null)
            {
                Debug.Log("Collision Generator: Nothing Selected.");
                return;
            }
                     
            GameObject obj = Selection.activeGameObject;
            boxcolliders = GetBoxColliders(obj.transform);
            meshcolliders = GetMeshColliders(obj.transform);
            convexcolliders = GetConvexColliders(obj.transform);
           
            for (int i = 0; i < boxcolliders.Count; i++)
            {
                boxcolliders[i].AddComponent<BoxCollider>();
                if(boxcolliders[i].layer == 0)
                {
                    showLayerWarning = true;
                }
            }

            for (int i = 0; i < boxcolliders.Count; i++)
            {
                BoxCollider collider = obj.AddComponent<BoxCollider>();

                ComponentUtility.CopyComponent(boxcolliders[i].GetComponent<BoxCollider>());
                ComponentUtility.PasteComponentValues(collider);
                boxcolliders[i].SetActive(false);

                collider.material = _phys;
            }

            for (int i = 0; i < meshcolliders.Count; i++)
            {
                MeshCollider collider = meshcolliders[i].AddComponent<MeshCollider>();
                collider.material = _phys;
                if (meshcolliders[i].layer == 0)
                {
                    showLayerWarning = true;
                }
            }

            for (int i = 0; i < convexcolliders.Count; i++)
            {
                MeshCollider collider = convexcolliders[i].AddComponent<MeshCollider>();
                collider.convex = true;
                collider.material = _phys;
                if (convexcolliders[i].layer == 0)
                {
                    showLayerWarning = true;
                }
            }

            if(showLayerWarning)
            {
                EditorUtility.DisplayDialog("Object Layer Warning", "One or more objects are in the default layer group, most objects should be in either Terrain or Building layers.", "Ok");
            }
        }
    }
    //These methods check string data set using the Blender Simu-Collider addon for box, mesh, and convex hull shapes only. 
    private List<GameObject> GetBoxColliders(Transform t)
    {
        List<GameObject> colliderObjects = new List<GameObject>();
        foreach (Transform childT in t)
        {
            if (childT.name.StartsWith(_boxprefix))
            {
                colliderObjects.Add(childT.gameObject);
            }

            if (childT.childCount > 0)
            {
                GetBoxColliders(childT);
            }
        }
        return colliderObjects;
    }

    private List<GameObject> GetMeshColliders(Transform t)
    {
        List<GameObject> colliderObjects = new List<GameObject>();
        foreach (Transform childT in t)
        {
            if (childT.name.StartsWith(_meshprefix))
            {
                colliderObjects.Add(childT.gameObject);
                childT.GetComponent<MeshRenderer>().enabled = false;
            }

            if (childT.childCount > 0)
            {
                GetMeshColliders(childT);
            }
        }
        return colliderObjects;
    }

    private List<GameObject> GetConvexColliders(Transform t)
    {
        List<GameObject> colliderObjects = new List<GameObject>();
        foreach (Transform childT in t)
        {
            if (childT.name.StartsWith(_convexprefix))
            {
                colliderObjects.Add(childT.gameObject);
                childT.GetComponent<MeshRenderer>().enabled = false;
            }

            if (childT.childCount > 0)
            {
                GetConvexColliders(childT);
            }
        }
        return colliderObjects;
    }
}

