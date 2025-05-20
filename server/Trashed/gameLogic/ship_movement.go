package gameLogic

import (
	"Trashed/Trashed/proto"
	"math"
	"time"
)

// ShipState represents the state of a ship in the game world.
type ShipState struct {
	PlayerUuid      string
	PosX            float64
	PosY            float64
	Angle           float64
	Speed           float64
	LaserBoostLevel int
	ShieldActive    bool
	ShieldCharges   int
	Lives           int
	LastShotTime    time.Time
	
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
// Now uses ShipState instead of proto.Position.
func UpdateShipPosition(ship *ShipState, input *proto.Input, deltaTime float64) *ShipState {
	const (
		shipAcceleration = 60   // units per second
		turnSpeed       = 1.2   // radians per second
		deceleration    = 0.98  // stop deceleration factor
	)

	if ship == nil {
		ship = &ShipState{}
	}

	// Calculate acceleration in the direction the ship is facing
	accelerationX := 0.0
	accelerationY := 0.0
	if input.Move {
		accelerationX = shipAcceleration * math.Sin(degreesToRadians(ship.Angle))
		accelerationY = -shipAcceleration * math.Cos(degreesToRadians(ship.Angle))
	} else {
		accelerationX = 0
		accelerationY = 0
	}

	// Stop: apply deceleration
	if input.Stop {
		accelerationX = 0
		accelerationY = 0
		// Apply rapid deceleration to speed (mimic Python logic)
		ship.Speed *= deceleration
	}

	// Rotation (left/right)
	if input.StrideLeft {
		ship.Angle -= turnSpeed
	}
	if input.StrideRight {
		ship.Angle += turnSpeed
	}

	if ship.Angle > 360 {
		ship.Angle -= 360
	} else if ship.Angle < 0 {
		ship.Angle += 360
	}

	// Update velocity based on acceleration
	vx := ship.Speed * math.Sin(degreesToRadians(ship.Angle))
	vy := -ship.Speed * math.Cos(degreesToRadians(ship.Angle))
	vx += accelerationX * deltaTime
	vy += accelerationY * deltaTime

	// Limit speed to maximum speed
	maxSpeed := 200.0 // Maximum speed
	if math.Sqrt(vx*vx+vy*vy) > maxSpeed {
		speedFactor := maxSpeed / math.Sqrt(vx*vx+vy*vy)
		vx *= speedFactor
		vy *= speedFactor
	}
	


	// Apply friction if not accelerating
	if accelerationX == 0 {
		vx -= shipAcceleration * deltaTime * sign(vx)
		if math.Abs(vx) < 0.01 {
			vx = 0
		}
	}
	if accelerationY == 0 {
		vy -= shipAcceleration * deltaTime * sign(vy)
		if math.Abs(vy) < 0.01 {
			vy = 0
		}
	}

	// Update position based on velocity
	ship.PosX += vx * deltaTime
	ship.PosY += vy * deltaTime

	// if the ship is out of bounds, wrap around the screen
	if ship.PosX < 0 {
		ship.PosX += 800 // Assuming screen width is 800
	} else if ship.PosX > 800 {
		ship.PosX -= 800
	}
	if ship.PosY < 0 {
		ship.PosY += 600 // Assuming screen height is 600
	} else if ship.PosY > 600 {
		ship.PosY -= 600
	}



	// Store speed for next tick
	ship.Speed = math.Sqrt(vx*vx + vy*vy)

	return ship
}

func sign(x float64) float64 {
	if x > 0 {
		return 1
	} else if x < 0 {
		return -1
	}
	return 0
}



