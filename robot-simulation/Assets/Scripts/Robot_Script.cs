using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Robot_Script : MonoBehaviour
{   
    public float move_speed = 5f;
    public float rotation_speed = 30f;
    public float velocity_speed = 100f;

    public float turning_velocity = 0.2f;

    public Rigidbody rb;


    // Start is called before the first frame update
    void Start()
    {

    }

    void HandleKeyPress()
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
            Vector3 moveDirection = transform.forward * move_speed * Time.deltaTime;
            transform.position += moveDirection;
        }
        if (Input.GetKey(KeyCode.S))
        {
            // Move backward in the opposite direction
            Vector3 moveDirection = -transform.forward * move_speed * Time.deltaTime;
            transform.position += moveDirection;
        }
    }

    

    // Update is called once per frame
    void Update()
    {

        HandleKeyPress();

    }

    public void Move(float[] movement_and_rotation)
    {   
        rb.velocity = transform.forward * movement_and_rotation[0];
        rb.angularVelocity = Vector3.up * movement_and_rotation[1] * turning_velocity;
        
        

    }


}
