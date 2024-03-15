using UnityEngine;

public class robot_script_test : MonoBehaviour
{
    private enum RobotState { MovingForward, Rotating, Stopped }

    private RobotState currentState = RobotState.MovingForward;
    private int moveCounter = 0;
    private const int MaxMoves = 2; // Maximum number of movement-rotation cycles
    private const float ForwardVelocity = 10f; // Constant forward velocity
    private const float RotationSpeed = 20f; // Constant rotation speed (degrees per second)
    private const int TargetIterations = 200; // Number of iterations for each movement or rotation action
    public string movement_state = "MANUAL";

    public float movement = 0f;
    public float rotation = 0f;

    private int updateCounter = 0; // Counter for the current number of updates
    public Rigidbody rb; // Rigidbody component for physics interactions

    void Start()
    {
        rb = GetComponent<Rigidbody>(); // Ensure the Rigidbody component is attached and assigned
    }

    void FixedUpdate()
    {
        switch (currentState)
        {
            case RobotState.MovingForward:
                MoveForward();
                break;
            case RobotState.Rotating:
                Rotate();
                break;
            case RobotState.Stopped:
                StopMovement();
                break;
        }

        // Increment the update counter and check if it's time to switch states
        if (++updateCounter >= TargetIterations)
        {
            updateCounter = 0; // Reset the counter for the next action
            SwitchState();
        }
    }

    private void MoveForward()
    {
        movement = ForwardVelocity;
        rotation = 0f;
        rb.velocity = transform.forward * ForwardVelocity;
        rb.angularVelocity = Vector3.zero; // Ensure there's no rotation while moving forward
    }

    private void Rotate()
    {
        movement = 0f;
        rotation = RotationSpeed * Mathf.Deg2Rad;
        rb.velocity = Vector3.zero; // Stop forward movement while rotating
        rb.angularVelocity = Vector3.up * (RotationSpeed * Mathf.Deg2Rad); // Convert degrees to radians for angular velocity
    }

    private void StopMovement()
    {
        movement = 0f;
        rotation = 0f;
        rb.velocity = Vector3.zero;
        rb.angularVelocity = Vector3.zero;
    }

    private void SwitchState()
    {
        if (currentState == RobotState.MovingForward)
        {
            currentState = RobotState.Rotating;
        }
        else if (currentState == RobotState.Rotating)
        {
            moveCounter++;
            currentState = (moveCounter >= MaxMoves) ? RobotState.Stopped : RobotState.MovingForward;
        }
    }

        public void Move(float[] movement_and_rotation)
    {   
         
        
            

    }

}
