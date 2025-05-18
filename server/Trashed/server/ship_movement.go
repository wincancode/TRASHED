package main

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

// UpdateShipPosition updates the ship's position based on the input and current state.
func UpdateShipPosition(ship *ShipState, input *proto.Input, deltaTime float64) {
	const (
		moveSpeed   = 80.0 // units per second
		turnSpeed   = 1.2 // degrees per second
	)

	if input.Move {
		ship.PosY -= moveSpeed * deltaTime * math.Cos(ship.Angle)
		ship.PosX += moveSpeed * deltaTime * math.Sin(ship.Angle)
	}
	if input.StrideLeft {
		ship.Angle -= turnSpeed * deltaTime
	}
	if input.StrideRight {
		ship.Angle += turnSpeed * deltaTime
	}
	if input.Stop {
		// Optionally implement deceleration or stop logic
	}
	// Shooting logic can be handled elsewhere
}


