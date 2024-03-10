
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
    public LineRenderer lineRenderer;
    private float counter = 0;
    private float dist = 15;
    private Vector3 aPos;
    private Vector3 bPos;
    public float lineDrawSpeed;

    public float timeout = 2;

    public Color color;
    public Transform origin;
    public Transform destination;

    public KeyCode key;

    public bool autonomous;
        
    // Use this for initialization
    void Start()
    {
        lineRenderer.enabled = false;
        lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
        lineRenderer.startColor = color;
        lineRenderer.endColor = color;
    }

    void updatePosition()
    {
        
        aPos = origin.position;
        bPos = new Vector3(aPos.x, aPos.y + 1.5f, aPos.z);
        bPos = origin.forward * dist + aPos;
        bPos = new Vector3(bPos.x, bPos.y + 1.5f, bPos.z);


        lineRenderer.SetPosition(0, aPos);
        lineRenderer.enabled = true;

    }

    // Update is called once per frame
    void Update()
    {

        counter += 1f / lineDrawSpeed;

        Debug.LogFormat("counter: {0}", counter);
        
        if(Input.GetKey(key) && autonomous == false)
        {
            if(counter < timeout)
            {
                Debug.Log("INSUFFICIENT TIME BETWEEN ATTACKS");
                return;
            }
            counter = 0;
            updatePosition();
        }

        if (counter < 1)
        {
            float x = Mathf.Lerp(0, dist, counter);

            Vector3 pointA = aPos;
            Vector3 pointB = bPos;

            Vector3 pointAloneLine = x * Vector3.Normalize(pointB - pointA) + pointA;


            lineRenderer.SetPosition(1, pointAloneLine);

        }
        else
        {
            lineRenderer.enabled = false;
            lineRenderer.SetPosition(1, aPos);
        }

        if(autonomous && counter >= timeout)
        {
            counter = 0;
            updatePosition();
        }

        

    }
}
