using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using UnityEngine.UI;


public class Robot_Script : MonoBehaviour
{   
    public float move_speed = 5f;
    public float rotation_speed = 30f;
    public Rigidbody rb;

    public int movement_const = 10;

    public string movement_state = "MANUAL";

    public Text robot_state_label;

    


    // Start is called before the first frame update
    void Start()
    {
        robot_state_label.text = "Current Movement: " + movement_state;
    }

    void HandleKeyPress()
    {

        if(movement_state == "MANUAL")
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

        if (Input.GetKeyUp(KeyCode.Q))
        {
            // change mode from manual to autonomous

            if(movement_state == "MANUAL")
            {
                movement_state = "AUTO";
            }
            else if(movement_state == "AUTO")
            {
                rb.velocity = transform.forward * 0;
                rb.angularVelocity =  Vector3.up * 0;
                movement_state = "MANUAL";
            }
            else
            {
                Debug.Log("INVALID MOVEMENT STATE");
            }

            robot_state_label.text = "Current Movement: " + movement_state;
        }
    }

    

    // Update is called once per frame
    void Update()
    {

        HandleKeyPress();

    }

    public void Move(float[] movement_and_rotation)
    {   
        if(movement_state == "AUTO")
        {
            rb.velocity = transform.forward * movement_and_rotation[0] * movement_const;
            Debug.Log(transform.forward);
            rb.angularVelocity = Vector3.up * movement_and_rotation[1];
        }        

    }


}