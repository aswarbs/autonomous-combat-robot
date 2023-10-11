using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class Robot_Script : MonoBehaviour
{

    private float speed = 10.0f;
    public GameObject robot;

// Start is called before the first frame update
    void Start()
        {
        
        }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.D))
        {
            transform.position += Vector3.right * speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.A))
        {
            transform.position += Vector3.left * speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.W))
        {
            transform.position += Vector3.forward * speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.S))
        {
            transform.position += Vector3.back * speed * Time.deltaTime;
        }
    }
}
