
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;


public class Attack : MonoBehaviour
{
    private LineRenderer lineRenderer;
    private float counter;
    private float dist = 15;
    private Vector3 aPos;
    private Vector3 bPos;
    public float lineDrawSpeed;

    private float time = 2;

    public Color color;
    public Transform origin;
    public Transform destination;

    public KeyCode key;
        
    // Use this for initialization
    void Start()
    {
        lineRenderer = GetComponent<LineRenderer>();
        lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
        lineRenderer.startColor = color;
        lineRenderer.endColor = color;
    }

    void updatePosition()
    {
        lineRenderer.enabled = true;
        aPos = new Vector3(origin.position.x, origin.position.y, origin.position.z); // Using these to move the lines back
        bPos = new Vector3(destination.position.x, destination.position.y, destination.position.z);


        lineRenderer.SetPosition(0, aPos);

    }

    // Update is called once per frame
    void Update()
    {

        if (Input.GetKey(key))
        {
            counter = 0;
            updatePosition();
        }

        if (counter < time)
        {
            counter += 1f / lineDrawSpeed;

            float x = Mathf.Lerp(0, dist, counter);

            Vector3 pointA = aPos;
            Vector3 pointB = bPos;

            Vector3 pointAloneLine = x * Vector3.Normalize(pointB - pointA) + pointA;

            lineRenderer.SetPosition(1, pointAloneLine);
            Debug.LogFormat("counter: {0} dist: {1}", counter, dist);
        }
        else
        {
            Debug.Log("hello");     
            lineRenderer.enabled = false;
        }

        

    }
}
