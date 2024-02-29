using UnityEngine;
public class VehicleControllerScript : MonoBehaviour
{
    public InputControllerScript InputCtrl;
    [Tooltip("Set ref in order of FL, FR, RL, RR")]
    public WheelCollider[] WheelColliders;

    [Tooltip("Set ref of wheel meshes in order of  FL, FR, RL, RR")]
    public Transform[] Wheels;

    public Transform CenterOfMass;

    public int Force;
    public int Angle;
    public int BrakeForce;

    private void Start()
    {
        GetComponent<Rigidbody>().centerOfMass = CenterOfMass.localPosition;
    }

    private void FixedUpdate()
    {
        Steer();
        Drive();
        Brake();
        UpdateWheelMovements();
    }
	
	//Drive forward/backward
    private void Drive()
    {
        WheelColliders[0].motorTorque = WheelColliders[1].motorTorque = InputCtrl.Vertical * Force;
    }
    
	//Steer left/right
    private void Steer()
    {
        WheelColliders[0].steerAngle = WheelColliders[1].steerAngle = InputCtrl.Horizontal * Angle;
    }

	//Apply brakes
    private void Brake()
    {
        WheelColliders[0].brakeTorque = WheelColliders[1].brakeTorque = InputCtrl.Brake * BrakeForce;
    }

	//imitate the wheelcollider movements onto the wheel-meshes
    private void UpdateWheelMovements()
    {
        for (var i = 0; i < Wheels.Length; i++)
        {
            Vector3 pos;
            Quaternion rot;
            WheelColliders[i].GetWorldPose(out pos, out rot);
            Wheels[i].transform.position = pos;
            Wheels[i].transform.rotation = rot;
        }
    }
}