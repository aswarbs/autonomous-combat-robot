
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

    public float checkRadius;

    public int opponentLayer;
        
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
        
        aPos = transform.position;
        aPos = new Vector3(aPos.x, aPos.y + 1.5f, aPos.z);
        if(autonomous)
        {
            Vector3 customTransform = transform.forward;
            customTransform.z -= 3 * (float)Math.PI / 2;
            bPos = customTransform * dist + aPos;
        }
        else
        {
            bPos = transform.forward * dist + aPos;
        }
       


        lineRenderer.SetPosition(0, aPos);
        lineRenderer.enabled = true;

    }


    void checkAttack()
    {

        // Define the layer of the opponent to filter the check
        // This assumes you have an opponent layer set up in your Unity project
        int opponentLayer = LayerMask.NameToLayer("Opponent");
        int layerMask = 1 << opponentLayer;

        // Perform the overlap sphere check
        Collider[] hitColliders = Physics.OverlapSphere(bPos, checkRadius, layerMask);

        // Check if any of the colliders belong to the opponent
        if (hitColliders.Length > 0)
        {
            // At least one opponent is within the attack range
            Debug.Log("Opponent hit!");

            // player.handleHit()  // opponent.handleHit()
        }
        else
        {
            // No opponent is within the attack range
            Debug.Log("Attack missed.");

            // player.handleMiss()  // opponent.handleMiss()
        }
    }

    public void ExecuteAttack()
    {
        if(counter < timeout)
        {
            Debug.Log("INSUFFICIENT TIME BETWEEN ATTACKS");
            return;
        }
        counter = 0;
        updatePosition();
        checkAttack();
    }

    

    // Update is called once per frame
    void Update()
    {

        counter += 1f / lineDrawSpeed;
        

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

        if(counter >= timeout)
        {
            if(autonomous)
            {
                counter = 0;
                updatePosition();
            }
            
        }
        

    }
}
