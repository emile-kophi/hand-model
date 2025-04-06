
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Custom;  // import name space

public class HandLandmarksSubscriber : MonoBehaviour
{
    public GameObject landmarkPrefab;  // creat  Prefab for landmarks
    private List<GameObject> landmarkSpheres = new List<GameObject>();  // list  for landmarks, evrey single landmark will be sostituite by sphere

    void Start()
    {
        // subscription for ROS topic
        ROSConnection.GetOrCreateInstance().Subscribe<All_landmarksMsg>("hand_landmarks", UpdateHand);
        
        // create sphere on the scene
        for (int i = 0; i < 21; i++)
        {
            GameObject sphere = Instantiate(landmarkPrefab);
            landmarkSpheres.Add(sphere);
        }
    }

    void UpdateHand(All_landmarksMsg msg)
    {
        // uodate the position for all sphere
        for (int i = 0; i < msg.landmarks.Length && i < landmarkSpheres.Count; i++)
        {
            Vector3 pos = new Vector3(
                (float)msg.landmarks[i].x,
                -(float)msg.landmarks[i].y,
                (float)msg.landmarks[i].z
            );

            landmarkSpheres[i].transform.position = pos;
            Debug.Log($"Landmark {i}: x={msg.landmarks[i].x}, y={msg.landmarks[i].y}, z={msg.landmarks[i].z}");
        }
        

     
    }
}
