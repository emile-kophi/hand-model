using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Custom;

public class HandLandmarksSubscriber2 : MonoBehaviour
{
    public GameObject landmarkPrefab;
    public float scaleFactor = 5.0f;
    public float sphereSize = 0.05f;
    public float lineWidth = 0.02f;

    public bool createGrids = true;
    public float gridSize = 3.0f;
    public float gridSpacing = 0.25f;

    public bool centerCameraOnGrid = true;

    private List<GameObject> landmarkSpheres = new List<GameObject>();
    private List<LineRenderer> fingerLines = new List<LineRenderer>();
    private Material[] fingerMaterials;
    private Vector3? initialWristRaw = null;

    private readonly int[][] fingerIndices = new int[][]
    {
        new int[] {0, 1, 2, 3, 4},      // Pollice
        new int[] {0, 5, 6, 7, 8},      // Indice
        new int[] {0, 9, 10, 11, 12},   // Medio
        new int[] {0, 13, 14, 15, 16},  // Anulare
        new int[] {0, 17, 18, 19, 20}   // Mignolo
    };

    void Start()
    {
        ROSConnection.GetOrCreateInstance().Subscribe<All_landmarksMsg>("hand_landmarks", UpdateHand);

        // Colori per le dita
        Color[] fingerColors = new Color[]
        {
            Color.red,
            Color.green,
            Color.blue,
            new Color(1f, 0.5f, 0f),  // arancione
            Color.magenta
        };

        // Crea materiali per le dita
        fingerMaterials = new Material[5];
        for (int i = 0; i < fingerColors.Length; i++)
        {
            Material mat = new Material(Shader.Find("Unlit/Color"));
            mat.color = fingerColors[i];
            fingerMaterials[i] = mat;
        }

        // Crea sfere per landmark
        for (int i = 0; i < 21; i++)
        {
            GameObject sphere = Instantiate(landmarkPrefab);
            sphere.transform.localScale = Vector3.one * sphereSize;

            int fingerIndex = GetFingerIndex(i);
            if (fingerIndex != -1)
                sphere.GetComponent<Renderer>().material = fingerMaterials[fingerIndex];

            landmarkSpheres.Add(sphere);
        }

        // Crea linee per ogni dito
        for (int i = 0; i < 5; i++)
        {
            GameObject lineObj = new GameObject("FingerLine_" + i);
            LineRenderer lr = lineObj.AddComponent<LineRenderer>();
            lr.positionCount = fingerIndices[i].Length;
            lr.startWidth = lineWidth;
            lr.endWidth = lineWidth;
            lr.material = fingerMaterials[i];
            lr.useWorldSpace = true;
            fingerLines.Add(lr);
        }

        // Griglia e camera
        if (createGrids)
        {
            CreateGridPlane(Vector3.zero, Vector3.right, Vector3.forward); // XY
            CreateGridPlane(Vector3.zero, Vector3.right, Vector3.up);      // XZ
            CreateGridPlane(Vector3.zero, Vector3.forward, Vector3.up);    // YZ
        }

        if (centerCameraOnGrid)
        {
            SetupCamera(Vector3.zero);
        }
    }

    void UpdateHand(All_landmarksMsg msg)
    {
        if (msg.landmarks.Length < 21) return;

        // Posizione polso attuale
        Vector3 currentWristRaw = new Vector3(
            (float)msg.landmarks[0].x,
            -(float)msg.landmarks[0].y,
            (float)msg.landmarks[0].z
        );

        // Salva offset iniziale solo al primo frame
        if (initialWristRaw == null)
            initialWristRaw = currentWristRaw;

        Vector3 offset = (Vector3)initialWristRaw;

        // Posizionamento sfere
        for (int i = 0; i < msg.landmarks.Length && i < landmarkSpheres.Count; i++)
        {
            Vector3 rawPos = new Vector3(
                (float)msg.landmarks[i].x,
                -(float)msg.landmarks[i].y,
                (float)msg.landmarks[i].z
            );

            Vector3 centered = (rawPos - offset) * scaleFactor;
            landmarkSpheres[i].transform.position = centered;
        }

        // Posizionamento linee dita
        for (int i = 0; i < fingerIndices.Length; i++)
        {
            for (int j = 0; j < fingerIndices[i].Length; j++)
            {
                int index = fingerIndices[i][j];
                fingerLines[i].SetPosition(j, landmarkSpheres[index].transform.position);
            }
        }
    }

    int GetFingerIndex(int landmarkIndex)
    {
        for (int i = 0; i < fingerIndices.Length; i++)
        {
            if (System.Array.Exists(fingerIndices[i], elem => elem == landmarkIndex))
                return i;
        }
        return -1;
    }

    void CreateGridPlane(Vector3 center, Vector3 axis1, Vector3 axis2)
    {
        GameObject gridParent = new GameObject("GridPlane");

        Material lineMaterial = new Material(Shader.Find("Unlit/Color"));
        lineMaterial.color = Color.white;

        int lines = Mathf.RoundToInt(gridSize / gridSpacing);

        for (int i = -lines; i <= lines; i++)
        {
            Vector3 start1 = center + axis1 * -gridSize + axis2 * i * gridSpacing;
            Vector3 end1 = center + axis1 * gridSize + axis2 * i * gridSpacing;
            CreateGridLine(start1, end1, lineMaterial, gridParent.transform);

            Vector3 start2 = center + axis2 * -gridSize + axis1 * i * gridSpacing;
            Vector3 end2 = center + axis2 * gridSize + axis1 * i * gridSpacing;
            CreateGridLine(start2, end2, lineMaterial, gridParent.transform);
        }
    }

    void CreateGridLine(Vector3 start, Vector3 end, Material mat, Transform parent)
    {
        GameObject lineObj = new GameObject("GridLine");
        lineObj.transform.parent = parent;

        LineRenderer lr = lineObj.AddComponent<LineRenderer>();
        lr.material = mat;
        lr.widthMultiplier = 0.005f;
        lr.positionCount = 2;
        lr.SetPosition(0, start);
        lr.SetPosition(1, end);
        lr.useWorldSpace = true;
    }

    void SetupCamera(Vector3 focusPoint)
    {
        Camera cam = Camera.main;
        if (cam == null)
        {
            GameObject camObj = new GameObject("Main Camera");
            cam = camObj.AddComponent<Camera>();
            cam.tag = "MainCamera";
        }

        cam.clearFlags = CameraClearFlags.SolidColor;
        cam.backgroundColor = new Color(0.36f, 0.25f, 0.20f);

        cam.transform.position = focusPoint + new Vector3(0, 1, -4);
        cam.transform.LookAt(focusPoint + Vector3.up * 0.5f);
    }
}
