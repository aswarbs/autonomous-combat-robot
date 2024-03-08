
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
    private float dist;
    private Vector3 aPos;
    private Vector3 bPos;
    public float lineDrawSpeed = 6f;
    public Transform origin;
    public Transform destination;
        
    // Use this for initialization
    void Start()
    {
        lineRenderer = GetComponent<LineRenderer>();
        aPos = new Vector3(origin.position.x, origin.position.y, origin.position.z); // Using these to move the lines back
        bPos = new Vector3(destination.position.x, destination.position.y, destination.position.z);

        lineRenderer.SetPosition(0, aPos);

        dist = Vector3.Distance(origin.position, destination.position);
    }

    // Update is called once per frame
    void Update()
    {

        if (counter < dist)
        {
            counter += .1f / lineDrawSpeed;

            float x = Mathf.Lerp(0, dist, counter);

            Vector3 pointA = aPos;
            Vector3 pointB = bPos;

            Vector3 pointAloneLine = x * Vector3.Normalize(pointB - pointA) + pointA;

            lineRenderer.SetPosition(1, pointAloneLine);
        }

    }
}
