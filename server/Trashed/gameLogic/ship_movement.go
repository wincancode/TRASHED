package gameLogic

import (
	"Trashed/Trashed/proto"
	"math"
)

// ShipState represents the state of a ship in the game world.
type ShipState struct {
	PlayerUuid string
	PosX      float64
	PosY      float64
	Angle     float64
	Speed     float64
}

// MovementInput represents the input for a ship's movement.
type MovementInput struct {
	Move        bool
	StrideLeft  bool
	StrideRight bool
	Stop        bool
	IsShoot     bool
}

func degreesToRadians(degrees float64) float64 {
	return degrees * math.Pi / 180
}

// UpdateShipPosition updates the ship's position and angle based on the input and current state, matching the Python and proto logic.
// Angle is stored in radians.
func UpdateShipPosition(position *proto.Position, input *proto.Input, deltaTime float64) (*proto.Position) {
	const (
		shipAcceleration    = 60   // units per second
		turnSpeed    = 1.2   // radians per second
		deceleration = 0.98   // stop deceleration factor
	)

	if position == nil {
		position = &proto.Position{X: 0, Y: 0}
	}


	
	// Calculate acceleration in the direction the ship is facing
	accelerationX := 0.0
	accelerationY := 0.0
	if input.Move {
		accelerationX = shipAcceleration * math.Sin(degreesToRadians(position.Angle))
		accelerationY = -shipAcceleration * math.Cos(degreesToRadians(position.Angle))
	} else {
		accelerationX = 0
		accelerationY = 0
	}

	// Stop: apply deceleration
	if input.Stop {
		accelerationX = 0
		accelerationY = 0
		// Apply rapid deceleration to speed (mimic Python logic)
		position.SpeedX *= deceleration
		position.SpeedY *= deceleration
	}


	


	// Rotation (left/right)
	if input.StrideLeft {
		position.Angle -= turnSpeed  
	}
	if input.StrideRight {
		position.Angle += turnSpeed 
	}

	if position.Angle > 360{
		position.Angle -= 360
	} else {
		if position.Angle < 0{
			position.Angle += 360
		}

	}
	

	// Update velocity based on acceleration
	position.SpeedX += accelerationX * deltaTime
	position.SpeedY += accelerationY * deltaTime

	// Apply friction if not accelerating
	if accelerationX == 0 {
		position.SpeedX -= shipAcceleration * deltaTime * sign(position.SpeedX)
		if math.Abs(position.SpeedX) < 0.01 {
			position.SpeedX = 0
		}
	}
	if accelerationY == 0 {
		position.SpeedY -= shipAcceleration * deltaTime * sign(position.SpeedY)
		if math.Abs(position.SpeedY) < 0.01 {
			position.SpeedY = 0
		}
	}

	// Update position based on velocity
	position.X += position.SpeedX * deltaTime
	position.Y += position.SpeedY * deltaTime

	// Store acceleration in the position struct
	position.AccelerationX = accelerationX
	position.AccelerationY = accelerationY

	return position
}

func sign(x float64) float64 {
	if x > 0 {
		return 1
	} else if x < 0 {
		return -1
	}
	return 0
}



