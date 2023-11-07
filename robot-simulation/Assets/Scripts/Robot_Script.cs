using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Robot_Script : MonoBehaviour
{
    private float speed = 10.0f;
    private float rotation_speed = 70.0f;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey(KeyCode.D))
        {
            // Rotate right
            transform.Rotate(Vector3.up * rotation_speed * Time.deltaTime);
        }
        if (Input.GetKey(KeyCode.A))
        {
            // Rotate left
            transform.Rotate(Vector3.up * -rotation_speed * Time.deltaTime);
        }

        if (Input.GetKey(KeyCode.W))
        {
            // Move forward in the direction the object is facing
            Vector3 moveDirection = transform.forward * speed * Time.deltaTime;
            transform.position += moveDirection;
        }
        if (Input.GetKey(KeyCode.S))
        {
            // Move backward in the opposite direction
            Vector3 moveDirection = -transform.forward * speed * Time.deltaTime;
            transform.position += moveDirection;
        }
    }

    public void Move(float[] movement_and_rotation)
    {   
        Vector3 moveDirection = transform.forward * movement_and_rotation[0] * Time.deltaTime;
        transform.position += moveDirection;
        transform.Rotate(Vector3.up * movement_and_rotation[1] * Time.deltaTime);
    }



}
